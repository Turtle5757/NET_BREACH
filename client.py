import socketio
import random
import time
import os

sio = socketio.Client()
is_frozen = False

# --- PUZZLE GENERATOR ---
def get_puzzle():
    puzzles = [
        ("encryption", "noitpyrcne"), ("kernel", "lenrek"),
        ("firewall", "llawerif"), ("bandwidth", "htdiwdnab"),
        ("database", "esabatad"), ("mainframe", "emarf niam")
    ]
    return random.choice(puzzles)

# --- EVENTS ---
@sio.on('update')
def on_update(data):
    print(f"\n[SYSTEM] Player {data['player'][:5]} score: {data['score']}/10")

@sio.on('attacked')
def on_attacked(data):
    global is_frozen
    is_frozen = True
    print(f"\n[!!!] ALERT: LATENCY SPIKE DETECTED BY {data['by'][:5]}")
    print("[!!!] SYSTEM FROZEN FOR 5 SECONDS...")
    time.sleep(5)
    is_frozen = False
    print("[!!!] SYSTEM RECOVERED. RESUME HACKING.")

@sio.on('winner')
def on_winner(data):
    print(f"\n\n!!! CRITICAL FAILURE !!!\nPlayer {data['winner'][:5]} won.")
    os._exit(0)

# --- MAIN GAME ---
def start():
    # RENAME THIS to your Render URL after deploying
    url = 'https://net-breach.onrender.com' 
    
    try:
        sio.connect(url)
    except:
        print("Connection failed.")
        return

    score = 0
    print("--- NET_BREACH TERMINAL ---")
    
    while score < 10:
        if not is_frozen:
            answer, scrambled = get_puzzle()
            print(f"\nDECRYPT: {scrambled}")
            guess = input(">> ").strip().lower()
            
            if is_frozen: # Check if we got attacked while typing
                continue

            if guess == answer:
                score += 1
                print(f"Correct. Score: {score}")
                sio.emit('solve_puzzle')
            else:
                print("Incorrect.")

if __name__ == "__main__":
    start()
