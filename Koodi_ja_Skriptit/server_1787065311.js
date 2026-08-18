const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

app.use(express.json({ limit: '10mb' }));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/api/bot-data', (req, res) => {
  const data = req.body;
  console.log(`[BOT DATA] Sivu: \${data.source_url} | Bannerit: \${data.matched_banners ? data.matched_banners.length : 0} | Popups: \${data.detected_popups_and_overlays ? data.detected_popups_and_overlays.length : 0}`);

  io.emit('bot update', data);
  res.status(200).json({ status: 'ok', message: 'Data vastaanotettu' });
});

function unpackChunk(buffer) {
  const firstPass = zlib.inflateSync(buffer);
  const secondPass = zlib.inflateSync(firstPass);
  return secondPass;
}

app.get('/api/unpacked-packages', (req, res) => {
  const dir = path.resolve('packed_ads_async');
  if (!fs.existsSync(dir)) {
    return res.json([]);
  }

  const files = fs.readdirSync(dir).filter(f => f.endsWith('.pkg'));
  
  const groups = {};
  files.forEach(file => {
    const prefix = file.split('_chunk_')[0];
    if (!groups[prefix]) groups[prefix] = [];
    groups[prefix].push(file);
  });

  const results = [];

  Object.keys(groups).forEach(prefix => {
    const sorted = groups[prefix].sort((a, b) => {
      const idxA = parseInt(a.split('_chunk_')[1]);
      const idxB = parseInt(b.split('_chunk_')[1]);
      return idxA - idxB;
    });

    let combinedBuffers = [];
    sorted.forEach(file => {
      const packedBuffer = fs.readFileSync(path.join(dir, file));
      try {
        const unpacked = unpackChunk(packedBuffer);
        combinedBuffers.push(unpacked);
      } catch (err) {
        console.error(`Virhe purkaessa tiedostoa \${file}:`, err);
      }
    });

    const fullBuffer = Buffer.concat(combinedBuffers);
    try {
      const jsonStr = fullBuffer.toString('utf-8');
      results.push({
        prefix: prefix,
        chunks_count: sorted.length,
        data: JSON.parse(jsonStr)
      });
    } catch (e) {
      console.error(`Pureskeluvirhe ryhmälle \${prefix}`);
    }
  });

  res.json(results);
});

io.on('connection', (socket) => {
  console.log('Käyttäjä liittyi chattiin');

  socket.on('chat message', (msg) => {
    if (typeof msg === 'string' && msg.length <= 5000) {
      io.emit('chat message', msg);
    } else {
      console.log('Ylikokoinen viesti hylätty (yli 5 kt)');
    }
  });

  socket.on('disconnect', () => {
    console.log('Käyttäjä poistui chatista');
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Chat_boxing + Selain-Bot palvelin käynnissä portissa \${PORT}`);
});