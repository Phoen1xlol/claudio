# -*- coding: utf-8 -*-
"""
Goldfish Monte Carlo — Broodscale Lab build.
Confronta la lista attuale con varianti che aggiungono Something Worth Saving (SWS).
Nessun avversario. London mulligan semplificato. Turni 1-8.

Uso:  python sim_broodscale.py [N_partite]   (default 20000; per risultati seri 100000)
Output: sim_out.json nella stessa cartella + tabella a schermo.
"""
import random, sys, json, os
from collections import Counter, defaultdict

FOREST_T = {"Forest", "Yavimaya", "Boseiju", "Woodland"}
LANDS = FOREST_T | {"Temple", "Lab", "Saga", "Cavern", "Gemstone"}

TYPES = {
    "Forest": {"land"}, "Yavimaya": {"land"}, "Boseiju": {"land"}, "Woodland": {"land"},
    "Temple": {"land"}, "Lab": {"land"}, "Cavern": {"land"}, "Gemstone": {"land"},
    "Saga": {"land", "enchantment"},
    "Stirrings": {"sorcery"}, "Rumble": {"sorcery"},
    "SWS": {"instant"}, "Dismember": {"instant"}, "Command": {"instant", "kindred"},
    "Blade": {"artifact"}, "Bauble": {"artifact"}, "Lantern": {"artifact"},
    "Drum": {"artifact"}, "Talisman": {"artifact"}, "Mite": {"artifact", "creature"},
    "Broodscale": {"creature"}, "Mycospawn": {"creature"}, "Devourer": {"creature"},
    "Emrakul": {"creature"}, "Fleshraker": {"creature"},
}
ELDRAZI = {"Broodscale", "Mycospawn", "Devourer", "Emrakul", "Fleshraker", "Command"}
COLORLESS_SPELL = (ELDRAZI - {"Broodscale", "Mycospawn"}) | {"Blade", "Bauble", "Lantern", "Drum",
                                                            "Talisman", "Mite"}
COLORLESS_CARD = COLORLESS_SPELL | {"Broodscale", "Mycospawn"} | LANDS   # Ancient Stirrings
PERMANENT = LANDS | {"Blade", "Bauble", "Lantern", "Drum", "Talisman", "Mite",
                     "Broodscale", "Mycospawn", "Devourer", "Emrakul", "Fleshraker"}
GREEN_SPELLS = {"Stirrings", "Rumble", "SWS", "Broodscale", "Mycospawn"}
# costo: (generico, G, C)
COST = {"Stirrings": (0, 1, 0), "Rumble": (1, 1, 0), "SWS": (1, 1, 0), "Broodscale": (1, 1, 0),
        "Blade": (1, 0, 0), "Bauble": (1, 0, 0), "Lantern": (1, 0, 0), "Drum": (1, 0, 0),
        "Talisman": (2, 0, 0), "Mycospawn": (3, 1, 0), "Fleshraker": (2, 0, 1),
        "Devourer": (5, 0, 2)}

# Lista di Ross Merriam in stream (14/09/2026) con 1 Fleshraker al posto di 1 Dismember
BASE_LANDS = {"Boseiju": 2, "Cavern": 1, "Temple": 4, "Forest": 6, "Gemstone": 1,
              "Woodland": 1, "Lab": 3, "Saga": 4, "Yavimaya": 1}
BASE_SPELLS = {"Stirrings": 4, "Blade": 3, "Mite": 1, "Lantern": 1, "Drum": 1, "Bauble": 1,
               "Broodscale": 4, "Rumble": 4, "Talisman": 1, "Dismember": 1, "Fleshraker": 1,
               "Mycospawn": 4, "Devourer": 3, "Command": 4, "Emrakul": 4}


def deck(changes):
    d = Counter(BASE_LANDS) + Counter(BASE_SPELLS)
    for k, v in changes.items():
        d[k] += v
        if d[k] <= 0:
            del d[k]
    assert sum(d.values()) == 60, sum(d.values())
    return [c for c, n in d.items() for _ in range(n)]


