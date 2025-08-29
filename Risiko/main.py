import os
from openpyxl import Workbook, load_workbook
import random
import json

territori = r"C:\Users\alessandrini\Documents\coding\games\Risiko\territori.json"
obiettivi = r"C:\Users\alessandrini\Documents\coding\games\Risiko\obiettivi.json"
continenti = r"C:\Users\alessandrini\Documents\coding\games\Risiko\continenti.json"
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

def carica_continenti():
    try:
        if not os.path.exists(continenti):
            print(f"❌ File continenti non trovato: {continenti}")
            return []
        else:
            with open(territori, 'r', encoding='utf-8') as file_continenti:
                return json.load(file_continenti)
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
                territorio["nome"].lower(),
                territorio["continente"].lower(),
                territorio["simbolo"].lower().strip()
            ])

    wb.save(EXCEL_PATH)
    print("✅ Territori assegnati ai giocatori, visulaizzabili file exel")
    return numero_carte

# ------------------- ASSEGNAZIONE OBIETTIVI -------------------

def assegna_obiettivi(lista_giocatori, wb, file_obiettivi):
    obiettivi= file_obiettivi.copy()
    random.shuffle(obiettivi)

    for giocatore in lista_giocatori:
        ws = wb[giocatore]
        obiettivo = obiettivi.pop()
        ws["B5"] = obiettivo["descrizione"]  # Obiettivo segreto in B5
    wb.save(EXCEL_PATH)
    print("✅ obiettivi assegnati ai giocatori, visulaizza file exel")

# ------------------- ASSEGNAZIONE TRUPPE -------------------

def inserire_truppe_iniziali(lista_giocatori, wb,pedine_iniziali,numero_carte):
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

# ------------------- ASSEGNA TRUPPE PER TERRITORI -------------------

def conta_territori(lista_giocatori, wb):

    for giocatore in lista_giocatori:
        territori_giocatore , count= visualizza_stati_numero(giocatore)

        pedine_da_posizionare = count // 3
        print(f"Il giocatore {giocatore} ha {count} territori, quindi spettano {pedine_da_posizionare} pedine.")

        truppe_posizionate = 0

        while truppe_posizionate < pedine_da_posizionare:
            dove = input("Dove vuoi posizionare le truppe? ").strip()
            if dove not in territori_giocatore:
                print("⚠️ Territorio non trovato. Riprova.")
                continue

            try:
                quante = int(input(f"Quante truppe vuoi posizionare in {dove}? "))
            except ValueError:
                print("❌ Inserisci un numero valido.")
                continue

            if quante <= 0 or truppe_posizionate + quante > pedine_da_posizionare:
                print(f"⚠️ Puoi posizionare al massimo {pedine_da_posizionare - truppe_posizionate} truppe.")
                continue

            # Trova la riga del territorio e scrivi le truppe in colonna D
            for riga in range(9, 22):
                if ws[f"A{riga}"].value == dove:
                    ws[f"D{riga}"] = quante
                    break

            truppe_posizionate += quante
            print(f"✅ Posizionate {quante} truppe in {dove} ({truppe_posizionate}/{pedine_da_posizionare})")

    wb.save(EXCEL_PATH)
    print("✅ Tutte le truppe sono state salvate nel file Excel.")

# ------------------- VISUALIZZA STATI (NO MAIN) -------------------

def visualizza_stati_numero(giocatore):
    ws = wb[giocatore]
    n_territori = 0
    territori_giocatore = []
    for riga in range(9, 23):  # righe dove ci sono i territori
        nome_territorio = ws[f"A{riga}"].value
        if nome_territorio:  # <-- meglio controllare che non sia None
            territori_giocatore.append(nome_territorio)
            n_territori += 1
    return territori_giocatore, n_territori

# ------------------- VISUALIZZA ARMATE PER STATI (NO MAIN) -------------------

def trova_truppe_riga_stato(giocatore, stato):
    ws = wb[giocatore]
    for riga in range(9, 23):
        if ws[f"A{riga}"].value == stato:
            return ws[f"D{riga}"].value, riga  # restituisco anche la riga
    return 0, None

