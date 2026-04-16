import socketio
import random
import time
import os

sio = socketio.Client()
is_frozen = False

def get_puzzle():
    puzzle_type = random.choice(["scramble", "math", "binary"])
    
    if puzzle_type == "scramble":
        words = ["proxy", "gateway", "payload", "cipher", "phishing", "malware"]
        target = random.choice(words)
        scrambled = "".join(random.sample(target, len(target)))
        return target, f"UNSCRAMBLE: {scrambled}"
    
    elif puzzle_type == "math":
        a, b = random.randint(10, 50), random.randint(10, 50)
        return str(a + b), f"DECRYPT SUM: {a} + {b}"
    
    elif puzzle_type == "binary":
        num = random.randint(1, 15)
        binary = bin(num)[2:].zfill(4)
        return str(num), f"CONVERT BINARY {binary} TO DECIMAL"

@sio.on('update')
def on_update(data):
    print(f"\n[NETWORK] User_{data['player'][:4]} progress: {data['score']}/15")

@sio.on('attacked')
def on_attacked(data):
    global is_frozen
    is_frozen = True
    print(f"\n[!!!] WARNING: DDoS ATTACK BY User_{data['by'][:4]}")
    print("[!!!] CONNECTION DROPPED. REBOOTING...")
    time.sleep(5)
    is_frozen = False
    print("[!!!] REBOOT COMPLETE. RESUME.")

@sio.on('winner')
def on_winner(data):
    print(f"\n\n[CRITICAL] ACCESS GRANTED TO User_{data['winner'][:4]}")
    print("YOU LOST. SYSTEM SHUTDOWN.")
    os._exit(0)

def start():
    # --- UPDATE THIS URL AFTER DEPLOYING TO RENDER ---
    RENDER_URL = 'https://net-breach.onrender.com' 
    
    try:
        sio.connect(RENDER_URL)
        print("CONNECTED TO NET_BREACH V1.0")
    except:
        print("ERROR: COULD NOT CONNECT TO HOST.")
        return

    score = 0
    while score < 15:
        if not is_frozen:
            answer, task = get_puzzle()
            print(f"\n{task}")
            guess = input("root@breach:~# ").strip().lower()
            
            if is_frozen: continue

            if guess == answer:
                score += 1
                print(f"OK. NODE {score} SECURED.")
                sio.emit('solve_puzzle')
            else:
                print("ACCESS DENIED.")

if __name__ == "__main__":
    start()
