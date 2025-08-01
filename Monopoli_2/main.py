import os
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
import random
import json

patrimonio=200
imprevisti_path = r"C:\Users\alessandrini\Documents\coding\data python\monopoli\imprevisti.json"
board_path =r"C:\Users\alessandrini\Documents\coding\data python\monopoli\monopoli_board.json"

folder = "monopoli"
os.makedirs(folder, exist_ok=True)
nome_file = 'monopoli_spese.xlsx'
exel_path = os.path.join(folder, nome_file)


def verifica_file():
    try:
        if os.path.exists(imprevisti_path) and os.path.exists(board_path):
            print("📁 i file esistonno")
            return True
        else:
            print("❌ File inesistenti.")
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
    
lista_giocatori = []
def aggiungi_giocatori():
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
    
def main():
    esiste = verifica_file()
    aggiungi_giocatori()
    if esiste:
        imprevisti = carica_imprevisti()
        board = carica_board()
        wb=Workbook()
        ws=wb.active
        ws.title= "Giocatori"
        ws.append(["Giocatori", "importo"])
        for giocatore in lista_giocatori:
            ws.append([giocatore,patrimonio])
        wb.save(exel_path)








if __name__ == "__main__":
    main()