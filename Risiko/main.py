import os
from openpyxl import Workbook, load_workbook
import random
import json

territori = r"C:\Users\alessandrini\Documents\coding\games\Risiko\territori.json"
obiettivi = r"C:\Users\alessandrini\Documents\coding\games\Risiko\obiettivi.json"
FOLDER = "Risiko"
os.makedirs(FOLDER, exist_ok=True)
NOME_FILE_EXCEL = "RisiKo.xlsx"
EXCEL_PATH = os.path.join(FOLDER, NOME_FILE_EXCEL)


# ------------------- CARICAMENTO FILE -------------------
def carica_obiettivi():
    try:
        if not os.path.exists(obiettivi):
            print(f"❌ File obiettivi non trovato: {obiettivi}")
            return []
        else:
            with open(obiettivi, 'r', encoding='utf-8') as file_obiettivi:
                return json.load(file_obiettivi)
    except json.JSONDecodeError:
        print("❌ Errore nel file obiettivi.json")
        return []


def carica_territori():
    try:
        if not os.path.exists(territori):
            print(f"❌ File territori non trovato: {territori}")
            return []
        else:
            with open(territori, 'r', encoding='utf-8') as file_territori:
                return json.load(file_territori)
    except json.JSONDecodeError:
        print("❌ Errore nel file territori.json")
        return []


# ------------------- CREAZIONE/VERIFICA FILE -------------------
def verifica_file(lista_giocatori, lista_colori, pedine_iniziali):
    try:
        if os.path.exists(EXCEL_PATH):
            eliminazione = input("attenzione la partita già esiste eliminarla ? (s/n)").lower().strip()
            if eliminazione == 's':
                print("📂 elimino file e creo nuova partita")
                os.remove(EXCEL_PATH)
            else:
                exit("❌ Operazione annullata, esco.")

        wb = Workbook()
        ws = wb.active
        ws.title = "Giocatori"

        for giocatore, colore in zip(lista_giocatori, lista_colori):
            foglio = wb.create_sheet(title=giocatore)
            
            # Intestazione informazioni generali
            foglio["A1"] = "Giocatore"
            foglio["B1"] = giocatore
            foglio["A2"] = "Colore"
            foglio["B2"] = colore
            foglio["A3"] = "Pedine Iniziali"
            foglio["B3"] = pedine_iniziali
            foglio["A5"] = "OBIETTIVO SEGRETO"
            # Lasciamo B5 vuota, verrà riempita dalla funzione assegna_obiettivi

            # Spazio prima dei territori
            foglio["A7"] = "Territori"
            foglio["A8"] = "Nome"
            foglio["B8"] = "Continente"
            foglio["C8"] = "Simbolo"
            foglio["D8"] = "numero Truppe"

        wb.save(EXCEL_PATH)
        print(f"✅ File '{EXCEL_PATH}' creato con i fogli dei giocatori.")
        return wb, ws

    except Exception as e:
        print(f"❌ Errore nel controllo dei file: {e}")
        return None, None


# ------------------- PEDINE INIZIALI -------------------
def pedine_distart(lista_giocatori):
    if len(lista_giocatori) == 3:
        return 35
    elif len(lista_giocatori) == 4:
        return 30
    elif len(lista_giocatori) == 5:
        return 25
    elif len(lista_giocatori) == 6:
        return 20

# ------------------- GIOCATORI -------------------
def aggiungi_giocatori():
    lista_giocatori = []
    while True:
        try:
            n_giocatori = int(input("Inserisci numero giocatori (3-6): "))
            if 3 <= n_giocatori <= 6:
                break
            else:
                print("⚠️ I giocatori devono essere almeno 3 e massimo 6.")
        except ValueError:
            print("❌ Inserisci un numero valido.")

    for i in range(n_giocatori):
        while True:
            nome = input(f"Inserisci nome giocatore {i+1}: ").strip().capitalize()
            if not nome:
                print("⚠️ Inserire un nome valido.")
            elif nome in lista_giocatori:
                print("⚠️ Nome già inserito, scegline un altro.")
            else:
                lista_giocatori.append(nome)
                print(f"✅ Giocatore '{nome}' aggiunto.")
                break

    print(f"\n🎮 Giocatori registrati: {lista_giocatori}")
    return lista_giocatori, n_giocatori


