const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(express.static('.')); // Serves your index.html

let rooms = {};

io.on('connection', (socket) => {
    socket.on('join_room', (room) => {
        socket.join(room);
        if (!rooms[room]) rooms[room] = {};
        rooms[room][socket.id] = { score: 0 };
        io.to(room).emit('system_msg', `User joined the breach.`);
    });

    socket.on('solve', (room) => {
        if (rooms[room] && rooms[room][socket.id]) {
            rooms[room][socket.id].score++;
            let score = rooms[room][socket.id].score;
            io.to(room).emit('score_update', { id: socket.id, score: score });

            if (score >= 15) io.to(room).emit('winner', socket.id);
        }
    });
});

server.listen(process.env.PORT || 3000, () => console.log('Server running'));
