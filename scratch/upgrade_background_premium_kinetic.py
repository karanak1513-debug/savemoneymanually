# -*- coding: utf-8 -*-
"""
Upgrades 3D background animation to Ultra-Premium Kinetic Chrome Sculpture:
- Triple Gyroscopic Chrome Rings (Platinum, Electric Cobalt Titanium, Brushed Steel)
- Kinetic Liquid-Mercury Vault Core (pulsing icosahedron sphere)
- Orbiting Wealth Pearls (specular chrome satellite spheres in elliptical orbits)
- 40 ambient shimmering stardust particles
- Dynamic Moving Studio Lights (orbiting Electric Cobalt point light + Ruby Rim light for live moving specular sheen)
- Calibrated radial overlay for stunning visibility while preserving text contrast
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Overlay to allow rich metallic visibility
old_overlay = 'style="background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.45) 0%, rgba(255, 255, 255, 0.82) 75%, rgba(255, 255, 255, 0.96) 100%);"'
new_overlay = 'style="background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.55) 60%, rgba(255, 255, 255, 0.90) 100%);"'

if old_overlay in html:
    html = html.replace(old_overlay, new_overlay, 1)
    print("Updated frosted overlay gradient for rich 3D visibility.")
else:
    print("Warning: old overlay string not matched directly.")

# 2. Replace Three.js Script
marker_start = "  <!-- 3D LUXURY METALLIC PRECISION STUDIO SHADER BACKGROUND SCRIPT -->"
if marker_start not in html:
    marker_start = "<!-- 3D LUXURY METALLIC"

idx_script_start = html.find(marker_start)
if idx_script_start == -1:
    idx_script_start = html.find('initThreeBackground')
    idx_script_start = html.rfind('<!--', 0, idx_script_start)

marker_end = "  <!-- ============================================================ -->\n  <!-- ES6 MODULE JAVASCRIPT: APPLICATION LOGIC"
idx_script_end = html.find(marker_end)
if idx_script_end == -1:
    idx_script_end = html.find('<script type="module">')

new_three_script = """  <!-- ============================================================ -->
  <!-- 3D KINETIC HYPER-CHROME VAULT SCULPTURE & STUDIO SHADER SCRIPT -->
  <!-- ============================================================ -->
  <script>
    (function initThreeBackground() {
      const canvas = document.getElementById('three-bg-canvas');
      if (!canvas || typeof THREE === 'undefined') return;

      const scene = new THREE.Scene();

      // Camera: Cinematic Perspective (38 deg), positioned for majestic depth
      const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 11.0;

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;

      // Master Kinetic Installation Group
      const sculptureGroup = new THREE.Group();
      scene.add(sculptureGroup);

      // Studio Lighting Rig with Live Dynamic Moving Orbiting Lights
      const ambientLight = new THREE.AmbientLight(0xF8FAFC, 1.4);
      scene.add(ambientLight);

      // Orbiting Key 1: Electric Cobalt Blue (casts dynamic gliding blue reflections)
      const cobaltOrbitLight = new THREE.PointLight(0x2563EB, 4.5, 40);
      scene.add(cobaltOrbitLight);

      // Orbiting Key 2: Vivid Crimson / Rose Gold (opposite warm edge reflection)
      const crimsonOrbitLight = new THREE.PointLight(0xE11D48, 2.6, 40);
      scene.add(crimsonOrbitLight);

      // Specular Top Key Light
      const keyStudioLight = new THREE.DirectionalLight(0xFFFFFF, 2.4);
      keyStudioLight.position.set(6, 14, 10);
      scene.add(keyStudioLight);

      // Backlight for edge silhouette
      const backRimLight = new THREE.DirectionalLight(0x93C5FD, 1.2);
      backRimLight.position.set(-8, -10, -8);
      scene.add(backRimLight);

      // ── ULTRA-PREMIUM METALLIC MATERIALS ──────────────────────────
      // Material A: Mirror-Polished Platinum Chrome
      const platinumChromeMat = new THREE.MeshPhysicalMaterial({
        color: 0xE2E8F0,
        metalness: 0.96,
        roughness: 0.08,
        clearcoat: 1.0,
        clearcoatRoughness: 0.06,
        reflectivity: 0.95,
        opacity: 0.88,
        transparent: true,
        wireframe: false
      });

      // Material B: Electric Cobalt Titanium Sheen
      const cobaltTitaniumMat = new THREE.MeshPhysicalMaterial({
        color: 0x3B82F6,
        metalness: 0.92,
        roughness: 0.12,
        clearcoat: 0.95,
        clearcoatRoughness: 0.08,
        opacity: 0.82,
        transparent: true,
        wireframe: false
      });

      // Material C: Liquid Silver Mirror Finish (Inner Core & Satellites)
      const liquidSilverMat = new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        metalness: 0.98,
        roughness: 0.05,
        clearcoat: 1.0,
        clearcoatRoughness: 0.04,
        opacity: 0.92,
        transparent: true,
        wireframe: false
      });

      // ── 1. TRIPLE GYROSCOPIC METALLIC RINGS ───────────────────────
      // Ring 1: Grand Outer Platinum Ring
      const outerRingGeo = new THREE.TorusGeometry(3.6, 0.20, 36, 120);
      const outerRing = new THREE.Mesh(outerRingGeo, platinumChromeMat);
      outerRing.rotation.x = Math.PI / 3.8;
      sculptureGroup.add(outerRing);

      // Ring 2: Intermediate Cobalt Titanium Counter-Ring
      const midRingGeo = new THREE.TorusGeometry(2.7, 0.16, 36, 100);
      const midRing = new THREE.Mesh(midRingGeo, cobaltTitaniumMat);
      midRing.rotation.y = Math.PI / 2.5;
      midRing.rotation.x = -Math.PI / 4.2;
      sculptureGroup.add(midRing);

      // Ring 3: Inner Fast-Gyroscopic Titanium Ring
      const innerRingGeo = new THREE.TorusGeometry(1.85, 0.12, 32, 80);
      const innerRing = new THREE.Mesh(innerRingGeo, platinumChromeMat);
      innerRing.rotation.z = Math.PI / 3;
      sculptureGroup.add(innerRing);

      // ── 2. CENTRAL KINETIC "VAULT CORE" (LIQUID MERCURY) ─────────
      const coreGeo = new THREE.IcosahedronGeometry(0.92, 4);
      const vaultCore = new THREE.Mesh(coreGeo, liquidSilverMat);
      sculptureGroup.add(vaultCore);

      // ── 3. ORBITING WEALTH PEARLS (SATELLITE CHROME SPHERES) ─────
      const pearls = [];
      const pearlGeo = new THREE.SphereGeometry(0.18, 24, 24);
      const pearlConfigs = [
        { radius: 2.2, speed: 1.2, phase: 0, tilt: 0.3 },
        { radius: 3.1, speed: 0.85, phase: Math.PI * 0.6, tilt: -0.5 },
        { radius: 4.1, speed: 0.6, phase: Math.PI * 1.3, tilt: 0.8 },
        { radius: 1.5, speed: 1.6, phase: Math.PI * 1.8, tilt: -0.2 }
      ];

      pearlConfigs.forEach(cfg => {
        const pearlMesh = new THREE.Mesh(pearlGeo, liquidSilverMat);
        sculptureGroup.add(pearlMesh);
        pearls.push({ mesh: pearlMesh, ...cfg });
      });

      // ── 4. FLOATING SPARKS & DIAMOND PARTICLES ───────────────────
      const sparkCount = 45;
      const sparkGeo = new THREE.BufferGeometry();
      const sparkPositions = new Float32Array(sparkCount * 3);
      for (let i = 0; i < sparkCount * 3; i += 3) {
        sparkPositions[i] = (Math.random() - 0.5) * 20;
        sparkPositions[i + 1] = (Math.random() - 0.5) * 14;
        sparkPositions[i + 2] = (Math.random() - 0.5) * 10;
      }
      sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPositions, 3));
      const sparkMat = new THREE.PointsMaterial({
        color: 0x93C5FD,
        size: 0.10,
        transparent: true,
        opacity: 0.70
      });
      const sparkPoints = new THREE.Points(sparkGeo, sparkMat);
      scene.add(sparkPoints);

      // ── 5. INTERACTION & PARALLAX TRACKING ───────────────────────
      let targetRotX = 0;
      let targetRotY = 0;
      let curRotX = 0;
      let curRotY = 0;

      window.addEventListener('pointermove', (e) => {
        const normX = (e.clientX / window.innerWidth) * 2 - 1;
        const normY = -(e.clientY / window.innerHeight) * 2 + 1;
        targetRotY = normX * 0.40;
        targetRotX = -normY * 0.28;
      }, { passive: true });

      window.addEventListener('deviceorientation', (e) => {
        if (e.beta !== null && e.gamma !== null) {
          targetRotX = (e.beta - 45) * 0.005;
          targetRotY = e.gamma * 0.007;
        }
      }, { passive: true });

      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }, { passive: true });

      // ── 6. ANIMATION RENDER LOOP ─────────────────────────────────
      let clock = new THREE.Clock();

      function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Organic Floating Bob
        sculptureGroup.position.y = Math.sin(elapsedTime * 0.9) * 0.30;

        // Dynamic Moving Studio Lighting (creates gliding specular chrome gleam)
        cobaltOrbitLight.position.x = Math.cos(elapsedTime * 0.75) * 9.5;
        cobaltOrbitLight.position.y = Math.sin(elapsedTime * 0.55) * 6.0 + 2.0;
        cobaltOrbitLight.position.z = Math.sin(elapsedTime * 0.75) * 8.0;

        crimsonOrbitLight.position.x = Math.sin(elapsedTime * 0.65) * -9.5;
        crimsonOrbitLight.position.y = Math.cos(elapsedTime * 0.45) * -5.0 - 1.5;
        crimsonOrbitLight.position.z = Math.cos(elapsedTime * 0.65) * 7.5;

        // Gyroscopic Counter-Rotations
        outerRing.rotation.x += 0.0022;
        outerRing.rotation.y += 0.0032;

        midRing.rotation.y -= 0.0036;
        midRing.rotation.z += 0.0018;

        innerRing.rotation.x -= 0.0028;
        innerRing.rotation.z -= 0.0032;

        // Vault Core Pulse & Spin
        vaultCore.rotation.y += 0.007;
        vaultCore.rotation.x += 0.005;
        const corePulse = 1.0 + Math.sin(elapsedTime * 1.8) * 0.06;
        vaultCore.scale.set(corePulse, corePulse, corePulse);

        // Orbiting Wealth Pearls
        pearls.forEach(p => {
          const angle = elapsedTime * p.speed + p.phase;
          p.mesh.position.x = Math.cos(angle) * p.radius;
          p.mesh.position.z = Math.sin(angle) * p.radius;
          p.mesh.position.y = Math.sin(angle * 1.5 + p.tilt) * (p.radius * 0.42);
        });

        // Slow drifting star sparks
        sparkPoints.rotation.y = elapsedTime * 0.025;
        sparkPoints.rotation.x = elapsedTime * 0.015;

        // Damped Cursor Tilt Parallax with smooth lerp
        curRotX += (targetRotX - curRotX) * 0.04;
        curRotY += (targetRotY - curRotY) * 0.04;
        sculptureGroup.rotation.x = curRotX;
        sculptureGroup.rotation.y = curRotY;

        renderer.render(scene, camera);
      }
      animate();
    })();
  </script>

"""

html = html[:idx_script_start] + new_three_script + html[idx_script_end:]
print("Replaced Three.js background script with Kinetic Hyper-Chrome Vault Sculpture.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Length:", len(html))
