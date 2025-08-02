import os
from openpyxl import Workbook, load_workbook
from datetime import datetime, timedelta
import random
import json

# === PERCORSI E COSTANTI ===
PATRIMONIO_INIZIALE = 1000
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
                foglio.append(["Turno", "Casella", "tipo", "colore", "Importo", "Saldo" , "descrizione"])

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
    with open(BOARD_PATH, 'r' , encoding="utf-8") as file:
        return json.load(file)
    

def lancia_dadi(giocatore, posizione_corrente, board, wb, imprevisti):
    try:
        dado = int(input(f"{giocatore}, lancia i dadi (2-12): "))
        if not 2 <= dado <= 12:
            print("❌ Inserisci un numero tra 2 e 12.")
            return lancia_dadi(giocatore, posizione_corrente, board, wb)
    except ValueError:
        print("❌ Inserisci un numero valido.")
        return lancia_dadi(giocatore, posizione_corrente, board, wb)

    nuova_posizione = (posizione_corrente + dado) % len(board)

    casella = next((p for p in board if p["posizione"] == nuova_posizione), None)

    if not casella:
        print("❌ Casella non trovata.")
        return posizione_corrente  # Nessun cambiamento

    nome = casella['nome']
    tipo = casella.get('tipo')
    colore = casella.get('colore')
    affitto = casella.get('affitto', 0)
    proprietario = casella.get('acquistato')
    prezzo = casella.get("prezzo", 0)

    print(f"{giocatore} è atterrato su '{nome}', tipo: {tipo}, colore: {colore}")

    # Recupera il foglio del giocatore
    if giocatore in wb.sheetnames:
        foglio = wb[giocatore]
        turno = foglio.max_row  # Prima riga = intestazione

        # Recupera saldo precedente se esiste
        if turno > 1:
            saldo_precedente = foglio.cell(row=turno, column=6).value  #scelgie la colonna 6 e la riga del turno precedente
            if saldo_precedente is not None:
                saldo = saldo_precedente
            else:
                saldo= PATRIMONIO_INIZIALE
        else:
            saldo = PATRIMONIO_INIZIALE

        importo = 0

        # Logica proprietà
        if tipo == "proprietà":
            if not proprietario:
                scelta = input("🏠 Vuoi acquistare questa proprietà? (s/n): ").strip().lower()
                if scelta == "s":
                    if saldo >= prezzo:
                        saldo -= prezzo
                        importo = -prezzo
                        casella["acquistato"] = giocatore  
                        print(f"✅ {giocatore} ha acquistato {nome} per {prezzo}€.")
                        # Scrivi la board aggiornata
                        with open(BOARD_PATH, 'w', encoding='utf-8') as file:
                            json.dump(board, file, indent=4, ensure_ascii=False)
                    else:
                        print("💸 Fondi insufficienti per acquistare.")
                else:
                    print("⏭ Hai deciso di non acquistare.")

            elif proprietario != giocatore:
                print(f"💰 La proprietà è già stata acquistata da {proprietario}. Devi pagare l'affitto di {affitto}€.")
                importo = -affitto
                saldo += importo  # Diminuisce saldo del giocatore attuale

                # Accredita affitto al proprietario
                if proprietario in wb.sheetnames:
                    foglio_proprietario = wb[proprietario]
                    turno_proprietario = foglio_proprietario.max_row  # Prima riga è intestazione

                    # Recupera saldo precedente del proprietario
                    if turno_proprietario > 1:
                        saldo_prec = foglio_proprietario.cell(row=turno_proprietario, column=6).value
                        saldo_proprietario = saldo_prec + affitto if saldo_prec else PATRIMONIO_INIZIALE + affitto
                    else:
                        saldo_proprietario = PATRIMONIO_INIZIALE + affitto
                    foglio_proprietario.append([turno_proprietario, "", "","", affitto, saldo_proprietario,f"Incasso affitto da {giocatore}"])
                    print(f"transazione eseguita correttamente di euro {affitto} , beneficiario {proprietario} , ordinante {giocatore} ")
                else:
                    print(f"⚠️ Errore: foglio del proprietario '{proprietario}' non trovato.")

            elif proprietario == giocatore:
                case_hotel = input(f"Che bello rivederti {giocatore}, vuoi costruire case o hotel? (s/n) ").strip().lower()
                if case_hotel == "s":
                    cosa = input("Cosa vuoi costruire? (casa/hotel): ").strip().lower()

                    if cosa == "casa":
                        try:
                            numero_case = int(input("Quante case vuoi acquistare? (1-4): ").strip())
                        except ValueError:
                            print("❌ Inserisci un numero valido.")
                            return

                        if 1 <= numero_case <= 4:
                            if numero_case == 1:
                                chiave_affitto = f"affitto_{numero_case}_casa"
                            else:
                                chiave_affitto = f"affitto_{numero_case}_case"

                            affitto_delle_infrastrutture = casella.get(chiave_affitto, 0)
                            saldo -= affitto_delle_infrastrutture
                            descrizione = f"🏠 Costruite {numero_case} case per {affitto_delle_infrastrutture} euro. Affitto ora: {affitto_delle_infrastrutture}€"
                            foglio.append([turno, "", "", "", -affitto_delle_infrastrutture, saldo, descrizione])
                            casella["numero_case"] = numero_case
                        else:
                            print("⚠️ Puoi costruire solo da 1 a 4 case.")

                    elif cosa == "hotel":
                        if not casella.get("hotel") and casella.get("numero_case", 0) == 4:
                            hotel = casella.get("affitto_albergo", 0)
                            saldo -= hotel
                            descrizione = f"🏨 Costruito 1 hotel per {hotel} euro. Affitto ora: {hotel}€"
                            foglio.append([turno, "", "", "", -hotel, saldo, descrizione])
                            casella["hotel"] = True
                        elif casella.get("hotel"):
                            print("⚠️ Hai già costruito un hotel qui.")
                        else:
                            print("⚠️ Devi avere prima 4 case per costruire un hotel.")



        if tipo == "imprevisto":
            if imprevisti:
                imprevisto = random.choice(imprevisti)
                descrizione = imprevisto.get("testo")
                importo = imprevisto.get("premio", 0)
                saldo += importo
                foglio.append([turno,"","","",importo,saldo,descrizione])
                print(f"{descrizione}")
            else:
                print("⚠️ Nessun imprevisto disponibile.")

        if tipo == "stazione":
            if not proprietario:
                scelta = input("🏠 Vuoi acquistare questa proprietà? (s/n): ").strip().lower()
                if scelta == "s":
                    if saldo >= prezzo:
                        saldo -= prezzo
                        importo = -prezzo
                        casella["acquistato"] = giocatore  
                        print(f"✅ {giocatore} ha acquistato {nome} per {prezzo}€.")
                        # Scrivi la board aggiornata
                        with open(BOARD_PATH, 'w', encoding='utf-8') as file:
                            json.dump(board, file, indent=4, ensure_ascii=False)
                    else:
                        print("💸 Fondi insufficienti per acquistare.")
                else:
                    print("⏭ Hai deciso di non acquistare.")

            elif proprietario != giocatore:
                print(f"💰 La proprietà è già stata acquistata da {proprietario}. Devi pagare l'affitto di {affitto}€.")
                importo = -affitto
                saldo += importo  # Diminuisce saldo del giocatore attuale

                # Accredita affitto al proprietario
                if proprietario in wb.sheetnames:
                    foglio_proprietario = wb[proprietario]
                    turno_proprietario = foglio_proprietario.max_row  # Prima riga è intestazione

                    # Recupera saldo precedente del proprietario
                    if turno_proprietario > 1:
                        saldo_prec = foglio_proprietario.cell(row=turno_proprietario, column=6).value
                        saldo_proprietario = saldo_prec + affitto if saldo_prec else PATRIMONIO_INIZIALE + affitto
                    else:
                        saldo_proprietario = PATRIMONIO_INIZIALE + affitto
                    foglio_proprietario.append([turno_proprietario, "", "","", affitto, saldo_proprietario,f"Incasso affitto da {giocatore}"])
                    print(f"transazione eseguita correttamente di euro {affitto} , beneficiario {proprietario} , ordinante {giocatore} ")
                else:
                    print(f"⚠️ Errore: foglio del proprietario '{proprietario}' non trovato.")
           
        wb.save(EXCEL_PATH)
    else:
        print(f"⚠️ Foglio per {giocatore} non trovato.")

    return nuova_posizione



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
        posizioni[giocatore] = lancia_dadi(giocatore, posizioni[giocatore], board , wb , imprevisti)


if __name__ == "__main__":
    main()