# ------------------- VISUALIZZA GIOCATORI CON PAESE (NO MAIN) -------------------
def trova_giocatore(lista_giocatori, paese):
    for giocatore in lista_giocatori:
        ws = wb[giocatore]
        for riga in range(9, 23):  # <-- così controlli tutte le righe da 9 a 22
            if ws[f"A{riga}"].value == paese:
                return giocatore
    return None  # se non trovato


# ------------------- AGGIORNA NUMERO TRUPPE (NO MAIN) -------------------
def aggiorna_truppe_stato(giocatore,stato,n_truppe_aggiornate):
    ws=wb[giocatore]
    _ , riga =  trova_truppe_riga_stato(giocatore,stato)
    valore_casella_attuale = ws[f"D{riga}"].value
    ws[f"D{riga}"].value = valore_casella_attuale + n_truppe_aggiornate

    print(f"{giocatore} ora ha in {stato}: {ws[f'D{riga}'].value}")
    wb.save(EXCEL_PATH)
    print("file aggiornato con successo")

# ------------------- PASSAGGIO STATO (NO MAIN) -------------------

def passaggio_stato(donatore, beneficiario, stato):
    # ws del donatore e beneficiario
    ws_donatore = wb[donatore]
    ws_beneficiario = wb[beneficiario]

    # cerca la riga del territorio nello stato donatore
    _, riga = trova_truppe_riga_stato(donatore, stato)

    if riga is None:
        print(f"{stato} non trovato tra i territori di {donatore}")
        return

    # leggi i dati del territorio
    nome = ws_donatore[f"A{riga}"].value
    continente = ws_donatore[f"B{riga}"].value
    simbolo = ws_donatore[f"C{riga}"].value

    n_truppe_spostate= int(input("quante truppe vuoi spostare ? min 1"))

    # aggiungi il territorio al beneficiario
    ws_beneficiario.append([
        nome.lower(),
        continente.lower(),
        simbolo.lower(),
        n_truppe_spostate  # puoi decidere quante truppe lasciare
    ])

    # elimina il territorio dal donatore (svuota riga)
    for col in ["A","B","C","D"]:
        ws_donatore[f"{col}{riga}"].value = None

    wb.save(EXCEL_PATH)
    print(f"{stato} trasferito da {donatore} a {beneficiario} con successo.")


# ------------------- ATTACCO -------------------

def attacco(lista_giocatori, giocatore):

    territori_giocatore , _ = visualizza_stati_numero(giocatore)
    stato_attacco= input(f"{giocatore} quale stato vuoi attaccare ? ").lower()
    stato_partenza = input(f"da quale stato parti ? ").lower()

    difensore = trova_giocatore(lista_giocatori, stato_attacco)

    if stato_partenza not in territori_giocatore:
        print(f"impossibile trovare lo stato di partenza di {giocatore}")
    
    numero_truppe_stato_attaccante , _ = trova_truppe_riga_stato(giocatore, stato_partenza)
    n_armate_attaccante = int(input(f"Con quante armate desideri attaccare {difensore} ? (max 3 ): "))
    while True:
        if n_armate_attaccante > 3 or n_armate_attaccante < 1:
            print("inserire da 1-3 armate")
            continue
        if n_armate_attaccante >= numero_truppe_stato_attaccante:
            print(f"Truppe nello stato {stato_partenza} insufficienti: {giocatore} ha selezionato {n_armate_attaccante} truppe, ma almeno una truppa deve rimanere nello stato di partenza.")
            continue
        else:
            break

    dado_attaccante=int(input(f"numero più alto del dado di {giocatore} "))
    dado_difensore = int(input(f"numero più alto del dado del {difensore} "))

    if dado_attaccante <= dado_difensore :
        print(f"ha vinto il {difensore}")
        aggiorna_truppe_stato(giocatore,stato_partenza,-1)
    else:
        print(f"ha vinto {giocatore}")
        aggiorna_truppe_stato(difensore,stato_attacco,-1)

        numero_truppe_stato_difensore , _ = trova_truppe_riga_stato(difensore, stato_attacco)

        if numero_truppe_stato_difensore == 0:
            print(f"{difensore} non ha più truppe nello stato {stato_attacco} il paese passa a {giocatore}")
            passaggio_stato(difensore,giocatore,stato_attacco)
        elif numero_truppe_stato_attaccante == 0:
                print(f"{giocatore} non ha più truppe nello stato {stato_partenza} il paese passa a {difensore}")
                passaggio_stato(giocatore,difensore,stato_partenza)

