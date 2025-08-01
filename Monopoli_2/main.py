import os
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
import random
import json

patrimonio=200
imprevisti_path = r"C:\Users\alessandrini\Documents\coding\games\Monopoli_2\imprevisti.json"
board_path =r"C:\Users\alessandrini\Documents\coding\games\Monopoli_2\monopoli_board.json"

folder = "Monopoli_2"
os.makedirs(folder, exist_ok=True)
nome_file = 'monopoli_spese.xlsx'
exel_path = os.path.join(folder, nome_file)

def verifica_file():
    try:
        if os.path.exists(imprevisti_path) and os.path.exists(board_path) and os.path.exists(exel_path):
            print("📁 i file esistonno !")
            return True
        else:
            print("❌ File inesistenti.")

            wb = Workbook()
            ws=wb.sheetnames["giocatori"]
            ws = wb.active
            ws.title = "Giocatori"
            ws.append(["Giocatori", "importo"])

            return False
    except Exception as e:
        print(f"❌ Errore nel controllo dei file: {e}")
        return False

def carica_imprevisti():
    try:
        with open(imprevisti_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    
def carica_board():
    try:
        with open(board_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    

def aggiungi_giocatori():
    lista_giocatori = []
    try:
        num_players = int(input("quanti giocatori ? "))
    except ValueError:
        print("❌ inserisci numero valido")
        return aggiungi_giocatori()
    for i in range(num_players):
        while True:
            giocatore = input(f"inserisci numero giocatore {i+1}: ").lower().strip()
            if giocatore:
                if giocatore in lista_giocatori:
                    print("⚠️ Giocatore già esiste")
                    continue
                print("✅ Player added.")
                lista_giocatori.append(giocatore)
                break
            else:
                print("❌ Invalid name. Try again.")
    print(f"Registered players: {lista_giocatori}")
    return lista_giocatori

def apri_json():
    with open(board_path, 'r' , "utf-8") as file:
        return json.load(file)
    

def lancia_dadi(board):
    posizione_iniziale=0
    numero_dati = int(input("inserisci numero dadi :"))
    if numero_dati >12:
        print("❌ Non puoi fare piu di 12 con 2 dadi ")
        return lancia_dadi(board)
    
    for posto in board:
        if posto["posizione"] == numero_dati:
            print(f"giocatore, atterrato nella casella {posto['nome']} , descrizione : {posto['tipo']} , colore {posto['colore']}")



def main():
    esiste= verifica_file()
    if not esiste:
        lista_giocatori = aggiungi_giocatori()
    imprevisti = carica_imprevisti()
    board = carica_board()

    wb = load_workbook(exel_path)
    ws = wb["Giocatori"]
    lista_giocatori = [row[0] for row in ws.iter_rows(min_row=2, max_col=1, values_only=True) if row[0]]

    lancia_dadi(board)








if __name__ == "__main__":
    main()