import socketio
import eventlet
import random

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

players = {}

@sio.event
def connect(sid, environ):
    players[sid] = {"score": 0}
    print(f"Hacker {sid} connected.")

@sio.event
def solve_puzzle(sid):
    if sid in players:
        players[sid]["score"] += 1
        score = players[sid]["score"]
        
        # 20% chance to trigger a sabotage attack on everyone else
        if random.random() < 0.20:
            print(f"Player {sid} triggered a Latency Spike!")
            sio.emit('attacked', {"by": sid}, skip_sid=sid)
            
        sio.emit('update', {"player": sid, "score": score})
        
        if score >= 10:
            sio.emit('winner', {"winner": sid})

@sio.event
def disconnect(sid):
    if sid in players:
        del players[sid]

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