# ------------------- ELIMINAZIONE GIOCATORE -------------------

def eliminazione_giocatore(lista_giocatori, turno):
    lista_sopravvissuti = []
    for giocatore in lista_giocatori:
        _ , n_territori = visualizza_stati_numero(giocatore)
        if n_territori == 0:
            print(f"Il giocatore {giocatore} è stato SCONFITTO al turno {turno} in quanto non possiede più territori")
        else:
            lista_sopravvissuti.append(giocatore)
    return lista_sopravvissuti

# ------------------- VINCITORE -------------------

def vincitore(giocatore, continenti):
    ws = wb[giocatore]
    obiettivo_assegnato = ws["B5"].value
    territori_giocatore, numero_stati = visualizza_stati_numero(giocatore)

    if obiettivo_assegnato == "Conquistare l'Europa, il Sud America e un terzo continente a scelta.":
        
        if all(t in territori_giocatore for t in continenti["europa"] + continenti["america_del_sud"]):
            print(f"{giocatore} ha conquistato Europa e Sud America!")

            altri_continenti = ["africa", "asia", "oceania", "america_del_nord"]
            for cont in altri_continenti:
                if all(t in territori_giocatore for t in continenti[cont]):
                    print(f"{giocatore} ha conquistato anche {cont}, obiettivo completato!")
                    return giocatore, True
    
    elif obiettivo_assegnato == "Conquistare l'Europa, l'Oceania e un terzo continente a scelta.":

        if all(t in territori_giocatore for t in continenti["europa"] + continenti["oceania"]):
            print(f"{giocatore} ha conquistato Europa e oceania!")

            altri_continenti = ["africa", "asia", "america_del_sud", "america_del_nord"]
            for cont in altri_continenti:
                if all(t in territori_giocatore for t in continenti[cont]):
                    print(f"{giocatore} ha conquistato anche {cont}, obiettivo completato!")
                    return giocatore, True    

    elif obiettivo_assegnato == "Conquistare l'Asia e il Sud America.":
        if all(t in territori_giocatore for t in continenti["asia"] + continenti["america_del_sud"]):
            print(f"{giocatore} ha conquistato asia e Sud America!")
            return giocatore, True  

    elif obiettivo_assegnato == "Conquistare l'Asia e l'Africa.":
        if all(t in territori_giocatore for t in continenti["asia"] + continenti["africa"]):
            print(f"{giocatore} ha conquistato asia e africa!")
            return giocatore, True  

    elif obiettivo_assegnato == "Conquistare il Nord America e l'Africa.":
        if all(t in territori_giocatore for t in continenti["america_del_nord"] + continenti["africa"]):
            print(f"{giocatore} ha conquistato nord america e africa!")
            return giocatore, True  

    elif obiettivo_assegnato == "Conquistare il Nord America e l'Oceania.":
        if all(t in territori_giocatore for t in continenti["america_del_nord"] + continenti["oceania"]):
            print(f"{giocatore} ha conquistato nord america e oceania!")
            return giocatore, True    

    elif obiettivo_assegnato == "Conquistare il Nord America e l'Europa.":
        if all(t in territori_giocatore for t in continenti["america_del_nord"] + continenti["europa"]):
            print(f"{giocatore} ha conquistato nord america e europa!")
            return giocatore, True

    elif obiettivo_assegnato == "Conquistare l'Africa e l'Europa.":
        if all(t in territori_giocatore for t in continenti["africa"] + continenti["europa"]):
            print(f"{giocatore} ha conquistato africa e europa!")
            return giocatore, True

    elif numero_stati == 24:
            print(f"{giocatore} ha conquistato 24 territori!")
            return giocatore, True

    elif numero_stati == 18:
            print(f"{giocatore} ha conquistato 18 territori!")
            return giocatore, True  

    return giocatore ,False

