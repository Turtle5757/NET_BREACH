const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(express.static('.'));

let rooms = {};

io.on('connection', (socket) => {
    socket.on('join_room', (room) => {
        socket.join(room);
        if (!rooms[room]) {
            rooms[room] = { host: socket.id, active: false, players: {} };
        }
        
        rooms[room].players[socket.id] = { score: 0, name: `Hacker_${socket.id.substring(0,4)}` };
        
        io.to(room).emit('lobby_update', {
            players: rooms[room].players,
            host: rooms[room].host,
            active: rooms[room].active
        });
    });

    socket.on('start_game', (room) => {
        if (rooms[room] && rooms[room].host === socket.id) {
            rooms[room].active = true;
            io.to(room).emit('game_start');
        }
    });

    socket.on('solve', (room) => {
        if (rooms[room] && rooms[room].active) {
            rooms[room].players[socket.id].score++;
            io.to(room).emit('lobby_update', { players: rooms[room].players });

            if (rooms[room].players[socket.id].score >= 15) {
                io.to(room).emit('winner', { id: socket.id, name: rooms[room].players[socket.id].name });
                rooms[room].active = false;
            }
        }
    });

    socket.on('disconnect', () => {
        // Simple cleanup can be added here if needed
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
