# Metodo: estrarre partite e decklist da melee.gg

Messo a punto nella chat "Analisi dati ultimi challenge magiconline" (settembre 2026). In quella chat girava come JavaScript dentro una pagina melee.gg aperta in Chrome, con l'utente loggato, tramite Claude in Chrome. Con web_fetch o curl non funziona: la pagina carica tutto via AJAX e servono i cookie di sessione.

## Eventi già estratti

| Evento | ID melee | Note |
|---|---|---|
| Spotlight Brisbane | 441441 | 2.360 match, 18 round; nomi liste scritti dai giocatori (143 nomi distinti, 66% normalizzati) |
| Spotlight Dallas | 405590 | 3.612 match; chiuso dal 5 settembre |
| RC Baltimore | 405588 | 6.022 match, 15 round + top 8; nomi normalizzati dall'organizzatore. Taglio day 2 tra r9 (303 match) e r10 (168) |
| Pro Tour Amsterdam (Marvel Super Heroes) | 434455 | 17-19 luglio, pre-ban, 19 round, ~150 giocatori, 1.420 match |
| RC Hangzhou | 451148 | 1.399 match, 9 round + top 8, ~400 giocatori, solo 631 normalizzati |

URL: `https://melee.gg/Tournament/View/<ID>`

## Endpoint

- **Round**: nella pagina del torneo, `#pairings-round-selector-container .round-selector` → `dataset.id` (roundId) e `dataset.name`.
- **Match di un round**: `POST /Match/GetRoundMatches/<roundId>`, DataTables server-side, body `application/x-www-form-urlencoded`, header `X-Requested-With: XMLHttpRequest`, `credentials: 'include'`. Pagina con `start`/`length` (500) fino a `recordsTotal`.
- **Risposta**: `j.data[]` → `m.Competitors[]` → per ciascuno:
  - `c.Decklists[0].DecklistName` (nome archetipo)
  - `c.Decklists[0].DecklistId`
  - `c.GameWins + c.GameByes` (game vinti)
  - `c.Team.Players[0].Username`
- **Decklist**: `GET /Decklist/View/<DecklistId>` → HTML → `#decklist-text` (value/textContent). Ha le sezioni "Maindeck" e "Sideboard", righe `N Nome carta`. Conviene scaricarle a blocchi paralleli da 14-30.

## Snippet (da eseguire nella pagina del torneo)

```js
const path='/Match/GetRoundMatches';
const rounds=[...document.querySelectorAll('#pairings-round-selector-container .round-selector')].map(b=>b.dataset.id);
const mkBody=(s,l)=>{const p=new URLSearchParams();p.set('draw','1');p.set('start',String(s));p.set('length',String(l));
 p.set('search[value]','');p.set('search[regex]','false');
 ['Table','Competitor','Result','Decklists'].forEach((n,i)=>{p.set(`columns[${i}][data]`,n);p.set(`columns[${i}][name]`,n);
  p.set(`columns[${i}][searchable]`,'true');p.set(`columns[${i}][orderable]`,'true');
  p.set(`columns[${i}][search][value]`,'');p.set(`columns[${i}][search][regex]`,'false');});return p;};
const raw=[];
for(let ri=0;ri<rounds.length;ri++){let start=0;
 while(true){
  const res=await fetch(`${path}/${rounds[ri]}`,{method:'POST',credentials:'include',
    headers:{'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest'},
    body:mkBody(start,500)});
  if(!res.ok)break; const j=await res.json();
  for(const m of (j.data||[])){
   const cs=(m.Competitors||[]).map(c=>({id:c.Decklists?.[0]?.DecklistId||null,
     nm:c.Decklists?.[0]?.DecklistName||null, g:(c.GameWins||0)+(c.GameByes||0)}));
   if(cs.length===2&&cs[0].id&&cs[1].id) raw.push([ri+1,cs[0].id,cs[0].nm,cs[0].g,cs[1].id,cs[1].nm,cs[1].g]);
  }
  start+=500; if(start>=(j.recordsTotal||0))break;}}
// raw = [round, idA, nomeA, gameA, idB, nomeB, gameB]
```

