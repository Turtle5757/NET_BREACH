import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# Structure: { room_id: { sid: {score: 0, streak: 0} } }
rooms = {}

@sio.event
def connect(sid, environ):
    print(f"Connection attempt: {sid}")

@sio.event
def join_room(sid, data):
    room = data['room'].lower()
    sio.enter_room(sid, room)
    
    if room not in rooms:
        rooms[room] = {}
    
    rooms[room][sid] = {"score": 0, "streak": 0}
    print(f"Hacker {sid} joined room: {room}")
    sio.emit('message', f"User_{sid[:4]} joined the lobby.", room=room)

@sio.event
def solve_puzzle(sid, data):
    room = data['room'].lower()
    if room in rooms and sid in rooms[room]:
        rooms[room][sid]["score"] += 1
        rooms[room][sid]["streak"] += 1
        score = rooms[room][sid]["score"]
        
        # Sabotage: Every 3 correct answers attacks others in the SAME room
        if rooms[room][sid]["streak"] >= 3:
            rooms[room][sid]["streak"] = 0
            sio.emit('attacked', {"by": sid}, room=room, skip_sid=sid)
        
        sio.emit('update', {"player": sid, "score": score}, room=room)
        
        if score >= 15:
            sio.emit('winner', {"winner": sid}, room=room)

@sio.event
def disconnect(sid):
    for room in rooms:
        if sid in rooms[room]:
            del rooms[room][sid]
            break

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
