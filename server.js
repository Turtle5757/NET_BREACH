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
        
        rooms[room].players[socket.id] = { score: 0, name: `User_${socket.id.substring(0,4)}` };
        
        // Tell everyone who is in the lobby
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
            const score = rooms[room].players[socket.id].score;
            
            io.to(room).emit('lobby_update', { players: rooms[room].players });

            if (score >= 15) {
                io.to(room).emit('winner', { id: socket.id, name: rooms[room].players[socket.id].name });
                rooms[room].active = false; // Reset for next round
            }
        }
    });

    socket.on('disconnect', () => {
        // Simple cleanup could be added here
    });
});

server.listen(process.env.PORT || 3000, () => console.log('Server running'));