class G:
    def __init__(self, cards, on_play, rng):
        self.rng = rng
        self.lib = cards[:]
        rng.shuffle(self.lib)
        self.hand, self.gy, self.bf = [], [], []
        self.spawn = 0
        self.turn = 0
        self.on_play = on_play
        self.seen = 0
        self.land_played = False
        self.missed_land = 0
        self.emrakul_turn = None
        self.max_emr_hand = 0
        self.labs = self.labs_imp = 0
        self.pending_sac = []
        self.gscrew = False

    def draw(self, n=1):
        for _ in range(n):
            if self.lib:
                self.hand.append(self.lib.pop(0))
                self.seen += 1

    def gy_types(self):
        t = set()
        for c in self.gy:
            t |= TYPES[c]
        return t

    def lands_bf(self):
        return [p for p in self.bf if p["name"] in LANDS]

    def has_yav(self):
        return any(p["name"] == "Yavimaya" for p in self.bf)

    def creatures(self):
        return self.spawn + sum(1 for p in self.bf if "creature" in TYPES[p["name"]])

    def on_bf(self, n):
        return any(p["name"] == n for p in self.bf)

    # ---- mana
    def sources(self):
        out = []
        for p in self.bf:
            if p["tapped"]:
                continue
            n = p["name"]
            if n in LANDS or n == "Talisman" or (n == "Drum" and self.creatures() > 0):
                out.append(p)
        return out

    def yield_of(self, p, spell):
        n, yav = p["name"], self.has_yav()
        if n in FOREST_T:
            return 1, True, False
        if n == "Temple":
            return (2 if spell in ELDRAZI else 1), yav, True
        if n == "Lab":
            return (2 if p["imprint"] and spell in COLORLESS_SPELL else 1), yav, True
        if n in ("Saga", "Gemstone"):
            return 1, yav, True
        if n == "Cavern":
            return 1, (yav or (spell in ELDRAZI and spell != "Command")), True
        if n == "Talisman":
            return 1, True, True
        if n == "Drum":
            return 1, True, False
        return 0, False, False

    def pay(self, spell, generic, g, c, commit=True):
        srcs = self.sources()
        info = {id(p): self.yield_of(p, spell) for p in srcs}
        used, spawn_used, leftover = set(), 0, 0

        def pick(pred, key):
            cand = [p for p in srcs if id(p) not in used and pred(p)]
            return min(cand, key=key) if cand else None

        rank_g = {"Forest": 0, "Boseiju": 0, "Woodland": 0, "Yavimaya": 0, "Drum": 1,
                  "Talisman": 2, "Cavern": 3, "Gemstone": 4, "Saga": 4, "Temple": 6, "Lab": 6}
        for _ in range(g):
            p = pick(lambda p: info[id(p)][1], lambda p: rank_g.get(p["name"], 5))
            if p is None:
                return False
            used.add(id(p))
            leftover += info[id(p)][0] - 1
        cneed = c
        while cneed > 0:
            p = pick(lambda p: info[id(p)][2], lambda p: -info[id(p)][0])
            if p is None:
                if self.spawn - spawn_used > 0:
                    spawn_used += 1; cneed -= 1; continue
                return False
            used.add(id(p)); cneed -= info[id(p)][0]
        leftover += max(0, -cneed)
        need = generic - leftover
        while need > 0:
            p = pick(lambda p: True, lambda p: (-info[id(p)][0], p["name"] in FOREST_T))
            if p is None:
                if self.spawn - spawn_used > 0:
                    spawn_used += 1; need -= 1; continue
                return False
            used.add(id(p)); need -= info[id(p)][0]
        if commit:
            for p in srcs:
                if id(p) in used:
                    p["tapped"] = True
            self.spawn -= spawn_used
        return True

    # ---- scelte
    def imprint_target(self):
        if "Devourer" in self.hand:
            return "Devourer"
        if self.hand.count("Emrakul") >= 2:
            return "Emrakul"
        return None

    def g_source_on_bf(self):
        yav = self.has_yav()
        return any(p["name"] in FOREST_T or p["name"] in ("Talisman", "Drum") or
                   (yav and p["name"] in LANDS) for p in self.bf)

    def choose_land(self):
        lands = [c for c in self.hand if c in LANDS]
        if not lands:
            return None
        if "Lab" in lands and self.imprint_target():
            return "Lab"
        if any(c in GREEN_SPELLS for c in self.hand) and not self.g_source_on_bf():
            for n in ("Yavimaya", "Forest", "Boseiju", "Woodland"):
                if n in lands:
                    return n
        if "Temple" in lands:
            return "Temple"
        if "Saga" in lands and self.turn <= 4:
            return "Saga"
        for n in ("Yavimaya", "Forest", "Boseiju", "Woodland", "Cavern", "Gemstone", "Saga", "Lab"):
            if n in lands:
                return n
        return lands[0]

    def play_land(self, n):
        self.hand.remove(n)
        p = {"name": n, "tapped": n == "Woodland" and not any(q["name"] in FOREST_T for q in self.bf),
             "imprint": None, "turn_in": self.turn}
        if n == "Lab":
            self.labs += 1
            t = self.imprint_target()
            if t:
                self.hand.remove(t); p["imprint"] = t; self.labs_imp += 1
        self.bf.append(p)
        self.land_played = True

    def pick_score(self, c):
        lands_hand = sum(1 for x in self.hand if x in LANDS)
        if c in LANDS and lands_hand == 0 and len(self.lands_bf()) < 7:
            return 100 + {"Temple": 6, "Saga": 2}.get(c, 1)
        if c == "Emrakul" and "Emrakul" not in self.hand:
            return 90
        lab_waiting = "Lab" in self.hand or any(p["name"] == "Lab" and not p["imprint"] for p in self.bf)
        if c == "Devourer" and lab_waiting and not self.imprint_target():
            return 80
        if c == "Temple":
            return 70
        if c == "Mycospawn":
            return 50
        if c == "Broodscale" and "Broodscale" not in self.hand and not self.on_bf("Broodscale"):
            return 45
        if c == "Blade" and "Blade" not in self.hand and not self.on_bf("Blade"):
            return 44
        if c in LANDS:
            return 40
        if c == "Talisman":
            return 35
        return 10

    def take_best(self, pool, allowed):
        cand = [c for c in pool if c in allowed]
        return max(cand, key=self.pick_score) if cand else None

    # ---- magie
    def cast_dig(self, name):
        gen, g, c = COST[name]
        if not self.pay(name, gen, g, c):
            return False
        self.hand.remove(name)
        if name == "Stirrings":
            top, self.lib = self.lib[:5], self.lib[5:]
            self.seen += len(top)
            b = self.take_best(top, COLORLESS_CARD)
            if b:
                top.remove(b); self.hand.append(b)
            self.rng.shuffle(top); self.lib += top
        else:
            top, self.lib = self.lib[:4], self.lib[4:]
            self.seen += len(top)
            b = self.take_best(top, PERMANENT)
            if b:
                top.remove(b); self.hand.append(b)
            self.gy += top
            if name == "Rumble":
                self.spawn += 1
        self.gy.append(name)
        return True

    def cast_command(self):
        for x in range(6, 0, -1):
            if self.pay("Command", x, 0, 2, commit=False):
                self.pay("Command", x, 0, 2)
                self.hand.remove("Command")
                self.spawn += x
                top, self.lib = self.lib[:x], self.lib[x:]
                self.seen += len(top)
                b = self.take_best(top, set(TYPES))
                if b:
                    top.remove(b); self.hand.append(b)
                self.lib += top
                self.gy.append("Command")
                return True
        return False

    def cast_perm(self, name):
        gen, g, c = COST[name]
        if not self.pay(name, gen, g, c):
            return False
        self.hand.remove(name)
        p = {"name": name, "tapped": False, "imprint": None, "turn_in": self.turn}
        self.bf.append(p)
        if name == "Mycospawn":
            lands = [x for x in self.lib if x in LANDS]
            if lands:
                pref = ["Temple", "Lab", "Yavimaya", "Forest", "Boseiju", "Saga", "Cavern", "Gemstone", "Woodland"]
                land = min(lands, key=pref.index)
                self.lib.remove(land)
                self.bf.append({"name": land, "tapped": True, "imprint": None, "turn_in": self.turn})
        if name in ("Bauble", "Lantern"):
            self.pending_sac.append(p)
        return True

    def try_emrakul(self):
        if "Emrakul" not in self.hand:
            return False
        if self.pay("Emrakul", max(0, 13 - len(self.gy_types())), 0, 0):
            self.hand.remove("Emrakul")
            self.emrakul_turn = self.turn
            return True
        return False

    def saga_step(self):
        for p in list(self.bf):
            if p["name"] == "Saga" and self.turn - p["turn_in"] == 2:
                has_brood = "Broodscale" in self.hand or self.on_bf("Broodscale")
                has_blade = "Blade" in self.hand or self.on_bf("Blade")
                order = (["Blade"] if has_brood and not has_blade else []) + \
                        ["Drum", "Bauble", "Lantern", "Blade", "Mite"]
                for t in order:
                    if t in self.lib:
                        self.lib.remove(t)
                        q = {"name": t, "tapped": False, "imprint": None, "turn_in": self.turn}
                        self.bf.append(q)
                        if t in ("Bauble", "Lantern"):
                            self.pending_sac.append(q)
                        break
                self.bf.remove(p)
                self.gy.append("Saga")

    def main(self):
        for _ in range(40):
            if not self.land_played:
                n = self.choose_land()
                if n:
                    self.play_land(n)
            if self.try_emrakul():
                return
            acted = False
            for name in ["Talisman", "Mycospawn", "Rumble", "Stirrings", "SWS"]:
                if name in self.hand:
                    ok = self.cast_perm(name) if name in ("Talisman", "Mycospawn") else self.cast_dig(name)
                    if ok:
                        acted = True; break
            if acted:
                continue
            if "Command" in self.hand and self.cast_command():
                continue
            for name in ["Broodscale", "Blade", "Drum", "Fleshraker", "Bauble", "Lantern", "Devourer"]:
                if name in self.hand:
                    if name == "Broodscale" and self.on_bf("Broodscale"):
                        continue
                    if name == "Drum" and self.creatures() == 0:
                        continue
                    if self.cast_perm(name):
                        acted = True; break
            if acted:
                continue
            for p in list(self.pending_sac):
                if p["turn_in"] < self.turn and p in self.bf:
                    if p["name"] == "Lantern" or self.pay("Bauble", 1, 0, 0):
                        self.bf.remove(p); self.pending_sac.remove(p)
                        self.gy.append(p["name"]); self.draw()
                        acted = True; break
            if not acted:
                return

    def take_turn(self):
        self.turn += 1
        for p in self.bf:
            p["tapped"] = False
        self.land_played = False
        if not (self.on_play and self.turn == 1):
            self.draw()
        self.saga_step()
        self.main()
        if not self.land_played:
            self.missed_land += 1
        if self.turn == 3 and any(c in GREEN_SPELLS for c in self.hand) and not self.g_source_on_bf():
            self.gscrew = True
        self.max_emr_hand = max(self.max_emr_hand, self.hand.count("Emrakul"))