# ------------------- ASSEGNAZIONE COLORI -------------------
def assegna_colore(lista_giocatori):
    lista_colori = []
    for giocatore in lista_giocatori:
        while True:
            colore = input(f"Inserisci colore per {giocatore} : ").strip().lower()
            if colore not in ["giallo", "rosso", "verde", "blu", "viola", "nero"]:
                print("⚠️ Colore non valido")
            elif colore in lista_colori:
                print("⚠️ Colore già scelto da un altro giocatore")
            else:
                lista_colori.append(colore)
                break
    return lista_colori

# ------------------- ASSEGNAZIONE TERRITORI -------------------
def assegna_territori(file_territori, lista_giocatori, wb):
    territori = file_territori.copy()
    random.shuffle(territori)

    # numero di territori per ciascun giocatore
    numero_carte = len(territori) // len(lista_giocatori)

    for giocatore in lista_giocatori:
        ws = wb[giocatore]

        for _ in range(numero_carte):
            territorio = territori.pop()
            ws.append([
                territorio["nome"],
                territorio["continente"],
                territorio["simbolo"]
            ])
    # ✅ Salva Excel aggiornato
    wb.save(EXCEL_PATH)
    print("✅ Territori assegnati ai giocatori, visulaizza file exel")
    return numero_carte

# ------------------- ASSEGNAZIONE OBIETTIVI -------------------
def assegna_obettivi(lista_giocatori, wb, file_obiettivi):
    obiettivi= file_obiettivi.copy()
    random.shuffle(obiettivi)
    for giocatore in lista_giocatori:
        ws = wb[giocatore]
        obiettivo = obiettivi.pop()
        ws["B5"] = obiettivo["descrizione"]  # Obiettivo segreto in B5
    wb.save(EXCEL_PATH)
    print("✅ obiettivi assegnati ai giocatori, visulaizza file exel")

def inserire_truppe(lista_giocatori, wb,pedine_iniziali,numero_carte):
    for giocatore in lista_giocatori:
        ws = wb[giocatore]
        # Leggi i territori dalla colonna B (righe 9-22, dove ci sono i territori)
        for riga in range(9, 9+numero_carte):  # righe dei territori
            territorio = ws[f"A{riga}"].value  # nome del territorio in colonna A
            if territorio:  # controlla che ci sia un territorio
                while True:
                    try:
                        n_truppe = int(input(f"Inserire numero di truppe nel territorio '{territorio}' per {giocatore}: "))
                        if n_truppe < 3 or n_truppe > pedine_iniziali:
                            print("numero truppe errato")
                        else:
                            break
                    except ValueError:
                        print("❌ Inserisci un numero valido.")
                ws[f"D{riga}"] = n_truppe  # scrive il numero di truppe accanto al simbolo
        print(f"✅ Truppe assegnate per {giocatore}")

    wb.save(EXCEL_PATH)
    print("✅ Tutte le truppe sono state salvate nel file Excel.")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    lista_giocatori, n_giocatori = aggiungi_giocatori()
    lista_colori = assegna_colore(lista_giocatori)
    pedine_iniziali = pedine_distart(lista_giocatori)

    file_territori = carica_territori()
    file_obiettivi = carica_obiettivi()
    
    wb, ws = verifica_file(lista_giocatori, lista_colori, pedine_iniziali)
    assegna_obettivi(lista_giocatori, wb, file_obiettivi)
    numero_carte= assegna_territori(file_territori, lista_giocatori, wb)
    inserire_truppe(lista_giocatori, wb,pedine_iniziali,numero_carte)
