# Analisi metagame Modern: riassunto della chat

Fonte: chat claude.ai "Analisi dati ultimi challenge magiconline" (fine agosto → 28 settembre 2026, 172 messaggi).
Link: https://claude.ai/chat/9a201de3-7a09-4b0a-ba02-666c0b8d27ad

Questo file raccoglie le conclusioni, i numeri chiave, le decisioni prese e le lezioni di metodo. I dati completi stanno in `dati/`, il metodo di estrazione in `metodo-estrazione-melee.md` e la simulazione in `../simulazioni/`.

---

## 0. Decisioni di inizio ottobre (dopo la guida aggiornata di Ross)

- **Lista per Ghent: la 75 attuale di Ross** (`dati/lista_ross_attuale.md`). I 3 Fleshraker hanno una ragione di matchup (specchio, Esper Blink, Goryo's, punire la land destruction) che il goldfish non vede: la config SWS resta un test, non la scelta di default.
- **Side di Paolo da allineare:** −1 Sire, −1 Ghost Quarter, +1 Nature's Claim, +1 Thief, +1 Warping Wail, +1 Six (i 2 slot mancanti più due cambi). Il Ghost Quarter che avevo proposto per lo specchio non ha supporto nel piano di Ross.

## 1. Stato attuale (28/09/2026)

- **Evento target: RC di Ghent** (paper), previsto a ottobre 2026.
- **Mazzo scelto: Mono-Green Broodscale.** Paolo sta giocando la **build Lab** (3 Ugin's Labyrinth). L'alternativa è la build Halfling, e la scelta tra le due è ancora aperta.
- **Ultimo test in corso:** aggiungere *Something Worth Saving* (SWS, dal set Reality Fracture: in pratica un Malevolent Rumble istantaneo che guadagna 1 vita invece di creare lo Spawn). La simulazione consiglia la **config D: −1 Devourer of Destiny, −1 Glaring Fleshraker, +2 SWS, tenere 4 Emrakul** (vedi §6).
- **Cose da fare**
  - Giocare la config D per circa 20 partite, contando quante volte Emrakul resta in mano con meno di 4 tipi nel cimitero.
  - Tenere il conto delle sconfitte dovute al mana e di quelle dovute al gioco, per decidere tra Lab e Halfling.
  - Priorità di testing: Devoted Druid (il matchup peggiore), specchio, Prowess.
  - Rigenerare la matrice stampando le "partite decise" (bug dei pareggi, §7).
  - Rifare il test mono-verde contro Gruul classificando per **magie** rosse e non per terre (Grove of the Burnwillows falsava il risultato). Il test su Labyrinth nel day 2 non è mai stato chiuso.
  - Classificare dalle carte le liste senza nome.

## 2. Profilo giocatore (dalla chat)

- Ha giocato soprattutto mazzi combo: Amulet (quello su cui ha più ore), Azorius Emry/Loki, Goryo's, Storm, Devoted, Affinity. Adora Rhinos, che però non esiste nel meta.
- Prima di Broodscale giocava **Azorius Oswald/Emry Cam** ("Grinding Emry": 54% su 233 partite nella coda dei mazzi meno giocati).
- Eloproject 1460. Amici forti: **Sascha Luescher** (limited top mondiale), **Luca Magni**. Team: Reto, Lorenzo "Snoopy", Grigor.
- In Standard gioca Jund Sacrifice su Arena (60% di winrate a Gold) e si diverte di più.
- Aree da migliorare secondo lui: sequencing, giocare attorno alle carte, impostare le linee, visione d'insieme.
- Gioca meglio parlando ad alta voce. Consiglio: online farlo sempre; al tavolo usare domande fisse ("cosa può fare con il mana aperto?", "dove voglio essere tra due turni?", "vado per il combo perché è la finestra giusta o perché ce l'ho in mano?") e subvocalizzare.
- Anti-tilt: dopo ogni partita una riga con cosa ha deciso bene, cosa male e cosa era fuori dal suo controllo.
- Tema ricorrente: cambiare mazzo spesso rende meno che fare tante partite sullo stesso mazzo. Esempio: MeninoNey con Living End fa il 62,5%, gli altri 16 piloti con lo stesso mazzo il 18,75%.

## 3. Cronologia delle decisioni (e perché sono cambiate)

1. **MTGO, 4 Challenge (128 slot):** proposto Izzet Prowess, poi Jeskai Energy. Campioni troppo piccoli.
2. **MTGO, 26 eventi (832 slot, 13-26/08):** Dimir Midrange (44% di conversione in top 8) o Jeskai Energy (47%). Il Living End di MeninoNey è un effetto pilota.
3. **Combo senza Goryo's al 21,7% di conversione** → Goryo's o Izzet Steel-Cutter (che in realtà è Emry). Amulet: 0 top 8 su 9 liste.
4. **Paper (Brisbane, Baltimore, matrice mtgdecks):** paper e MTGO divergono (Broodscale 0,7% su MTGO, 11,5% a Baltimore). "Forse porto Goryo's" (stabile tra Dallas e Baltimore).
5. **Dati melee (13.414 partite):** Goryo's scende al 47% all'RC, Broodscale 55% su 1.669 partite → **Broodscale**.
6. **Solo day 2:** Broodscale al 50%, uguale a Goryo's. Ma la conversione al day 2 è Broodscale 35% contro Goryo's 18% (media 24%) → Broodscale resta davanti.
7. **Hangzhou:** mono-verde 56% contro Gruul 44-49% su due continenti → **mono-verde confermata**.

## 4. Numeri chiave

### MTGO (26 Challenge, 832 slot, 13-26/08/2026)
- Consign to Memory satura intorno al 55% dei mazzi, senza trend.
- Conversione in top 8 (baseline 25%):

| Mazzo | Conversione |
|---|---|
| Jeskai Energy | 47,4% (9/19, 0 vittorie) |
| Dimir Mid | 44% |
| Living End | 33,3% (18,75% senza MeninoNey) |
| Esper Blink | 32,1% |
| Goryo's | 30,4% (24/79) |
| Izzet Prowess | 29,8% |
| Eldrazi | 23,4% |
| Affinity | 18,9% |
| Boros Energy | 18,2% |
| Ruby Storm | 17,6% |

### Metagame paper
- **Baltimore RC, day 1 (1.495 giocatori):** Mono-Green Broodscale 11,5%, Izzet Prowess 11,0%, Goryo's 8,4%, Esper Blink 7,7%, Affinity 5,6%, Dimir 4,5%, Devoted 3,8%, Boros Energy 3,4%, Other 26,7%.
- **Dallas → Baltimore in una settimana:** Broodscale da 6,3% a 11,5%, Other da 32,9% a 26,7%. Il campo converge.
- **Baltimore, top 75 (indice di conversione):** Affinity 1,90, Broodscale 1,86, Living End 1,82, Goryo's 1,27, Esper Blink 1,04, Prowess 0,85. Ha vinto Devoted, con Curtis Lam 13-0.

### Classifica melee (RC Baltimore, 15 round)

| Mazzo | WR | Partite |
|---|---|---|
| Boros Ponza | 56% | 293 |
| Broodscale | 55% | 1.669 |
| Affinity | 54% | 679 |
| Tron | 52% | 258 |
| Esper Blink | 51% | 872 |
| Goryo's | 47% | 877 |

Tutti i campioni (RC + 2 Spotlight): Izzet Prowess 47% su oltre 2.200 partite.

### Broodscale: riga matchup (da usare per la preparazione)

| Avversario | % campo Baltimore | WR campione pieno | WR solo day 2 |
|---|---|---|---|
| Specchio | 11,5 | 50% (356) | 50% (86) |
| Izzet Prowess | 11,0 | 54% (272) | 47% (55) |
| Esper Goryo's | 8,4 | 55% (218) | 52% (30) |
| Esper Blink | 7,7 | 53% (222) | 55% (59) |
| Izzet Affinity | 5,6 | 61% (168) | 52% (33) |
| Dimir Midrange | 4,5 | 66% (116) | 60% (15) |
| **Devoted Druid** | 3,8 | **43% (109)** | 42% (27) |
| Boros Energy | 3,4 | 46% (113) | **36% (29)** |
| MG Eldrazi | 3,3 | 52% (91) | 60% (25) |
| Domain Zoo | 2,7 | 46% (55) | 44% (9) |
| Boros LD (Ponza) | 2,5 | 62% (71) | 62% (14) |
| Ruby Storm | 2,5 | 63% (68) | 60% (16) |
| Neoform | 2,3 | 51% (49) | 50% (6) |
| Living End | 2,2 | 65% (67) | 58% (12) |
| Jeskai Control | 1,7 | 55% (55) | 33% (9) |
| Eldrazi Tron | 1,2 | 73% (50) | 71% (9) |
| Amulet Titan | 1,2 | 49% (51) | 30% (10) |

- A Hangzhou Broodscale contro Prowess fa l'11% su 19 partite. È un campione troppo piccolo: segnalato, non usato.
- Pesando la riga su un campo ipotetico di Ghent (specchio al 17%, Devoted al 7%) il WR atteso è circa 53%.

### Goryo's, per confronto (4 fonti che convergono)
- Contro Prowess 56% (212), contro Broodscale 45% (218), contro Esper Blink 36% (150), contro Affinity 40% (124).
- Al Pro Tour: 51% su 266 partite. Il pilota incide poco sul risultato di questo mazzo.

## 5. Costruzione di Broodscale

- **Mono-verde meglio del Gruul:** 56% contro 49% negli USA, 56% contro 44% a Hangzhou. Il confine è "niente **magie** rosse" (Unholy Heat), e Grove of the Burnwillows va bene. Attenzione: in parte il dato misura anche quanto sono aggiornate le liste, perché Merriam stesso ha cambiato idea sul Gruul in poche settimane.
- **Lista di consenso (Baltimore, 47 liste mono-verdi con almeno 8 vittorie):** vedi `dati/liste_consenso_baltimore.md`.
- **Lista di Paolo (build Halfling della guida):**
  - Main: 3 Delighted Halfling, 4 Basking Broodscale, 1 Glaring Fleshraker, 4 Sowing Mycospawn, 3 Emrakul, 4 Ancient Stirrings, 4 Malevolent Rumble, 4 Kozilek's Command, 2 Dismember, 3 Blade of the Bloodchief, 2 Vexing Bauble, 1 Haywire Mite, 1 Soul-Guide Lantern, 1 Springleaf Drum
  - Terre: 4 Urza's Saga, 4 Eldrazi Temple, 4 Grove of the Burnwillows, 2 Boseiju, 1 Cavern of Souls, 1 The Mycosynth Gardens, 1 Yavimaya, 6 Forest
  - Side: 1 Dismember, 1 Vexing Bauble, 1 Grafdigger's Cage, 1 Pithing Needle, 1 Soulless Jailer, 2 Thief of Existence, 2 Six, 1 Sire of Seven Deaths, 2 Warping Wail, 2 Nature's Claim, 1 Gemstone Caverns
- **Lista attuale di Ross (fine settembre):** vedi `dati/lista_ross_attuale.md`.
- **Lab build di Ross Merriam in stream (14/09):** 3 Lab, 4 Emrakul / 3 Devourer, 2 Dismember main, 1 Vexing Bauble main, 1 Shifting Woodland, 1 Gemstone main, 6 Forest, 1 Talisman, 0 Fleshraker. In side ha Ghost Quarter (per lo specchio contro Labyrinth) e Warping Wail. È convergente al consenso di Baltimore su 7 punti su 7.
- **Scarti per carta che reggono al filtro day 2:** solo mono-verde contro splash. Ugin's Labyrinth, Devourer e Yavimaya a +8/+10 sul campione pieno spariscono in day 2: erano marcatori di liste aggiornate. Pithing Needle in main: debole.
- **Sideboard guide:** il PDF `broodscale-guida-definitiva.pdf` (13 pagine, 21 matchup con ESCE / ENTRA / IN DRAW, tutte le colonne verificate da Paolo) è nella chat. È derivato dalla griglia di Ross Merriam rielaborata da Paolo, quindi non è riprodotto qui. Lettura della griglia: l'asterisco indica lo swap solo on the draw (tipicamente Cavern of Souls o una terra → Gemstone Caverns). Contro Affinity e Boros LD Gemstone Caverns entra sempre, anche on the play.
- **Esper Blink (risolto, guida di Ross di ottobre):** resta 3 contro 3; Ross vorrebbe togliere anche il quarto Broodscale e fa entrare Sire come quarta carta se si vuole.

### Principi di gioco emersi
- **False tempo** (Merriam): nei matchup interattivi apri con mana veloce e interazione e usa la combo come minaccia, così l'avversario deve tenere mana aperto.
- **Da una mano ridotta** vale il contrario: scegli la linea che vince se l'avversario non ha la risposta.
- **Contro Esper Blink** tutto ruota attorno a Solitude.
  - Cerca Vexing Bauble con la Saga: spegne l'evoke di Solitude e il rebound di Ephemerate.
  - Senza Bauble, esaurisci le loro Solitude fermando Phelia e Overlord.
  - Gioca fair e non esporre due creature chiave a un solo Ephemerate.
  - Tieni gli Eldrazi Temple in mano contro Knight of the White Orchid e Clarion Conqueror. Clarion spegne anche il sacrificio degli Spawn e l'equip della Blade.
  - Six è meglio di Sire contro i midrange: costa 3 e ha reach. Sire è la carta anti-aggro.
- **Contro Boros Energy** il pericolo vero è Ajani + Goblin Bombardment, per cui serve Pithing Needle. Dismember su Guide of Souls è di solito corretto.
- **Specchio:** Kozilek's Command è la carta più importante. Una Blade in difesa su una Broodscale rende difficile la combo avversaria. Ghost Quarter, preso con Mycospawn kickato, toglie le terre chiave dell'avversario.
- **Vexing Bauble:** la condizione è "nessun mana speso". Contrasta Mishra's Bauble, Mutagenic Growth pagata con vita, l'evoke e il rebound. Non contrasta il flashback pagato con mana.

## 6. Simulazione SWS (28/09)

Script in `../simulazioni/sim_broodscale.py` (goldfish Monte Carlo, `python sim_broodscale.py 100000`).

Risultati on the play, 100.000 partite:

| Metrica | A attuale | B (−Dev −Emr −Flesh +3 SWS) | C (−Emr −Flesh +2 SWS) | **D (−Dev −Flesh +2 SWS)** |
|---|---|---|---|---|
| Emrakul lanciata entro il T6 | 54,5% | 58,0% | 55,2% | **62,7%** |
| Emrakul in mano non lanciata al T6 | 24,0% | 15,0% | 16,5% | 18,7% |
| Due Emrakul in mano insieme | 15,0% | 7,9% | 8,3% | 13,9% |
| Almeno 5 tipi nel cimitero al T5 | 43% | 59% | 54% | 54% |
| Lab con imprint | 57,7% | 47,1% | 56,5% | 50,9% |

- SWS risolve la causa del problema (il cimitero), quindi non serve tagliare anche un'Emrakul.
- Il costo è l'imprint del Lab.
- Per un terzo SWS si può tagliare il secondo Dismember o la Vexing Bauble main, ma è una decisione da prendere in base al metagame.
- Limiti del modello: nessun avversario, SWS giocata a velocità stregoneria, reveal di Devourer non modellato.

## 7. Lezioni di metodo (e errori già fatti: non ripeterli)

- **Celle piccole:** le raccomandazioni su 12-30 partite sono state smentite ogni volta che il campione è cresciuto. Serve un numero di partite per ogni conclusione.
- **Effetto pilota:** un singolo giocatore può gonfiare un archetipo (MeninoNey). Va sempre controllato.
- **Confondimento carta/pilota:** Containment Priest faceva +14 contro Broodscale ma non entra in quel matchup. Era un marcatore di piloti preparati, e l'ha scoperto Paolo. Test: la carta può influenzare fisicamente quel matchup?
- **Robusti su due test indipendenti:** White Orchid Phantom in Esper Blink è negativa (38% contro 51% contro Broodscale, 42% contro 70% nello specchio). Consiglio agli amici con Esper Blink: toglierla. Consign to Memory in main è negativa contro Broodscale.
- **Classifiche intermedie di un torneo:** sono rumorose (Esper Blink sembrava a 2,84 al round 6 e ha chiuso a 1,04).
- **Tabelloni dei primi classificati:** sono un bias di selezione ("Broodscale batte Goryo's 2 volte su 3" era falso).
- **Pareggi:** se il WR è calcolato senza pareggi, anche il denominatore stampato deve escluderli.
- **Griglie da immagine:** Claude le ha lette male 4 volte (celle attribuite alla colonna adiacente). **Fai dettare la griglia a Paolo** invece di interpretare l'immagine.
- **Regole:** prima di correggere Paolo su una regola, verifica l'Oracle text. Su Vexing Bauble aveva ragione lui.
- **Portable Hole** prende solo MV ≤ 1: non Clarion Conqueror.
- **Contenuti a pagamento** (Patreon di Ross Merriam): non riformattarli né riassumerli in documenti autonomi. Si possono usare come contesto quando Paolo li cita.
- **REL Competitive:** gli appunti preparati si consultano solo tra un match e l'altro. Da verificare con il judge a Ghent.

## 8. Altri file prodotti in chat (li ha Paolo, non sono qui)
- `modern-matchup-matrix.pdf` / `modern-ghent-dossier.pdf`: heatmap e liste di consenso di 13 archetipi.
- `modern-day2-analysis.pdf`: matrice del day 2 e verdetti sulle scelte di costruzione.
- `broodscale-guida-definitiva.pdf`: deck guide e sideboard guide.
