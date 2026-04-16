import socketio
import eventlet
import random

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

players = {}

@sio.event
def connect(sid, environ):
    players[sid] = {"score": 0, "streak": 0}
    print(f"Hacker {sid} has breached the entry point.")

@sio.event
def solve_puzzle(sid):
    if sid in players:
        players[sid]["score"] += 1
        players[sid]["streak"] += 1
        score = players[sid]["score"]
        streak = players[sid]["streak"]

        # Trigger sabotage on a streak of 3
        if streak >= 3:
            players[sid]["streak"] = 0 # Reset streak
            print(f"Player {sid} launched a DDoS attack!")
            sio.emit('attacked', {"by": sid}, skip_sid=sid)
        
        sio.emit('update', {"player": sid, "score": score})
        
        if score >= 15: # Increased winning score to 15
            sio.emit('winner', {"winner": sid})

@sio.event
def disconnect(sid):
    if sid in players:
        del players[sid]

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
