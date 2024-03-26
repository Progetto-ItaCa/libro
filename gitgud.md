# GITGUD

![YOU DIED](https://i.ytimg.com/vi/-ZGlaAxB7nI/maxresdefault.jpg)


## Cos'è il controllo del versionamento del codice

Persone diverse stanno lavorando a un progetto che presuppone di scrivere del codice. Modifiche fatte in parallelo da persone diverse potrebbero risultare in conflitto se agiscono sulla stessa linea di codice: diciamo che l'utente `A` scrive in `file.txt`:

```
le rose sono rosse
```

Nello stesso momento invece `B` scrive (in una copia che sta sul suo computer)

```
le rose sono blu
```

Chi ha ragione? Come fanno `A` e `B`a mettersi d'accordo su quale delle due versioni del file `file.txt` va usata nel progetto?

Per risolvere questo problema servirebbe una maniera di rappresentare univocamente le varie versioni di un file di testo, tenendo traccia di come esso evolve nel tempo; l'ideale sarebbe rendere possibile *tornare indietro* a una versione precedente del file dopo aver sperimentato qualcosa che si è rivelato fallace, e risolvere quanto più automaticamente possibile conflitti analoghi a quello sopra.

Hence git.

## Cosa è un repo

Un "repo" o *repository* è un apparato che risolve il problema di rappresentare la storia di modifiche successive potenzialmente divergenti ad una base di codice.

L'entità fondamentale in un repo è il *diff*, ovvero le differenze nel codice tra una versione e quella precedente.

Internamente il repo è rappresentato come un grafo diretto aciclico, ed in particolare ai suoi nodi sono associati i diff, oltre ad alcuni metadati.

I metadati includono timestamp, nome utente, ed un hash crittografico calcolato sulla concatenazione di metadati, diff, e hash del nodo genitore.

Questo fa del repo un [Merkle tree](https://it.wikipedia.org/wiki/Albero_di_Merkle).

Sebbene i nodi rappresentino DIFFERENZE tra due versioni del codice, è uso comune trattare i loro hash univoci come se si riferissero allo stato dell'intera base di codice nel momento in cui il nodo è stato creato (ovvero, la somma delle differenze di tutti gli antenati del nodo).

Gli hash sono riferimenti univoci e immutabili a "stati" del codice, ma non sono pratici nell'uso quotidiano.
Questo è il motivo per cui l'albero viene decorato con delle etichette mobili (che prendono il nome di *branch* o *tag* a seconda del modo in cui vengono spostate). Più dettagli di seguito.

## Dove è un repo

Ogni cartella di un computer può essere resa un repo con il comando `git init` (vedi sotto); questa nota introduttiva però non parlerà di nulla che a a che fare con la creazione delle repo, la loro cancellazione etc.

Se si trova sulla propria macchina viene chiamato repository o origin **locale**.

Se si trova sulla macchina di qualche servizio di hosting (e.g. GitHub, BitBucket, GitLab, ...) viene chiamato repository o origin **remoto**.

La differenza non è nella struttura ma nell'utilizzo: i repo remoti sono tipicamente quelli di riferimento utilizzato per la condivisione del codice tra vari utenti. Tutti gli utenti che contribuiscono a un progetto "puntano" al repo remoto e riferiscono ad esso le modifiche, salvo esplicita scelta di non farlo.

Infatti gli utenti possono creare una versione locale del repo remoto, applicare delle modifiche, e "spingerle" poi verso il repo remoto per condividerle (o confrontarle e riconciliare i conflitti) con gli altri.
## Come si usa un repo (da soli, con git)

Il principale servizio che ospita repository remote è [GitHub](https://github.com/). Ne parliamo dopo.

Lo strumento principale con cui si manipolano repository locali è [git](https://git-scm.com/).

Si tratta di una commandline utility, e nel seguito esamineremo i principali comandi. A seconda del proprio OS, ci sono diversi modi di installarlo sulla propria macchina, ma è molto probabile che sia già presente.
### Clonare un repo

Per creare una copia locale di un repository remoto il comando da utilizzare è **`clone`**; il parametro importante da fornire è l'indirizzo del repository remoto: ad esempio, aperto un terminale

```bash
$ git clone git@github.com:Progetto-ItaCa/libro.git

Cloning into 'libro'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 12 (delta 3), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (12/12), 5.78 KiB | 5.78 MiB/s, done.
Resolving deltas: 100% (3/3), done.
```
Il comando crea una cartella col nome del repo, ed all'interno è possibile trovare il codice. Con il comando **`log`** è possibile esaminare una lista delle ultime modifiche:

```bash
$ cd libro
$ git log

commit b943a2bd7eb13e35ba9fa194d2beced4d377a1f1 (HEAD -> main, origin/main, origin/HEAD)
Author: fouche <fosco.loregian@gmail.com>
Date:   Sat Mar 26 11:21:36 2022 +0200

    Rename main.tex to sample.tex
```

Il testo `Rename ...` è un esempio di un *commit*; un commit è una stringa di testo che descrive i cambiamenti che sono stati fatti sul codice dall'`Author`. Ogni commit è identificato da un codice alfanumerico `b943a2...77a1f1` che permette di riferirvisi se necessario.

L'indicazione `HEAD` denota che lo stato dei file nella cartella è quello corrispondente al momento della creazione del commit. In altri termini: `HEAD` indica lo stato storico del repo su cui i file nella cartella sono "sintonizzati".

L'indicazione `main` denota il `branch` di lavoro corrente; si tratta di una etichetta mobile che individua un certo "filone" di sviluppo. Ce ne possono essere molti, grosso modo in funzione di quanti sotto-progetti sono in corso.

Le indicazioni `origin/*` hanno un significato analogo, ma in relazione allo stato del repository remoto.

Entrare nel dettaglio non è fondamentale al momento.

### Modificare un repo

Immaginiamo che il contenuto della repo che abbiamo appena clonato sia il seguente:

```bash
$ ls -l

-rw-r--r-- 1 <user>   33 Mar 27 16:52 README.md
-rw-r--r-- 1 <user>  309 Mar 27 16:52 beauty.py
-rw-r--r-- 1 <user> 4652 Mar 27 16:52 itaca.sty
-rw-r--r-- 1 <user> 1538 Mar 27 16:52 sample.tex
```

`git` può darci delle informazioni sullo stato della repo col comando `status`:

```bash
$ git status

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

```

`On branch main` informa l'utente di quale branch sta abitando.

`Your branch is up to date with 'origin/main'` significa che il repo locale in questo momento è sincronizzato con quello remoto.

`nothing to commit, working tree clean` significa che non ci sono nuove modifiche apportate ai file rispetto a quanto già contenuto nel repo.

Se ora apportiamo dell modifiche ai file (modificando un singolo file, cancellandone uno, creando una cartella...) come possiamo aggiornare lo stato del repository in modo che gli altri utenti che collaborano al progetto vedano queste modifiche?

Innanzitutto, osserviamo che `git status` è sensibile alle modifiche fatte: se vogliamo modificare il file `README.md`

```
# libro
Il grande libro di ItaCa
```

in

```
# libro
Il meraviglioso libro di ItaCa
```

dopo aver fatto questa modifica e salvato il file, `git status` ci avverte che è cambiato qualcosa:

```bash
$ git status

On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")

```

`Changes not staged for commit` suggerisce che ci sono delle modifiche che è possibile mettere in `stage` per effettuare un `commit`. Questo è il primo passo della sequenza di azioni per pubblicare le proprie modifiche.

Lo `stage` è un "palco" su cui è possibile posizionare le modifiche fatte ai file tramire il comando `git add`.

```bash
$ git add README.md
$ git status

On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   README.md

```

`git commit -m <MESSAGGIO>` è il comando con cui si conferma la volontà di aggiungere le modifiche messe in _stage_ al repo annotandole con un `<MESSAGGIO>`:

```bash
$ git commit -m "edit README.md"

[main eeea38c] edit README.md
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git status

On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

`Your branch is ahead of 'origin/main' by 1 commit` ci conferma che il repo locale contiene un commit in più rispetto a quello remoto. Si tratta di quello che abbiamo appena creato.

Questo è il momento di pubblicare le nostre modifiche col comando `git push`:

```bash
$ git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 16 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 297 bytes | 297.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/Progetto-ItaCa/libro.git
   b943a2b..eeea38c  main -> main

$ git status

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
A questo punto se un altro utente clonasse il repo riceverebbe anche la nostra modifica.

Questo conclude il processo con cui il codice che abbiamo modificato è stato reso disponibile agli altri; prima di questo momento, le modifiche sono essenzialmente reversibili. Dopo aver `push`ato il codice, in senso stretto non è più possibile eliminare una loro traccia.

Per i novizi, quest'ultima caratteristica di `git` è allo stesso tempo la soluzione al problema originario, e la causa di una enorme quantità di problemi ausiliari...

Tornando a noi: cosa succede ora se gli utenti *hanno già* una copia locale al momento del nostro push? Tramite `git status` possono vedere che sono "rimasti indietro" rispetto al punto dove gli altri autori hanno portato il codice:

```bash
$ git status

On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

`Your branch is behind 'origin/main' by 1 commit` significa che non hanno il commit che abbiamo appena pushato, e `can be fast-forwarded` li rassicura del fatto che possono riceverlo senza rischi di conflitti con il comando `pull`:

```bash
$ git pull

Updating b943a2b..eeea38c
Fast-forward
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git status

On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Possiamo chiedere a git di mostrare esplicitamente le modifiche applicate dall'ultimo commit col comando `diff`:

```bash
$ git diff HEAD^

diff --git a/README.md b/README.md
index 88c3a71..89cc611 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,2 @@
 # libro
-Il grande libro di ItaCa
+Il meraviglioso libro di ItaCa
```

Possiamo vedere che è stata rimossa la riga che inizia con `-` ed sostituita con la riga che inizia con `+` all'interno del file `README.md`.

### Branching

Un modo più raffinato di agire sul codice consiste nel creare un differente "branch" dentro il quale modificare, creare, cancellare... file diversi. L'idea è che si dice a git di creare un'etichetta `viola` da portarsi dietro in ogni commit futuro.

Diamo il comando

```bash
git checkout -b viola
```
Così facendo, da main si diparte un nuovo "branch":

[![](https://mermaid.ink/img/pako:eNo9zDEOwjAMBdCrVJ57gswgDsDqxSRuExHbVXCQUNW7k6Gw_f_19HeIlhgCrMVvjbYcUKOJFEd9NNKYp3exSmPNHJ_W_d9PBTMIN6GSxsuOOk0InlkYIYyYeKFeHQH1GLRviZyvqbg1CAvVF89A3e3-0QjBW-cfuhRaG8mpji-RBz0z)](https://mermaid.live/edit#pako:eNo9zDEOwjAMBdCrVJ57gswgDsDqxSRuExHbVXCQUNW7k6Gw_f_19HeIlhgCrMVvjbYcUKOJFEd9NNKYp3exSmPNHJ_W_d9PBTMIN6GSxsuOOk0InlkYIYyYeKFeHQH1GLRviZyvqbg1CAvVF89A3e3-0QjBW-cfuhRaG8mpji-RBz0z)

Se ora si fanno dei commit in `viola`:

[![](https://mermaid.ink/img/pako:eNo9zDEOwyAMBdCrIM85AXOrHqCrFxecYBVMRE2lKsrdw5B08v9fT94g1MjgYRF7NFqTRw21FDHUVyMNyX2lZhpr4vCu3f79VNeFCQq3QhLHtw3VOQRLXBjBjxh5pp4NAXUftK-RjO9RrDbwM-UPT0Dd6vOnAby1zhe6CS2Nyqn2A8T7QIY)](https://mermaid.live/edit#pako:eNo9zDEOwyAMBdCrIM85AXOrHqCrFxecYBVMRE2lKsrdw5B08v9fT94g1MjgYRF7NFqTRw21FDHUVyMNyX2lZhpr4vCu3f79VNeFCQq3QhLHtw3VOQRLXBjBjxh5pp4NAXUftK-RjO9RrDbwM-UPT0Dd6vOnAby1zhe6CS2Nyqn2A8T7QIY)

il flusso di lavoro procede come al solito, con l'unica differenza che ora i commit fatti dopo aver creato `viola` sono "taggati" con l'etichetta che abbiamo creato.

Al momento di confrontare il contenuto di `main` con il branch `viola` saranno possibili dei confronti più puntuali perché riguarderanno solo i commit etichettati con `viola`; questo rende più ordinato e chiaro il progresso del progetto (e GitHub ha una interfaccia intuitiva per gestire i conflitti).

[![](https://mermaid.ink/img/pako:eNpFzTEOwzAIQNGrRMw5gedWPUBXFmqT2KqxI4IrVVHuXg9JusHnSWzga2BwMCd7KC3RYfFVJBmWl1LxcfikmqnXyP5dm137oa4utBrr_yCsM58aC4zQi1AK_duGZRgQLLIwgutj4IlaNgQse6dtCWR8D8mqgpsorzwCNavPb_HgTBuf6JZoVpJD7T9Ri00x)](https://mermaid.live/edit#pako:eNpFzTEOwzAIQNGrRMw5gedWPUBXFmqT2KqxI4IrVVHuXg9JusHnSWzga2BwMCd7KC3RYfFVJBmWl1LxcfikmqnXyP5dm137oa4utBrr_yCsM58aC4zQi1AK_duGZRgQLLIwgutj4IlaNgQse6dtCWR8D8mqgpsorzwCNavPb_HgTBuf6JZoVpJD7T9Ri00x)

Mentre noi lavoravamo su `viola` qualcuno ha modificato `main`: il conflitto va risolto! Spesso questo avviene automaticamente, perché `git` sa capire quale modifica precede quale altra. In questo caso, il contenuto di `main` e di `viola` possono essere riunificati (con un commit su `main` che solitamente inizia con `Merge pull request ...`).

`git branch` permette di vedere tutti i branch aperti nella repo.
```bash
$ git branch
* gitgud
  main
```
Quello con la stellina è il branch dove ci troviamo al momento. Per tornare a `main` è sufficiente dire `git checkout main`: così facendo, *tutti gli edit che non sono stati committati vanno persi*! Quindi non fatelo se non lo volete davvero.

Altre operazioni possibili sono la cancellazione di un branch, con `git checkout -d`: leggete [qui](https://www.cloudbees.com/blog/git-delete-branch-how-to-for-both-local-and-remote) se volete, ma non credo dovrete preoccuparvi troppo di questo (io ed altri cancelleremo i branch che non servono più).

## Come si usa un repo (in compagnia, con GitHub)

Quando molte persone contribuiscono ad un unico repo accade naturalmente che ognuno produca una "storia" divergente da quella degli altri.

Supponiamo che un secondo utente abbia modificato lo stesso file `README.md`, in maniera diversa: per la sua copia locale, `README.md` contiene

```
# libro
Il brutto libro di ItaCa
```

Questo è un esempio di *conflitto* tra le versioni dello stesso file.

E' possibile riconciliare le due versioni? Si! E molta dell'utilità di `git` viene dai suoi algoritmi che nella maggior parte delle situazioni permettono di risolvere conflitti senza interventi manuali.

Nonostante questo, ci sono delle regole di igiene che è opportuno rispettare per minimizzare il rischio di conflitti complessi da risolvere ("perdere" irrimediabilmente un frammento di codice usando git è pressoché impossibile, a meno di poche eccezioni; queste eccezioni quasi sempre sono causate dal violare le regole che seguono).

* *Lavora sempre su un branch personale*: sarà buona pratica fissare delle regole generali per i nomi dei branch (qualcosa tipo `<user>/<sezione>-<comment>`, quindi qualcosa tipo `fouche/CHAPTER1-diagrams`, `ivan/APPENDIX-comments`...). Ci penserò, non è urgente, ma potrebbe evitare molte fatiche in futuro.
* *Committa spesso*, privilegiando piccole modifiche, descritte **chiaramente** nei messaggi di commit. Quello che può accadere altrimenti è che il proprio lavoro venga sovrascritto dalle modifiche fatte da altri quando si pullano nella propria copia locale. **Questo è l'unico modo in cui è letteralmente impossibile recuperare il codice che avete perso**. Avete editato una riga? Commitate "missing \colon in chapter1". Corretto un typo? Committate "typos section 3.2". Cambiato una macro? `git commit -m "\category is now mathbf"`. There is no such thing as "too frequent commits"
* *Pusha spesso*: il branch che hai creato è tuo, non ci saranno conflitti col lavoro degli altri, ed il tuo lavoro sarà sempre al sicuro nel repo remoto. Ci preoccuperemo poi di confrontarlo riga per riga con il `main`.
* Il push di un commit è una operazione che si può costringere git a eseguire anche quando si lamenta che questo potrebbe creare problemi ad altri utenti. In progetti di medie/grandi dimensioni *non* bisogna mai forzarlo in dei branch pubblici, che rappresentano un pezzo di storico del progetto che è condiviso tra vari utenti (solitamente i branch hanno nomi esplicativi: `main` è certamente condiviso tra tutti, mentre `fouche/CHAPTER7-yoneda` esiste mentre ci lavoro, e poi viene mergiato in main; sul secondo posso forzare un push, sul primo no, [pena rendere la vita molto dura a tutti gli altri](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)).


Per effettuare le operazioni di riconciliazione del lavoro dei collaboratori è conveniente utilizzare l'interfaccia web di GitHub.
è possibile farlo anche localmente, ma su GH è semplice esaminare differenze, conflitti, e discutere in contesto di eventuali correzioni coi revisori.

GitHub prevede che si crei un account (come lo avete fatto per mille altri siti) con un username che vi identifichi, e a cui solo voi potete accedere; potete creare delle vostre repo, editarle, condividerle con altri, o renderle private (invisibili a chiunque non vi abbia accesso).

Questo è il mio profilo:

![](https://i.imgur.com/oEMHCfs.png)

il vostro avrà un aspetto molto simile (e se accedete al mio, voi vedrete solo le repo pubbliche).


### Cos'è (e come si usa) una pull request

Spesso chi vuole contribuire a un repo non ne ha completo accesso (per esempio per ragioni di sicurezza; oppure progetti molto grandi possono avere dei collaboratori saltuari, che sono perfetti estranei: per questo motivo il proprietario di un repo può voler esaminare i cambiamenti fatti da qualcuno prima di integrarli nel suo progetto).

Se `A` vuole modificare il contenuto di un repo ad accesso ristretto deve prima creare *un altro* repo remoto a cui può accedere e che può modificare senza restrizioni (un "fork" del repo originario), per poi confrontare il fork con quest'ultimo. Questo avviene nel proprio profilo GitHub.

Questa azione si chiama una "pull request": l'utente che ha forkato il repo originario domanda al suo proprietario `B` il permesso di mergiare i contributi dal fork al repo originario, mostrandogli le modifiche che ha fatto (alcuni commit del suo storico).

Questo è un esempio della lista delle PR sulla repo di agda-categories:

![](https://i.imgur.com/wyCnGdm.png)

Ciascuna pull request è il contributo di `A` che chiede di collaborare al progetto passando per il vaglio preliminare di `B` che approva le PR dopo averle esaminate.

L'interazione tipica tra `A` e `B` è una cosa del genere

- `A` fa una PR
- `B` legge cosa contiene (guarda commit per commit in cosa consistono le modifiche fatte da `A`)
- se `B` le ritiene accettabili (e non ci sono conflitti), può decidere di mergiare i commit sottoposti da `A` nella sua repo
- se ci sono conflitti o `B` ritiene opportune delle ulteriori modifiche chiede ad `A` di eseguirle (GitHub permette di commentare in maniera puntuale -riga per riga- il codice dei commit in una PR)
- `A` esegue i cambiamenti chiesti
- ...
- finché a un certo punto (si spera) si converge al momento in cui `B` accetta la PR.

Quando `A` vuole forkare un repo, lo fa da GitHub e gli appare una copia della repo forkata nel proprio profilo; da lì, `A` clona una copia locale e agisce come al solito. In poche parole una PR permette di confrontare due branch di repo remote su cui persone diverse hanno agito e unificare il loro contenuto. Ad `A` quindi serve una copia in remoto del repo di `B`! Questo è ciò a cui serve un fork.

### Qualche considerazione finale

Imparare a usare git è un processo che non finisce mai, e passa per diversi momenti di illuminazione, seguita da frustrazione, seguita da ulteriore illuminazione, seguita... ma (come accade con TeX) il ritorno in termini di qualità del lavoro (inteso come work in progress) e del prodotto finito è ineguagliato da tanti altri metodi più o meno civili di controllo versione. E' impensabile gestire un progetto che abbia piu di due autori, senza controllo versione; git è l'unico modo razionale di farlo, ed è complesso e stratificato perché il processo di creazione del codice da parte di più di una persona è complesso e stratificato.

Degli ottimi modi di imparare a usarlo sono

- zillioni di [video di youtube](https://www.youtube.com/results?search_query=using+git) che promettono di insegnarlo in 15 minuti o meno.
- corsi online relativamente a basso costo, come quelli di [udemy](https://www.udemy.com/course/git-complete/) e udacity.
- gli amici e i colleghi che sanno già usarlo.

---

Questa nota è stata redatta da [me](https://github.com/tetrapharmakon) e da [paolobrasolin](https://github.com/paolobrasolin) (che sa molto più git di me e che potete comodamente pagare in birra appena lo vedete --così come a me).