def mulligan(cards, rng, on_play):
    for size in (7, 6, 5):
        g = G(cards, on_play, rng)
        g.draw(7)
        nl = sum(1 for c in g.hand if c in LANDS)
        if 2 <= nl <= 5 or size == 5:
            for _ in range(7 - size):
                lands = [c for c in g.hand if c in LANDS]
                if len(lands) > 3:
                    bad = next((c for c in ("Gemstone", "Cavern", "Woodland", "Boseiju", "Forest") if c in g.hand), lands[0])
                else:
                    pri = ["Devourer", "Emrakul", "Dismember", "Mite", "Fleshraker", "Lantern", "Bauble",
                           "Command", "Blade", "Broodscale", "Drum", "Talisman", "Mycospawn", "SWS", "Rumble", "Stirrings"]
                    bad = next((c for c in pri if c in g.hand), g.hand[0])
                g.hand.remove(bad); g.lib.append(bad)
            return g, 7 - size


def run(cards, n, on_play, seed):
    rng = random.Random(seed)
    R = defaultdict(float)
    for _ in range(n):
        g, mull = mulligan(cards, rng, on_play)
        R["mull"] += mull > 0
        for t in range(1, 9):
            if g.emrakul_turn is None:
                g.take_turn()
            else:
                g.turn += 1
            if t in (3, 4, 5, 6):
                ty = len(g.gy_types())
                R[f"types_T{t}"] += ty
                R[f"types5_T{t}"] += ty >= 5
                R[f"seen_T{t}"] += g.seen
                R[f"lands_T{t}"] += len(g.lands_bf())
                R[f"access_T{t}"] += ("Emrakul" in g.hand) or g.emrakul_turn is not None
                R[f"stuck_T{t}"] += ("Emrakul" in g.hand) and g.emrakul_turn is None
                brood = "Broodscale" in g.hand or g.on_bf("Broodscale")
                blade = "Blade" in g.hand or g.on_bf("Blade")
                R[f"combo_T{t}"] += brood and blade
            if t == 4:
                R["miss_T4"] += g.missed_land > 0
        et = g.emrakul_turn
        for t in (4, 5, 6, 7, 8):
            R[f"emr_by_T{t}"] += et is not None and et <= t
        R["clog2"] += g.max_emr_hand >= 2
        R["gscrew"] += g.gscrew
        R["labs"] += g.labs
        R["labs_imp"] += g.labs_imp
    out = {k: v / n for k, v in R.items()}
    out["imp_rate"] = R["labs_imp"] / R["labs"] if R["labs"] else 0
    return out


