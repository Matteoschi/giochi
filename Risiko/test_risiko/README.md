

## 🧪 Debugging & Randomized Version (`risiko_random.py`)

Alongside the main script (`risiko.py`), this project also includes an **alternative version** called **`risiko_random.py`**.  
This file is not meant for actual gameplay between human players, but is instead a **debugging and stress-testing tool** created to help validate the correctness of the core mechanics.

### 🔍 Purpose of `risiko_random.py`

In the normal `risiko.py`, many parts of the game require **user input**:
- Choosing where to place reinforcements  
- Selecting which territory to attack from and which one to target  
- Deciding how many dice to roll in an attack or defense  
- Managing card exchanges and troop movements  

While this is essential for real players, it makes **debugging complex game logic** difficult, because:
- You need to manually enter commands each time  
- You cannot easily simulate **multiple full games**  
- Edge cases (like rare attack outcomes or continent control scenarios) may take a long time to appear naturally  

To solve this, `risiko_random.py` **automates all user decisions** using **random choices**.  

---

### ⚙️ How It Works

- Every time the main game requires input (e.g., troop placement, attack selection), the **computer randomly picks a valid option**.  
- The flow of the game is **fully automatic**: once started, it proceeds without waiting for players.  
- Troop numbers, dice rolls, objectives, and attacks are all decided by **pseudo-randomness**.  

This way, the game can:
1. **Run unattended** from start to finish  
2. **Stress test rules** by exploring many random scenarios  
3. Help developers identify **logical inconsistencies** or **Excel integration bugs**  

---

### 🛠 Why It’s Useful for Debugging

The random version allows developers to:
- **Quickly simulate dozens of games** without human input  
- Verify that:
  - Territories are always distributed correctly  
  - Troop counts never become negative  
  - Battles resolve according to Risiko rules  
  - Continent bonuses are calculated consistently  
  - Victory and elimination conditions trigger properly  
- Spot **rare bugs** that only occur under unusual conditions (e.g., when a player simultaneously completes multiple objectives)  

Essentially, `risiko_random.py` acts as a **stress-testing sandbox**: instead of carefully orchestrated matches, it produces **chaotic and unpredictable games** that are ideal for shaking out hidden problems.

---

### 🎲 Benefits of Randomized Testing

- **Faster iterations**: You can run the game multiple times in a row without intervention  
- **Coverage of edge cases**: Random decisions expose the system to scenarios that human players might never choose  
- **Automatic error discovery**: If an exception or invalid game state occurs, it’s much easier to spot and fix  
- **Confidence in stability**: After dozens of random runs without errors, developers can trust that the system handles a wide range of possibilities  

---

### 🚫 Not for Real Gameplay

It is important to note that `risiko_random.py` is **not intended for normal use**:
- Human players will have **no control** over what happens  
- The game will feel **nonsensical**, as all moves are random and not strategic  
- The sole purpose is **debugging, testing, and development**  

For real matches, always use the **main file `risiko.py`**, where players can interact, make decisions, and enjoy the full experience of Risiko.

---

✅ In short:  
- `risiko.py` → for **real human gameplay**  
- `risiko_random.py` → for **debugging, automated testing, and error discovery**

---
