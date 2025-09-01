# 🎲 Risiko Python Manager

This project is a **Python-based game manager for Risiko!**  
It allows players to create, track, and manage a full game of Risiko with **automatic territory assignment, objective handling, troop placement, attacks, continent bonuses, and victory conditions** — all integrated with an **Excel file (`RisiKo.xlsx`)** for persistence and transparency.

The script is fully interactive and guides players through every stage of the game.

---

## 📑 Table of Contents

1. [Features](#-features)  
2. [Requirements](#-requirements)  
3. [File Structure](#-file-structure)  
4. [How It Works](#-how-it-works)  
   - [Initialization](#initialization)  
   - [Player Management](#player-management)  
   - [Territory Assignment](#territory-assignment)  
   - [Objectives](#objectives)  
   - [Troop Placement](#troop-placement)  
   - [Attacks & Battles](#attacks--battles)   
5. [Excel File Details](#-excel-file-details)  
6. [JSON File Formats](#-json-file-formats)  
   - [territori.json](#territorijson)  
   - [obiettivi.json](#obiettivijson)  
   - [continenti.json](#continentijson)  
---

## ✨ Features

- ✅ Load **territories, objectives, and continents** from JSON files  
- ✅ **Interactive player registration** (3–6 players)  
- ✅ Assign **unique colors** per player  
- ✅ Generate and manage a **Risiko Excel file** with sheets per player  
- ✅ Automatically **assign territories and secret objectives**  
- ✅ Handle **initial troop placement** (with rules by player count)  
- ✅ **Turn-based system** with troop bonuses, card exchanges, and reinforcements  
- ✅ **Battle system** (dice-based combat, troop losses, territory conquest)  
- ✅ **Continent bonuses** (Europe, Asia, Americas, Africa, Oceania)  
- ✅ **Victory conditions** (objectives or number of territories)  
- ✅ Automatic **elimination of defeated players**  
- ✅ Full **Excel integration** with troops, territories, objectives, and cards  

---

## 🛠 Requirements

- **Python 3.8+**
- [openpyxl](https://pypi.org/project/openpyxl/) (for Excel integration)
- JSON files (`territori.json`, `obiettivi.json`, `continenti.json`)

Install dependencies:

```bash
pip install openpyxl
```

```bash
Risiko/
│── RisiKo.xlsx              # Generated game Excel file
│── territori.json           # All territories
│── obiettivi.json           # Secret objectives
│── continenti.json          # Continent groupings
│── risiko.py                # Main Python script
```

## ⚙️ How It Works
### Initialization

- Create the RisiKo.xlsx file in a Risiko/ folder

- Add one sheet per player

- Store player info (name, color, starting troops, secret objective)

### Player Management

- Prompt user for number of players (3–6)

- Each player inputs their name and color (from: giallo, rosso, verde, blu, viola, nero)

- Starting troops:

    - 3 players → 35

    - 4 players → 30

    - 5 players → 25

    - 6 players → 20

### Territory Assignment

- Territories are randomly shuffled and evenly distributed among players

- Each sheet stores:

    - Territory name

    - Continent

    - Symbol (used for cards)

    - Troop count (initially 1, then updated)

### Objectives

- Each player receives a random secret objective from obiettivi.json

- Stored in cell B5 of the player’s sheet

### Troop Placement

- Troops are placed automatically:

    - 1 troop per territory initially

    - Remaining troops are placed manually by players

- Each turn, reinforcements are calculated:

    - At least territories // 3

    - Plus continent bonuses

    - Plus card bonuses if a valid set is played

### Attacks & Battles

- Player chooses an attacking state and a target state

- Attacks are resolved with dice (attacker: up to 3, defender: up to 2)

- Dice results determine troop losses

- If a defender loses all troops, the territory changes owner

## 📊 Excel File Details

Each player has a dedicated sheet with:

General Info:

- Name

- Color

- Starting Troops

- Secret Objective

Territories Table:

- Column A → Territory Name

- Column B → Continent

- Column C → Symbol

- Column D → Troops

| Nome     | Continente         | Simbolo | numero Truppe |
| -------- | ------------------ | ------- | ------------- |
| alaska   | america\_del\_nord | fante   | 3             |
| brasilia | america\_del\_sud  | cavallo | 2             |


## 📜 JSON File Formats
### territori.json
```json
[
  {
    "nome": "alaska",
    "continente": "america_del_nord",
    "simbolo": "fante"
  },
  {
    "nome": "brasile",
    "continente": "america_del_sud",
    "simbolo": "cavallo"
  }
]
```
### obiettivi.json
```json
[
  { "descrizione": "Conquistare l'Asia e l'Africa." },
  { "descrizione": "Conquistare il Nord America e l'Europa." },
  { "descrizione": "Conquistare 24 territori." }
]
```
### continenti.json
```json

{
  "europa": ["islanda", "scandinavia", "ucraina", "europa_occidentale", "europa_meridionale", "europa_settentrionale", "gran_bretagna"],
  "asia": ["ural", "siberia", "mongolia", "cina", "india", "medio_oriente", "giappone"],
  "america_del_nord": ["alaska", "alberta", "ontario", "quebec", "groenlandia", "stati_uniti_occidentali", "stati_uniti_orientali", "america_centrale"],
  "america_del_sud": ["venezuela", "brasile", "perù", "argentina"],
  "africa": ["egitto", "congo", "sudafrica", "madagascar", "africa_orientale", "africa_settentrionale"],
  "oceania": ["australia_occidentale", "australia_orientale", "nuova_guinea", "indonesia"]
}
```
## 🔄 Game Flow

1) Register players (names & colors)

2) Load JSON files (territories, objectives, continents)

3) Create new RisiKo.xlsx

4) Assign objectives and territories

5) Players place initial troops

6) Turn Loop begins:

    - Calculate reinforcements

    - Place new troops

    - (Optional) Exchange cards

    - Attack opponents

    - Move troops

    - Check eliminations & victory

7) End when only one player remains or an objective is completed

## ⚠️ Known Limitations

- Manual dice input (players must type dice rolls instead of automatic random rolls)

- Some functions (e.g., troop placement, state lookup) assume fixed row ranges (9–30) in Excel → limited scalability

- Error handling is basic (inputs can cause invalid states if players insist)

- JSON paths are hardcoded, must be updated manually