// ============================================================
// VAULT.FI — 3D KINETIC VAULT CORE (HTML5 CANVAS 60FPS)
// High-Performance Gyroscopic Orbital Engine
// ============================================================

export function initVault3DCanvas(canvas) {
  if (!canvas) return { setMode: () => {}, destroy: () => {} };

  const ctx = canvas.getContext("2d", { alpha: true });
  let animationFrameId = null;
  let isDestroyed = false;

  // Visual state modes: 'IDLE' | 'HOVER' | 'AUTHENTICATING' | 'SUCCESS'
  let currentMode = "IDLE";
  let modeSpeedMultiplier = 1.0;
  let targetSpeedMultiplier = 1.0;
  let glowIntensity = 1.0;
  let targetGlowIntensity = 1.0;

  // Viewport & DPI
  let width = 0;
  let height = 0;
  let dpr = window.devicePixelRatio || 1;
  let centerX = 0;
  let centerY = 0;

  // Interactive mouse gyro tilt
  let mouseX = 0;
  let mouseY = 0;
  let gyroX = 0;
  let gyroY = 0;
  let targetGyroX = 0;
  let targetGyroY = 0;

  // Base rotation angles
  let angleX = 0.35;
  let angleY = 0.5;
  let angleZ = 0.2;

  // 3D Projection parameters
  const focalLength = 320;
  const baseRadius = 75;

  // Ambient floating particles
  const particleCount = 42;
  const particles = [];
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: (Math.random() - 0.5) * 260,
      y: (Math.random() - 0.5) * 220,
      z: (Math.random() - 0.5) * 220,
      size: Math.random() * 2.2 + 0.8,
      speedY: -(Math.random() * 0.25 + 0.1),
      phase: Math.random() * Math.PI * 2,
      color: Math.random() > 0.3 ? "#2563EB" : "#10B981",
    });
  }

  // 3D Icosahedron Core Vertices (Golden ratio)
  const phi = (1 + Math.sqrt(5)) / 2;
  const coreScale = baseRadius * 0.48;
  const rawVertices = [
    [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
    [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
    [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1],
  ].map(([x, y, z]) => {
    const len = Math.hypot(x, y, z);
    return [
      (x / len) * coreScale,
      (y / len) * coreScale,
      (z / len) * coreScale,
    ];
  });

  // Icosahedron Edges (30 edges)
  const coreEdges = [];
  for (let i = 0; i < rawVertices.length; i++) {
    for (let j = i + 1; j < rawVertices.length; j++) {
      const d = Math.hypot(
        rawVertices[i][0] - rawVertices[j][0],
        rawVertices[i][1] - rawVertices[j][1],
        rawVertices[i][2] - rawVertices[j][2]
      );
      if (Math.abs(d - (coreScale * 1.05)) < 12) {
        coreEdges.push([i, j]);
      }
    }
  }

  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    centerX = width / 2;
    centerY = height / 2;
  }

  window.addEventListener("resize", resize);
  resize();

  // Mouse tilt tracking
  function onMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / width;
    const y = (e.clientY - rect.top) / height;
    targetGyroX = (y - 0.5) * 0.75;
    targetGyroY = (x - 0.5) * 0.95;
  }

  function onMouseLeave() {
    targetGyroX = 0;
    targetGyroY = 0;
  }

  window.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseleave", onMouseLeave);

  // 3D Math Helper: Rotate point by Euler angles
  function rotate3D(x, y, z, ax, ay, az) {
    // Rotate X
    const cosX = Math.cos(ax), sinX = Math.sin(ax);
    const y1 = y * cosX - z * sinX;
    const z1 = y * sinX + z * cosX;

    // Rotate Y
    const cosY = Math.cos(ay), sinY = Math.sin(ay);
    const x2 = x * cosY + z1 * sinY;
    const z2 = -x * sinY + z1 * cosY;

    // Rotate Z
    const cosZ = Math.cos(az), sinZ = Math.sin(az);
    const x3 = x2 * cosZ - y1 * sinZ;
    const y3 = x2 * sinZ + y1 * cosZ;

    return [x3, y3, z2];
  }

  // Project 3D point to 2D screen
  function project(x, y, z) {
    const scale = focalLength / (focalLength + z);
    return [centerX + x * scale, centerY + y * scale, scale, z];
  }

  // Render a 3D Ring with dashes and node ticks
  function drawGyroscopicRing(radius, tiltX, tiltY, tiltZ, segmentCount, color, tickGlow, dashRatio = 0.6) {
    const pts = [];
    for (let i = 0; i <= segmentCount; i++) {
      const theta = (i / segmentCount) * Math.PI * 2;
      const rx = Math.cos(theta) * radius;
      const rz = Math.sin(theta) * radius;
      const [px, py, pz] = rotate3D(rx, 0, rz, tiltX, tiltY, tiltZ);
      const [sx, sy, sc, zDepth] = project(px, py, pz);
      pts.push({ sx, sy, sc, zDepth, theta });
    }

    // Draw segmented ring segments
    for (let i = 0; i < pts.length - 1; i++) {
      const p1 = pts[i];
      const p2 = pts[i + 1];

      // Depth alpha
      const alpha = Math.max(0.15, Math.min(0.9, 0.45 + (p1.zDepth / (baseRadius * 2.5)) * 0.4));
      ctx.beginPath();
      ctx.moveTo(p1.sx, p1.sy);
      ctx.lineTo(p2.sx, p2.sy);

      ctx.strokeStyle = color.replace("ALPHA", (alpha * glowIntensity).toFixed(2));
      ctx.lineWidth = Math.max(1, (1.6 * p1.sc));
      ctx.stroke();

      // Node ticks on every 4th segment
      if (i % 4 === 0) {
        ctx.beginPath();
        ctx.arc(p1.sx, p1.sy, Math.max(1.5, 2.5 * p1.sc), 0, Math.PI * 2);
        ctx.fillStyle = tickGlow.replace("ALPHA", (alpha * 1.2 * glowIntensity).toFixed(2));
        ctx.fill();
      }
    }
  }

  // Animation Loop
  let lastTime = performance.now();

  function render(now) {
    if (isDestroyed) return;

    const delta = Math.min((now - lastTime) / 1000, 0.1);
    lastTime = now;

    // Smooth mode transition
    modeSpeedMultiplier += (targetSpeedMultiplier - modeSpeedMultiplier) * 0.08;
    glowIntensity += (targetGlowIntensity - glowIntensity) * 0.08;

    // Gyro damping
    gyroX += (targetGyroX - gyroX) * 0.06;
    gyroY += (targetGyroY - gyroY) * 0.06;

    // Update rotation angles with subtle natural drift
    angleX += 0.35 * delta * modeSpeedMultiplier;
    angleY += 0.48 * delta * modeSpeedMultiplier;
    angleZ += 0.22 * delta * modeSpeedMultiplier;

    const effAngleX = angleX + gyroX;
    const effAngleY = angleY + gyroY;

    // Clear Canvas with crisp alpha
    ctx.clearRect(0, 0, width, height);

    // 1. Ambient Central Core Halo / Radiant Gradient
    const haloRadius = baseRadius * 1.5 * glowIntensity;
    const haloGrad = ctx.createRadialGradient(
      centerX, centerY, 0,
      centerX, centerY, haloRadius
    );
    if (currentMode === "SUCCESS") {
      haloGrad.addColorStop(0, "rgba(16, 185, 129, 0.22)");
      haloGrad.addColorStop(0.5, "rgba(16, 185, 129, 0.06)");
      haloGrad.addColorStop(1, "rgba(16, 185, 129, 0)");
    } else {
      haloGrad.addColorStop(0, "rgba(37, 99, 235, 0.18)");
      haloGrad.addColorStop(0.5, "rgba(59, 130, 246, 0.05)");
      haloGrad.addColorStop(1, "rgba(37, 99, 235, 0)");
    }
    ctx.fillStyle = haloGrad;
    ctx.fillRect(0, 0, width, height);

    // 2. Ambient Floating Node Particles
    particles.forEach((p) => {
      p.y += p.speedY;
      if (p.y < -130) p.y = 130;

      const [px, py, pz] = rotate3D(p.x, p.y, p.z, effAngleX * 0.3, effAngleY * 0.3, 0);
      const [sx, sy, sc, zDepth] = project(px, py, pz);

      const pAlpha = Math.max(0.1, Math.min(0.85, 0.45 + (zDepth / 220) * 0.4));
      ctx.beginPath();
      ctx.arc(sx, sy, p.size * sc, 0, Math.PI * 2);
      ctx.fillStyle = p.color === "#2563EB"
        ? `rgba(37, 99, 235, ${(pAlpha * glowIntensity * 0.7).toFixed(2)})`
        : `rgba(16, 185, 129, ${(pAlpha * glowIntensity * 0.8).toFixed(2)})`;
      ctx.fill();
    });

    // 3. Outer Gyroscopic Orbital Track (Equatorial Orbit)
    drawGyroscopicRing(
      baseRadius * 1.28,
      effAngleX,
      effAngleY,
      angleZ * 0.5,
      48,
      "rgba(37, 99, 235, ALPHA)",
      "rgba(59, 130, 246, ALPHA)"
    );

    // 4. Middle Gyroscopic Orbital Track (Inclined Orbit)
    drawGyroscopicRing(
      baseRadius * 1.05,
      effAngleX + 0.85,
      -effAngleY * 1.1,
      angleZ * 0.8,
      40,
      "rgba(30, 64, 175, ALPHA)",
      "rgba(37, 99, 235, ALPHA)"
    );

    // 5. Inner Fast Ring (Vertical Meridian Track)
    drawGyroscopicRing(
      baseRadius * 0.82,
      -effAngleX * 1.2,
      effAngleY * 0.9 + 1.2,
      -angleZ * 1.2,
      32,
      currentMode === "SUCCESS" ? "rgba(16, 185, 129, ALPHA)" : "rgba(37, 99, 235, ALPHA)",
      currentMode === "SUCCESS" ? "rgba(5, 150, 105, ALPHA)" : "rgba(96, 165, 250, ALPHA)"
    );

    // 6. Central 3D Kinetic Geometric Vault Core (Icosahedron)
    const projectedVertices = rawVertices.map(([vx, vy, vz]) => {
      // Internal counter-spin
      const [rx, ry, rz] = rotate3D(vx, vy, vz, -effAngleX * 0.8, -effAngleY * 1.2, angleZ);
      return project(rx, ry, rz);
    });

    // Draw Icosahedron Edges with depth-weighted strokes
    coreEdges.forEach(([i, j]) => {
      const v1 = projectedVertices[i];
      const v2 = projectedVertices[j];
      const avgZ = (v1[3] + v2[3]) / 2;
      const edgeAlpha = Math.max(0.2, Math.min(1.0, 0.55 + (avgZ / (coreScale * 2)) * 0.45));

      ctx.beginPath();
      ctx.moveTo(v1[0], v1[1]);
      ctx.lineTo(v2[0], v2[1]);
      ctx.strokeStyle = currentMode === "SUCCESS"
        ? `rgba(16, 185, 129, ${(edgeAlpha * glowIntensity).toFixed(2)})`
        : `rgba(37, 99, 235, ${(edgeAlpha * glowIntensity).toFixed(2)})`;
      ctx.lineWidth = Math.max(1.2, 1.8 * ((v1[2] + v2[2]) / 2));
      ctx.stroke();
    });

    // Draw Core Vertex Glow Nodes
    projectedVertices.forEach(([sx, sy, sc, zDepth]) => {
      const vAlpha = Math.max(0.3, Math.min(1.0, 0.6 + (zDepth / (coreScale * 2)) * 0.4));
      ctx.beginPath();
      ctx.arc(sx, sy, Math.max(1.8, 3.2 * sc), 0, Math.PI * 2);
      ctx.fillStyle = currentMode === "SUCCESS"
        ? `rgba(16, 185, 129, ${(vAlpha * glowIntensity).toFixed(2)})`
        : `rgba(96, 165, 250, ${(vAlpha * glowIntensity).toFixed(2)})`;
      ctx.fill();
    });

    // 7. Central Radiant Vault Nucleus
    const nucleusSize = Math.max(3, 5.5 + Math.sin(now * 0.003) * 1.5);
    const nucleusGrad = ctx.createRadialGradient(
      centerX, centerY, 0,
      centerX, centerY, nucleusSize * 2.5
    );
    if (currentMode === "SUCCESS") {
      nucleusGrad.addColorStop(0, "#10B981");
      nucleusGrad.addColorStop(0.4, "rgba(16, 185, 129, 0.8)");
      nucleusGrad.addColorStop(1, "rgba(16, 185, 129, 0)");
    } else {
      nucleusGrad.addColorStop(0, "#2563EB");
      nucleusGrad.addColorStop(0.4, "rgba(59, 130, 246, 0.8)");
      nucleusGrad.addColorStop(1, "rgba(37, 99, 235, 0)");
    }
    ctx.beginPath();
    ctx.arc(centerX, centerY, nucleusSize * 2.5, 0, Math.PI * 2);
    ctx.fillStyle = nucleusGrad;
    ctx.fill();

    animationFrameId = requestAnimationFrame(render);
  }

  animationFrameId = requestAnimationFrame(render);

  return {
    setMode(mode) {
      currentMode = mode;
      if (mode === "HOVER") {
        targetSpeedMultiplier = 2.4;
        targetGlowIntensity = 1.35;
      } else if (mode === "AUTHENTICATING") {
        targetSpeedMultiplier = 4.2;
        targetGlowIntensity = 1.6;
      } else if (mode === "SUCCESS") {
        targetSpeedMultiplier = 1.2;
        targetGlowIntensity = 1.25;
      } else {
        // IDLE
        targetSpeedMultiplier = 1.0;
        targetGlowIntensity = 1.0;
      }
    },
    destroy() {
      isDestroyed = true;
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseleave", onMouseLeave);
    },
  };
}
