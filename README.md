# Libro di ItaCa

Il meraviglioso libro di ItaCa -- Teoria delle categorie.

## Struttura del progetto

```
main.tex                  documento principale
itaca.dtx / itaca.sty     pacchetto condiviso (macro, ambienti, opzioni)
quiver.sty                wrapper per diagrammi commutativi (q.uiver.app)
gitcommit.tex             hash del commit (generato da make hash)
cap/
  00/intro.tex            introduzione
  01/categorie.tex        cap. 1 -- categorie (+ cap/01/sec/*.tex)
  02/limiti.tex           cap. 2 -- limiti e colimiti (+ cap/02/sec/*.tex)
  03-aggiunti.tex         cap. 3 -- funtori aggiunti
  04-yoneda.tex           cap. 4 -- lemma di Yoneda
  05-YAL.tex              cap. 5 -- Yet Another Limit
  06-monadi.tex           cap. 6 -- monadi
  07-fattorizzazione.tex  cap. 7 -- sistemi di fattorizzazione
  08-monoidali-…          cap. 8 -- categorie monoidali, interne, arricchite
  09-nervi-…              cap. 9 -- nervi e realizzazioni
  extra_enricoV_…         cap. 10 -- categorie algebriche
  AA-appendice.tex        appendice
  AX-complementi.tex      complementi
  AB-soluzioni.tex        soluzioni degli esercizi
```

## Prerequisiti

Il progetto usa Nix per gestire le dipendenze (TeX Live 2023).

```bash
nix develop          # entra nella shell con tutto il necessario
```

## Compilazione

### Uso quotidiano (veloce)

Il ciclo di lavoro consigliato per editare un capitolo:

```bash
make fmt                              # una tantum (~2s): precompila il preambolo
make fast CH=cap/07-fattorizzazione   # compila un solo capitolo (~1s)
make fast CH=cap/01/categorie         # capitolo grande (~17s)
make fast                             # libro intero (~17s)
```

`make fmt` va rieseguito solo quando cambiano il preambolo di `main.tex`
o `itaca.sty`.

### Alternative (piu lente, ma con latexmk)

Questi target usano latexmk (gestione automatica dei passaggi multipli,
bibtex, makeindex, ecc.):

```bash
make dev                              # libro intero, opzioni fast (~41s)
make chap CH=cap/07-fattorizzazione   # un solo capitolo (~7s)
make watch-dev                        # come dev, ricompila al salvataggio
make watch-chap CH=cap/01/categorie   # come chap, ricompila al salvataggio
```

### Build completa (CI)

Produce il PDF definitivo con indice, bibliografia, todonotes, showkeys:

```bash
make main.pdf     # build completa (~65s, 3 passaggi + bibtex)
make book         # come sopra, con touch preventivo dei .aux
```

### Documentazione del pacchetto

```bash
make itaca.pdf    # genera la documentazione di itaca.dtx
```

## Opzioni del pacchetto `itaca`

Il pacchetto `itaca.sty` (generato da `itaca.dtx` via `tex itaca.ins`)
supporta queste opzioni:

| Opzione          | Effetto                                       |
|------------------|-----------------------------------------------|
| `fast`           | implica `noshowkeys`, `notodos`, `nocjk`      |
| `showkeys`       | mostra le label (default: on)                 |
| `noshowkeys`     | nasconde le label                             |
| `todos`          | attiva todonotes (default: on)                |
| `notodos`        | disattiva todonotes                           |
| `cjk`            | carica CJK per lo yoneda in hiragana (default: on) |
| `nocjk`          | non carica CJK, usa fallback latino           |
| `externalize`    | attiva la cache TikZ (richiede `-shell-escape`) |
| `noexternalize`  | disattiva la cache TikZ (default)             |

## Comandi utili

```bash
make hash         # aggiorna gitcommit.tex con l'hash corrente
make view         # apre main.pdf con evince
make pretty       # formatta i .tex con beautifier.py
make clean        # rimuove tutti i file generati
make clean-cache  # rimuove la cache dei diagrammi TikZ
```

## Cache dei diagrammi TikZ (opzionale)

Il libro contiene ~163 diagrammi TikZ/tikz-cd e ~171 diagrammi xy-pic.
Per evitare di ricompilarli ogni volta, si puo costruire una cache:

```bash
make cache        # costruisce la cache (~15 min la prima volta)
make dev ITACA_DEV_OPTS=fast,externalize   # usa la cache
```

La cache va in `tikz-cache/` (nel `.gitignore`). Dopo modifiche ai
diagrammi, rifare `make cache`. Per svuotarla: `make clean-cache`.

## Note per chi contribuisce

- Modificare `itaca.dtx` (non `itaca.sty` direttamente); rigenerare con
  `tex itaca.ins` o `make itaca.sty`.
- I capitoli 1 e 2 sono suddivisi in sezioni dentro `cap/01/sec/` e
  `cap/02/sec/`; gli altri sono file singoli.
- Per aggiungere un capitolo, inserirlo sia in `\include{...}` che nella
  lista `\includeonly{...}` dentro `main.tex`.
