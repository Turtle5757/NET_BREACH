import socketio
import random
import time
import os

sio = socketio.Client()
is_frozen = False
current_room = ""

def get_puzzle():
    puzzle_type = random.choice(["scramble", "math", "binary"])
    if puzzle_type == "scramble":
        words = ["proxy", "gateway", "payload", "cipher", "phishing"]
        target = random.choice(words)
        return target, f"UNSCRAMBLE: {''.join(random.sample(target, len(target)))}"
    elif puzzle_type == "math":
        a, b = random.randint(10, 60), random.randint(10, 60)
        return str(a + b), f"DECRYPT SUM: {a} + {b}"
    elif puzzle_type == "binary":
        num = random.randint(1, 15)
        return str(num), f"CONVERT BINARY {bin(num)[2:].zfill(4)} TO DECIMAL"

@sio.on('message')
def on_message(msg):
    print(f"\n[LOBBY] {msg}")

@sio.on('update')
def on_update(data):
    print(f"\n[NETWORK] User_{data['player'][:4]} score: {data['score']}/15")

@sio.on('attacked')
def on_attacked(data):
    global is_frozen
    is_frozen = True
    print(f"\n[!!!] DDoS ATTACK BY User_{data['by'][:4]}. SYSTEM FROZEN...")
    time.sleep(5)
    is_frozen = False
    print("[!!!] REBOOT COMPLETE.")

@sio.on('winner')
def on_winner(data):
    print(f"\n\n[CRITICAL] User_{data['winner'][:4]} BYPASSED THE MAINFRAME.")
    os._exit(0)

def start():
    # --- UPDATE TO YOUR RENDER URL ---
    RENDER_URL = 'https://net-breach.onrender.com' 
    
    try:
        sio.connect(RENDER_URL)
    except:
        print("COULD NOT CONNECT TO NETWORK.")
        return

    print("====================================")
    print("      WELCOME TO NET_BREACH v1.1    ")
    print("====================================")
    global current_room
    current_room = input("Enter Secret Lobby Name: ").strip().lower()
    sio.emit('join_room', {'room': current_room})
    
    print(f"\nWAITING FOR OTHERS IN '{current_room}'...")
    print("Press Enter to start hacking when ready!")
    input()

    score = 0
    while score < 15:
        if not is_frozen:
            answer, task = get_puzzle()
            print(f"\n{task}")
            guess = input("root@breach:~# ").strip().lower()
            
            if is_frozen: continue

            if guess == answer:
                score += 1
                sio.emit('solve_puzzle', {'room': current_room})
                print(f"ACCEPTED. PROGRESS: {score}/15")
            else:
                print("DENIED.")

if __name__ == "__main__":
    start()