# ------------------- MAIN -------------------

if __name__ == "__main__":
    # ------------------- INIZIALIZZAZIONE -------------------
    lista_giocatori, n_giocatori = aggiungi_giocatori()
    lista_colori = assegna_colore(lista_giocatori)
    pedine_iniziali = pedine_distart(lista_giocatori)

    file_territori = carica_territori()
    file_obiettivi = carica_obiettivi()
    file_continenti = carica_continenti()
    
    wb, ws = verifica_file(lista_giocatori, lista_colori, pedine_iniziali)
    assegna_obiettivi(lista_giocatori, wb, file_obiettivi)
    numero_carte = assegna_territori(file_territori, lista_giocatori, wb)
    inserire_truppe_iniziali(lista_giocatori, wb, pedine_iniziali, numero_carte)

    # ------------------- CICLO DI GIOCO -------------------
    turno = 0
    while len(lista_giocatori) > 1:
        giocatore = lista_giocatori[turno % len(lista_giocatori)]
        print(f"\n--- È il turno di {giocatore} ---")

        while True:
            # scelta azione
            try:
                scelta_azione = int(input("Vuoi (1) passare, (2) attaccare o (3) muovere truppe? "))
            except ValueError:
                print("Inserisci un numero valido.")
                continue

            # ------------------- PASSA TURNO -------------------
            if scelta_azione == 1:
                print(f"{giocatore} ha terminato il turno.\n")
                break

            # ------------------- ATTACCO -------------------
            elif scelta_azione == 2:
                print("\n--- Modalità attacco ---")
                while True:
                    attacco(lista_giocatori, giocatore)
                    continua_attacco = input("Vuoi attaccare ancora? (s/n) ").lower()
                    if continua_attacco != 's':
                        break
                print("--- Fine attacco ---")

            # ------------------- SPOSTAMENTO TRUPPE -------------------
            elif scelta_azione == 3:
                print("\n--- Modalità spostamento truppe ---")
                while True:
                    stato_donatore = input("Da quale stato vuoi prelevare le truppe? ").lower()
                    stato_beneficiario = input("In quale stato vuoi posizionare le truppe? ").lower()
                    try:
                        n_truppe_da_posizionare = int(input(f"Quante truppe vuoi spostare da {stato_donatore} a {stato_beneficiario}? "))
                    except ValueError:
                        print("Numero truppe non valido.")
                        continue

                    truppe_disponibili, _ = trova_truppe_riga_stato(giocatore, stato_donatore)
                    if n_truppe_da_posizionare >= truppe_disponibili:
                        print(f"Non puoi spostare più truppe di quante ce ne sono nello stato {stato_donatore}.")
                        continue

                    aggiorna_truppe_stato(giocatore, stato_donatore, -n_truppe_da_posizionare)
                    aggiorna_truppe_stato(giocatore, stato_beneficiario, n_truppe_da_posizionare)

                    continua_spostamento = input("Vuoi spostare ancora delle truppe? (s/n) ").lower()
                    if continua_spostamento != 's':
                        break
                print("--- Fine spostamento truppe ---")

            else:
                print("Scelta non valida. Riprova.")

        # ------------------- ELIMINAZIONE GIOCATORI -------------------
        lista_giocatori = eliminazione_giocatore(lista_giocatori, turno)
        if len(lista_giocatori) == 1:
            print(f"🎉 Il vincitore è {lista_giocatori[0]}!")
            break
        giocatore_vittorioso , vittoria = vincitore(giocatore,file_continenti)
        if vittoria == True:
            print(f"ABBIAMO UN VINCITORE : {giocatore_vittorioso}")
            break

        turno += 1
