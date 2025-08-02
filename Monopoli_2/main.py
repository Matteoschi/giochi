import os
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
import random
import json

# === PERCORSI E COSTANTI ===
PATRIMONIO_INIZIALE = 200
FOLDER = "Monopoli_2"
os.makedirs(FOLDER, exist_ok=True)
NOME_FILE_EXCEL = "monopoli_spese.xlsx"
EXCEL_PATH = os.path.join(FOLDER, NOME_FILE_EXCEL)
IMPREVISTI_PATH = r"C:\Users\alessandrini\Documents\coding\games\Monopoli_2\imprevisti.json"
BOARD_PATH = r"C:\Users\alessandrini\Documents\coding\games\Monopoli_2\monopoli_board.json"


def verifica_file(lista_giocatori):
    try:
        if os.path.exists(IMPREVISTI_PATH) and os.path.exists(BOARD_PATH) and os.path.exists(EXCEL_PATH):
            print("📁 I file esistono!")
            wb = load_workbook(EXCEL_PATH)
            ws = wb.active
            return True, wb , ws
        else:
            print("❌ File mancanti. Creo nuovo file Excel...")
            wb = Workbook()
            ws = wb.active
            ws.title = "Giocatori"
            ws.append(["Giocatore", "Patrimonio"])

            # Aggiungi giocatori al foglio principale
            for giocatore in lista_giocatori:
                ws.append([giocatore, PATRIMONIO_INIZIALE])

            # Crea un foglio per ogni giocatore
            for giocatore in lista_giocatori:
                foglio = wb.create_sheet(title=giocatore)
                foglio.append(["Turno", "Casella", "tipo", "colore", "Importo", "Saldo"])

            wb.save(EXCEL_PATH)
            print(f"✅ File '{NOME_FILE_EXCEL}' creato con i fogli dei giocatori.")
            return False, wb , ws
    except Exception as e:
        print(f"❌ Errore nel controllo dei file: {e}")
        return False, None , None


def carica_imprevisti():
    try:
        with open(IMPREVISTI_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    
def carica_board():
    try:
        with open(BOARD_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("❌ Errore nel file board.")
        return []

def aggiungi_giocatori():
    lista_giocatori = []
    try:
        num_players = int(input("Quanti giocatori? "))
    except ValueError:
        print("❌ Inserisci un numero valido.")
        return aggiungi_giocatori()

    for i in range(num_players):
        while True:
            nome = input(f"Inserisci nome del giocatore {i+1}: ").strip().lower()
            if not nome:
                print("❌ Nome non valido.")
            elif nome in lista_giocatori:
                print("⚠️ Giocatore già inserito.")
            else:
                lista_giocatori.append(nome)
                print("✅ Giocatore aggiunto.")
                break
    print(f"🎮 Giocatori registrati: {lista_giocatori}")
    return lista_giocatori

def apri_json():
    with open(BOARD_PATH, 'r' , "utf-8") as file:
        return json.load(file)
    

def lancia_dadi(giocatore, posizione_corrente, board , wb):
    try:
        dado = int(input(f"{giocatore}, lancia i dadi (2-12): "))
        if not 2 <= dado <= 12:
            print("❌ Inserisci un numero tra 2 e 12.")
            return lancia_dadi(giocatore, posizione_corrente, board)
    except ValueError:
        print("❌ Inserisci un numero valido.")
        return lancia_dadi(giocatore, posizione_corrente, board)

    nuova_posizione = (posizione_corrente + dado) % len(board)
    
    casella = next((p for p in board if p["posizione"] == nuova_posizione), None)

    if casella:
        nome = casella['nome']
        tipo = casella['tipo']
        colore = casella['colore']
        print(f"{giocatore} è atterrato su '{nome}', tipo: {tipo}, colore: {colore}")

        # 📄 Scrittura nel foglio Excel del giocatore
        if giocatore in wb.sheetnames:
            foglio = wb[giocatore]
            turno = foglio.max_row  # Assumiamo che ogni riga sia un turno (prima riga è intestazione)
            descrizione = f"{tipo}, colore: {colore}" if colore else None
            importo = 0  # Puoi cambiarlo con la logica economica futura
            saldo = PATRIMONIO_INIZIALE  # Per ora saldo fisso
            foglio.append([turno, nome, tipo, colore , importo, saldo])
            wb.save(EXCEL_PATH)



def main():

    if not os.path.exists(EXCEL_PATH):
        lista_giocatori = aggiungi_giocatori()
    else:
        lista_giocatori = None  

    file_esistente, wb, ws = verifica_file(lista_giocatori)


    if file_esistente:
        lista_giocatori = [
            row[0] for row in ws.iter_rows(min_row=2, max_col=1, values_only=True) if row[0]
        ]
        print(f"👥 Giocatori caricati dal file: {lista_giocatori}")

    # Carica dati di gioco
    imprevisti = carica_imprevisti()
    board = carica_board()

    # Posizioni iniziali
    posizioni = {g: 0 for g in lista_giocatori}

    # Turno iniziale
    for giocatore in lista_giocatori:
        posizioni[giocatore] = lancia_dadi(giocatore, posizioni[giocatore], board , wb)









if __name__ == "__main__":
    main()