const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});
// Tarjoillaan index.html pääsivuna
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Kuunnellaan Socket.IO-yhteyksiä
io.on('connection', (socket) => {
  console.log('Käyttäjä liittyi chattiin');

  // server.js - Lisätään viestin lähetysaika
socket.on('chat message', (kryptattu) => {
  if (typeof msg === 'string' && msg.length <= 5000) {
    // Lisätään aikaleima, jotta ajastin on synkronoitu
    const timestampedMsg = { data: kryptattu, timestamp: Date.now() };
    io.emit('chat message', timestampedMsg);
  }
});

  socket.on('disconnect', () => {
    console.log('Käyttäjä poistui chatista');
  });
});

// Käytetään ympäristömuuttujan PORT-arvoa (esim. Renderissä) tai oletuksena 3000
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Chat_boxing-palvelin käynnissä portissa ${PORT}`);
});
