const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Tarjotaan staattiset tiedostot (kuten index.html) samasta kansiosta
app.use(express.static(__dirname));

io.on('connection', (socket) => {
  console.log('QEMU-solmu yhdistetty socketin kautta:', socket.id);

  // Välitetään salattu/kryptattu viesti eteenpäin kaikille solmuille
  socket.on('chat message', (kryptattuViesti) => {
    // Varmistetaan viestin muoto ja koko
    if (typeof kryptattuViesti === 'string' && kryptattuViesti.length <= 10000) {
      io.emit('chat message', kryptattuViesti);
    }
  });

  socket.on('disconnect', () => {
    console.log('QEMU-solmu irtautui:', socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Chat_boxing palvelin käynnissä portissa ${PORT}`);
});