Parser delle decklist:

```js
const parse=txt=>{let sec='main';const main={},side={};
 for(const line of txt.split('\n')){const s=line.trim();if(!s)continue;
  if(/^maindeck/i.test(s)){sec='main';continue;} if(/^sideboard/i.test(s)){sec='side';continue;}
  const m=s.match(/^(\d+)\s+(.+)$/);if(!m)continue;const t=sec==='main'?main:side;
  t[m[2].trim()]=(t[m[2].trim()]||0)+(+m[1]);} return {main,side};};
// fetch(`/Decklist/View/${id}`,{credentials:'include'}) -> DOMParser -> querySelector('#decklist-text')
```

Consiglio: salva i dati grezzi in JSON su disco invece che nel localStorage del browser, così non si perdono quando Chrome si scollega (in chat è successo più volte).

## Normalizzazione degli archetipi (regex, l'ordine conta)

```
goryo → Goryo's | broodscale → Broodscale | devoted druid|abzan combo → Devoted | amulet → Amulet Titan
neoform → Neoform | living end → Living End | ruby storm|mono-red storm|mono-red combo → Ruby Storm
land destruction → Boros Ponza | eldrazi tron → Eldrazi Tron
eldrazi trudge|eldrazi ramp|mono-green eldrazi\b → MG Eldrazi | prowess → Izzet Prowess | affinity → Affinity
esper blink → Esper Blink | azorius blink|orzhov blink → Azorius Blink
jeskai energy|boros energy|azorius energy|\benergy\b → Energy | domain zoo|zoo → Domain Zoo
hollow one | belcher | yawgmoth | burn | merfolk | mill | necro → Necrodominance | reanimator → Reanimator
\btron\b → Tron | dimir (midrange|control) → Dimir | jeskai control|azorius control|dimir control → Control
loki → Azorius Loki
```

Sinonimi fra fonti diverse (dettati da Paolo): UR Cutter Prowess = Izzet Prowess; Instant Reanimator / Esper Reanimator = Goryo's; Reanimator = Dimir Persist; UrzaTron = Eldrazi Tron; 4/5c Aggro = Domain Zoo; Eldrazi Ramp (mtgdecks) = Fight Rigging/Trudge; Pinnacle Affinity / Izzet Metalcraft = Affinity; Allosaurus = Neobrand; Boros Wildfire = Boros Ponza (= Boros Land Destruction/Kaheera); Broodscale Bloodchief / Eldrazi Bloodchief Combo = Broodscale; Oswald Grinding Cam = Azorius Emry/Oswald.

Le liste senza nome (solo colori, es. "Mono-Green", "W-U-B-G") vanno classificate dalle carte. È il passo che manca ancora.

## Regole di metodo imparate (vedi anche il file principale)

- WR = vittorie/(vittorie+sconfitte). **Stampa sempre "partite decise"**, non il totale con i pareggi (bug trovato da Paolo).
- Celle sotto ~20 partite: indicative. Sotto 5: non mostrarle.
- Day 2 = round 10+ negli eventi da 15 round. Filtrare sul day 2 comprime verso il 50%.
- Split per carta: prima chiedersi se la carta **entra fisicamente** in quel matchup. Se no, è un marcatore (pilota preparato, lista aggiornata), non una causa.
- Varianti di build: classificare per **magie** (es. Unholy Heat = Gruul), non per terre (Grove of the Burnwillows sta anche nella mono-verde).
- Non pesare RC vs Spotlight con moltiplicatori arbitrari: tenerli separati e confrontarli (a settembre 2026 combaciavano, tranne Dimir e Domain Zoo).
- I matchup sono stabili nel tempo anche attraverso un ban, il metagame no.
