# 🏠 Gestionale Monopoli in Python

Questo progetto è una **versione gestionale** di **Monopoli** realizzata interamente in Python.  
Non si tratta di un gioco grafico, ma di un **gestore di partita** che tiene traccia di tutte le azioni, movimenti, acquisti, affitti e scambi, salvando automaticamente i dati su un file Excel.

È pensato per **giocare a Monopoli fisicamente**, mentre il programma si occupa di aggiornare in tempo reale saldi, proprietà, costruzioni, tasse e imprevisti.

---

## 📜 Caratteristiche principali

- **Creazione automatica dei dati di gioco**
  - File Excel (`monopoli_spese.xlsx`) con foglio "Giocatori" e un foglio per ogni giocatore
  - Inizializzazione del saldo per ciascun giocatore (patrimonio iniziale di default: **10000€**)
- **Gestione completa delle caselle del tabellone**
  - Proprietà normali: acquisto, affitto, costruzioni (case e hotel)
  - Stazioni: affitto variabile in base al numero posseduto
  - Società: affitto calcolato in base al lancio del dado e numero possedute
  - Caselle speciali: "Via", tasse, imprevisti
- **Sistema di affitti avanzato**
  - Affitto raddoppiato se si possiede l’intero gruppo di colore
  - Calcolo automatico affitti con case/hotel
- **Sistema di costruzione**
  - Possibilità di acquistare da 1 a 4 case o un hotel (solo se già presenti 4 case)
- **Gestione delle transazioni**
  - Pagamento tasse
  - Pagamento affitti
  - Bonus per passaggio dal Via (+200€)
- **Funzione di scambio tra giocatori**
  - Scambio di denaro
  - Scambio di proprietà con eventuale conguaglio in denaro
- **Salvataggio automatico**
  - Ogni operazione aggiorna sia il file Excel che i file JSON della board e degli imprevisti

---

## 📂 Struttura del progetto
```bash
Monopoli_2/
│
├── monopoli_spese.xlsx # File Excel con dati giocatori e cronologia mosse
├── imprevisti.json # Elenco degli imprevisti (premi/penalità)
├── monopoli_board.json # Dati completi del tabellone
└── main.py # Script Python principale
```
---

## 📑 Struttura del file Excel

- **Foglio "Giocatori"**
  - Contiene nomi e saldi iniziali dei partecipanti
- **Foglio di ciascun giocatore**
Turno | Casella | ID Casella | Tipo | Colore | Importo | Saldo | Descrizione

markdown
Copia
Modifica
- **Turno**: numero progressivo del turno per quel giocatore
- **Casella**: nome della casella in cui si è atterrati
- **ID Casella**: indice della casella nel tabellone
- **Tipo**: proprietà, stazione, società, tassa, imprevisto...
- **Colore**: colore della proprietà (se applicabile)
- **Importo**: importo positivo (entrata) o negativo (uscita)
- **Saldo**: saldo attuale del giocatore
- **Descrizione**: spiegazione dell’azione

---

## ⚙️ Requisiti

- **Python 3.x**
- Librerie:
- `openpyxl` → per leggere/scrivere file Excel
- `json` → per leggere/scrivere la board e gli imprevisti
- `random` → per pescare imprevisti casuali

Installazione librerie necessarie:
```bash
pip install openpyxl
```

## 🚀 Come avviare una partita
1) Prepara i file JSON

- imprevisti.json deve contenere una lista di eventi con relativo premio/penalità.

- monopoli_board.json deve contenere le caselle del tabellone, con:

    - Nome

    - Posizione

    - Tipo (proprietà, stazione, società, tassa, imprevisto, speciale)

    - Prezzo, affitto e dettagli costruzioni (se applicabile)

2) Avvia lo script

```bash

python main.py
```

3) Se è la prima partita

- Il programma chiederà il numero di giocatori e i loro nomi

- Verrà creato monopoli_spese.xlsx con i dati iniziali

4) Svolgimento del gioco

- Ad ogni turno, il giocatore inserisce il risultato del lancio dei dadi

- Il programma calcola automaticamente:

    - Spostamento sul tabellone

    - Eventuali acquisti/affitti

    - Costruzioni possibili

    -  Bonus/malus da imprevisti e tasse

- In alternativa, il giocatore può digitare scambio per avviare uno scambio

## 🎮 Comandi principali in partita
- Numero (2-12) → indica il risultato del lancio dei dadi

- scambio → avvia la procedura di scambio

- Modalità soldi: trasferisce denaro tra due giocatori

- Modalità proprietà: scambia proprietà con eventuale conguaglio

## 🔍 Esempio di turno
```sql
giocatore1, lancia i dadi (2-12) oppure digita 'scambio' per scambiare: 8
🎲 giocatore1 ha tirato 8 e si sposta da Vicolo Corto a Stazione Nord | tipo: stazione | colore: NA | proprietario: None
🏠 Vuoi acquistare Stazione Nord per 200€? (s/n): s
✅ Hai acquistato Stazione Nord per 200€.
```
## 📌 Note importanti
- Backup: il file monopoli_spese.xlsx viene aggiornato continuamente, ma si consiglia di fare copie di sicurezza se la partita è lunga.

- Case e hotel: il costo per costruire viene letto direttamente dal file monopoli_board.json.

- Affitti variabili: il calcolo per proprietà, stazioni e società è automatico e basato sullo stato attuale della board.

## 🔮 Possibili miglioramenti futuri
 - Gestione ipoteca delle proprietà

 - Miglioramento messaggi in console

 - Aggiunta di statistiche grafiche dei giocatori

 - Interfaccia grafica (GUI)

 - Log automatico della partita in formato PDF

## 👨‍💻 Autore
Progetto sviluppato in Python come gestionale per partite di Monopoli reali, con salvataggio automatico dei dati e calcolo degli eventi di gioco.