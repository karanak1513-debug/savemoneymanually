import fs from 'node:fs';
import zlib from 'node:zlib';

function createPNG(size, drawPixelFn) {
  const width = size;
  const height = size;
  
  // Raw scanlines: each line starts with filter byte 0
  const rowSize = 1 + width * 4;
  const rawData = Buffer.alloc(rowSize * height);
  
  for (let y = 0; y < height; y++) {
    const rowOffset = y * rowSize;
    rawData[rowOffset] = 0; // Filter None
    for (let x = 0; x < width; x++) {
      const [r, g, b, a] = drawPixelFn(x, y, width, height);
      const pxOffset = rowOffset + 1 + x * 4;
      rawData[pxOffset] = r;
      rawData[pxOffset + 1] = g;
      rawData[pxOffset + 2] = b;
      rawData[pxOffset + 3] = a;
    }
  }

  const deflated = zlib.deflateSync(rawData);

  // CRC32 calculation
  const crcTable = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    }
    crcTable[n] = c;
  }
  function calcCRC(buf) {
    let c = 0xffffffff;
    for (let i = 0; i < buf.length; i++) {
      c = crcTable[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
    }
    return (c ^ 0xffffffff) >>> 0;
  }

  function makeChunk(typeStr, dataBuf) {
    const typeBuf = Buffer.from(typeStr, 'ascii');
    const lenBuf = Buffer.alloc(4);
    lenBuf.writeUInt32BE(dataBuf.length, 0);

    const crcInput = Buffer.concat([typeBuf, dataBuf]);
    const crcVal = calcCRC(crcInput);
    const crcBuf = Buffer.alloc(4);
    crcBuf.writeUInt32BE(crcVal, 0);

    return Buffer.concat([lenBuf, typeBuf, dataBuf, crcBuf]);
  }

  // PNG Signature
  const sig = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);

  // IHDR chunk
  const ihdrData = Buffer.alloc(13);
  ihdrData.writeUInt32BE(width, 0);
  ihdrData.writeUInt32BE(height, 4);
  ihdrData[8] = 8; // Bit depth: 8
  ihdrData[9] = 6; // Color type: 6 (RGBA)
  ihdrData[10] = 0; // Compression: 0 (deflate)
  ihdrData[11] = 0; // Filter: 0
  ihdrData[12] = 0; // Interlace: 0
  const ihdrChunk = makeChunk('IHDR', ihdrData);

  // IDAT chunk
  const idatChunk = makeChunk('IDAT', deflated);

  // IEND chunk
  const iendChunk = makeChunk('IEND', Buffer.alloc(0));

  return Buffer.concat([sig, ihdrChunk, idatChunk, iendChunk]);
}

// Draw brand shield logo
function brandPixel(x, y, width, height) {
  const nx = (x + 0.5) / width;  // 0 to 1
  const ny = (y + 0.5) / height; // 0 to 1

  // Rounded rectangle check for badge background
  const cornerR = 0.22;
  const inBadge = (nx >= 0.05 && nx <= 0.95 && ny >= 0.05 && ny <= 0.95);
  let distToCorner = 0;
  const cx = nx < 0.5 ? 0.05 + cornerR : 0.95 - cornerR;
  const cy = ny < 0.5 ? 0.05 + cornerR : 0.95 - cornerR;
  const isCorner = (nx < cx && ny < cy) || (nx > cx && ny < cy) || (nx < cx && ny > cy) || (nx > cx && ny > cy);
  if (isCorner) {
    distToCorner = Math.hypot(nx - cx, ny - cy);
    if (distToCorner > cornerR) return [0, 0, 0, 0]; // Transparent outside squircle
  }

  // Gradient background: Cobalt #2563EB to Deep Blue #1D4ED8
  const gradT = (nx + ny) / 2;
  const bgR = Math.round(37 + (29 - 37) * gradT);
  const bgG = Math.round(99 + (78 - 99) * gradT);
  const bgB = Math.round(235 + (216 - 235) * gradT);

  // Center Shield coordinates (normalized)
  const sx = (nx - 0.5) * 2; // -1 to 1
  const sy = ny; // 0 to 1

  // Shield boundary function:
  // Top: sy >= 0.22
  // Sides: |sx| <= 0.65 for sy between 0.22 and 0.45
  // Bottom taper: below sy 0.45, curve to (0, 0.82)
  let inShield = false;
  let inShieldBorder = false;

  const topY = 0.22;
  const midY = 0.46;
  const botY = 0.82;
  const maxW = 0.62;

  if (sy >= topY && sy <= botY) {
    let allowedW = maxW;
    if (sy > midY) {
      const t = (sy - midY) / (botY - midY);
      allowedW = maxW * (1 - Math.pow(t, 1.4));
    }
    const distW = Math.abs(sx);
    if (distW <= allowedW) {
      inShield = true;
      if (distW >= allowedW - 0.12 || sy <= topY + 0.07 || sy >= botY - 0.07) {
        inShieldBorder = true;
      }
    }
  }

  // Central circle vault
  const vaultDist = Math.hypot(sx, (sy - 0.46) * 2);
  const inVault = vaultDist <= 0.22;
  const inVaultRing = vaultDist >= 0.12 && vaultDist <= 0.22;

  if (inShieldBorder || inVaultRing) {
    return [255, 255, 255, 255]; // Crisp white emblem
  }

  if (inVault) {
    return [255, 255, 255, 220];
  }

  if (inShield) {
    // Subtle shield inner fill (slightly lighter/translucent)
    return [
      Math.min(255, bgR + 35),
      Math.min(255, bgG + 35),
      Math.min(255, bgB + 20),
      255
    ];
  }

  return [bgR, bgG, bgB, 255];
}

// Generate PNGs
const png16 = createPNG(16, brandPixel);
const png32 = createPNG(32, brandPixel);
const png192 = createPNG(192, brandPixel);

fs.writeFileSync('favicon-16x16.png', png16);
fs.writeFileSync('favicon-32x32.png', png32);
fs.writeFileSync('apple-touch-icon.png', png192);

// Generate valid ICO containing 16x16 and 32x32 PNGs
function createICO(images) {
  // images: array of { width, height, buffer }
  const count = images.length;
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0); // reserved
  header.writeUInt16LE(1, 2); // ICO type
  header.writeUInt16LE(count, 4); // count

  let offset = 6 + count * 16;
  const entries = [];
  const bodies = [];

  for (const img of images) {
    const entry = Buffer.alloc(16);
    entry.writeUInt8(img.width >= 256 ? 0 : img.width, 0);
    entry.writeUInt8(img.height >= 256 ? 0 : img.height, 1);
    entry.writeUInt8(0, 2); // color count
    entry.writeUInt8(0, 3); // reserved
    entry.writeUInt16LE(1, 4); // color planes
    entry.writeUInt16LE(32, 6); // bpp
    entry.writeUInt32LE(img.buffer.length, 8); // size
    entry.writeUInt32LE(offset, 12); // offset

    entries.push(entry);
    bodies.push(img.buffer);
    offset += img.buffer.length;
  }

  return Buffer.concat([header, ...entries, ...bodies]);
}

const icoBuf = createICO([
  { width: 16, height: 16, buffer: png16 },
  { width: 32, height: 32, buffer: png32 }
]);

fs.writeFileSync('favicon.ico', icoBuf);
console.log('Successfully generated favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png!');
