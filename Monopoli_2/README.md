# 🏠 Gestionale Monopoli in Python

Questo progetto implementa una versione **gestionale** del gioco **Monopoli** in Python, con salvataggio dei dati in Excel (`openpyxl`) e gestione di tabellone, proprietà, affitti, tasse, imprevisti e scambi tra giocatori.

## 📋 Funzionalità

- Creazione automatica di un file Excel con:
  - Foglio principale con i giocatori e il loro saldo iniziale
  - Un foglio separato per ciascun giocatore con lo storico delle mosse
- Gestione delle **proprietà**:
  - Acquisto, affitto (anche doppio in caso di possesso del gruppo colore)
  - Costruzione case e hotel
- Gestione **stazioni** e **società**
- Gestione **tasse** e **imprevisti**
- Passaggio dal **Via** con bonus automatico
- Funzione **scambio** per trasferire denaro o proprietà tra giocatori
- Salvataggio e aggiornamento continuo di:
  - File Excel (`monopoli_spese.xlsx`)
  - File JSON della board (`monopoli_board.json`)
  - File JSON degli imprevisti (`imprevisti.json`)

## 📂 Struttura file
```bash
Monopoli_2/
│
├── monopoli_spese.xlsx # File Excel con i dati della partita
├── imprevisti.json # Lista degli imprevisti
├── monopoli_board.json # Dati del tabellone
└── main.py # Codice principale
```
## ⚙️ Requisiti

- Python 3.x
- Librerie Python:
  - `openpyxl`
  - `json`
  - `random`

Per installare le dipendenze principali:
```bash
pip install openpyxl
```
## 🚀 Come usare
1) Assicurati di avere nella cartella indicata:

    - imprevisti.json

    - monopoli_board.json

2) Avvia lo script:

``` bash
python main.py
```
3) Alla prima esecuzione:

    - Inserisci il numero di giocatori e i loro nomi

    - Verrà creato monopoli_spese.xlsx

- A turno i giocatori lanceranno i dadi (o potranno digitare scambio per fare uno scambio).

- Segui le istruzioni mostrate in console per acquistare, pagare affitti, costruire, ecc.

## 🧩 Comandi speciali
Durante il turno:

- `scambio` → avvia la procedura di scambio denaro/proprietà tra giocatori

# 📑 Struttura del file Excel
**Foglio "Giocatori"**: elenco con saldo iniziale

**Foglio del singolo giocatore:**

```nginx
Turno | Casella | ID Casella | Tipo | Colore | Importo | Saldo | Descrizione
```

## 🔮 Miglioramenti futuri (TODO)
- Gestione dell'ipoteca delle proprietà

- Miglioramento interfaccia (possibile versione GUI)

- Statistiche automatiche della partita