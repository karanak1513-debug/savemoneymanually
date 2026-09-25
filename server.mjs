import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
let PORT = parseInt(process.env.PORT || process.argv[2] || "3001", 10);

const MIME_TYPES = {
  ".html": "text/html; charset=UTF-8",
  ".js": "text/javascript; charset=UTF-8",
  ".mjs": "text/javascript; charset=UTF-8",
  ".css": "text/css; charset=UTF-8",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
};

const server = http.createServer((req, res) => {
  let reqUrl = req.url.split("?")[0];
  let filePath = path.join(__dirname, reqUrl === "/" ? "index.html" : reqUrl);

  // If file doesn't exist, check if it's an /app route or fallback to index.html
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(__dirname, "index.html");
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || "application/octet-stream";

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500, { "Content-Type": "text/plain" });
      res.end("Server Error");
      return;
    }
    res.writeHead(200, {
      "Content-Type": contentType,
      "Access-Control-Allow-Origin": "*",
    });
    res.end(content);
  });
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.log(`Port ${PORT} is busy, trying port ${PORT + 1}...`);
    PORT++;
    server.listen(PORT);
  } else {
    console.error("Server error:", err);
  }
});

server.listen(PORT, () => {
  console.log(`Save Money Manually server running at http://localhost:${PORT}`);
});