CONFIGS = {
    "A attuale": {},
    "B proposta": {"Devourer": -1, "Emrakul": -1, "Fleshraker": -1, "SWS": 3},
    "C tieni 3 Devourer": {"Emrakul": -1, "Fleshraker": -1, "SWS": 2},
    "D tieni 4 Emrakul": {"Devourer": -1, "Fleshraker": -1, "SWS": 2},
}

KEYS = ["emr_by_T5", "emr_by_T6", "emr_by_T7", "access_T6", "stuck_T6", "clog2", "types_T4",
        "types_T5", "types5_T5", "seen_T4", "seen_T5", "lands_T4", "miss_T4", "imp_rate",
        "combo_T4", "gscrew", "mull"]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    res = {}
    for name, ch in CONFIGS.items():
        cards = deck(ch)
        res[name] = {"play": run(cards, N, True, 11), "draw": run(cards, N, False, 22)}
        print(name, "ok", flush=True)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_out.json")
    json.dump(res, open(out_path, "w"), indent=1)
    for side in ("play", "draw"):
        print("\n==", side)
        print(f"{'metrica':12}" + "".join(f"{k[:18]:>20}" for k in res))
        for k in KEYS:
            print(f"{k:12}" + "".join(f"{res[c][side][k]:>20.3f}" for c in res))
