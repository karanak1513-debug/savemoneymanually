# -*- coding: utf-8 -*-
"""
Upgrades 3D background to Luxury Metallic Precision:
1. Deletes wireframe TorusKnot completely.
2. Renders dual interlocking Smooth Polished Metallic Torus Rings (THREE.TorusGeometry(3.2, 0.28, 32, 100)).
3. High-gloss reflective sheen & brushed chrome material:
   THREE.MeshPhysicalMaterial:
   color: 0xCBD5E1 (Platinum White / Silver Slate)
   roughness: 0.15
   metalness: 0.85
   clearcoat: 0.9
   transmission: 0.1
   opacity: 0.22
   transparent: true
4. Studio Lighting Rig:
   Ambient Light: Soft White (0xF8FAFC, intensity: 1.2)
   Directional Accent 1: Electric Cobalt Blue (0x2563EB, intensity: 2.5) top-left
   Directional Accent 2: Crimson Ruby (0xE11D48, intensity: 0.8) bottom-right
5. Camera & Interactive Motion:
   THREE.PerspectiveCamera(40, ...)
   Dual axes drift: rotation.x += 0.0015, rotation.y += 0.002
   Damped mouse parallax with smooth lerping (factor: 0.03)
6. Canvas overlay with subtle radial frosted gradient for legibility & pointer-events: none
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Canvas in DOM with frosted radial blend overlay
old_canvas_block = '  <!-- Interactive Three.js Background Canvas -->\n  <canvas id="three-bg-canvas" class="fixed inset-0 w-full h-full pointer-events-none z-0"></canvas>'
new_canvas_block = """  <!-- 3D Luxury Metallic Studio Background Canvas -->
  <canvas id="three-bg-canvas" class="fixed inset-0 w-full h-full pointer-events-none z-0"></canvas>
  <div id="three-bg-overlay" class="fixed inset-0 w-full h-full pointer-events-none z-0" style="background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.45) 0%, rgba(255, 255, 255, 0.82) 75%, rgba(255, 255, 255, 0.96) 100%);"></div>"""

if old_canvas_block in html:
    html = html.replace(old_canvas_block, new_canvas_block)
    print("Updated canvas DOM with frosted gradient overlay.")
else:
    # Alternative match
    idx_canv = html.find('<canvas id="three-bg-canvas"')
    if idx_canv != -1:
        end_canv = html.find('>', idx_canv) + 1
        html = html[:idx_canv] + '<canvas id="three-bg-canvas" class="fixed inset-0 w-full h-full pointer-events-none z-0"></canvas>\n  <div id="three-bg-overlay" class="fixed inset-0 w-full h-full pointer-events-none z-0" style="background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.45) 0%, rgba(255, 255, 255, 0.82) 75%, rgba(255, 255, 255, 0.96) 100%);"></div>' + html[end_canv:]
        print("Updated canvas DOM via fallback.")

# 2. Replace Three.js script block with the luxury metallic studio shader
idx_script_start = html.find('<!-- 3D INTERACTIVE THREE.JS BACKGROUND SCRIPT')
if idx_script_start == -1:
    idx_script_start = html.find('(function initThreeBackground()')
    idx_script_start = html.rfind('<!--', 0, idx_script_start)

idx_script_end = html.find('<!-- ============================================================ -->\n  <!-- ES6 MODULE JAVASCRIPT: APPLICATION LOGIC')
if idx_script_end == -1:
    idx_script_end = html.find('<script type="module">')

new_metallic_script = """<!-- ============================================================ -->
  <!-- 3D LUXURY METALLIC PRECISION STUDIO SHADER BACKGROUND SCRIPT -->
  <!-- ============================================================ -->
  <script>
    (function initThreeBackground() {
      const canvas = document.getElementById('three-bg-canvas');
      if (!canvas || typeof THREE === 'undefined') return;

      const scene = new THREE.Scene();

      // Camera: Subtle perspective (40 deg), centered behind content layer
      const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 11.5;

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.05;

      // Studio Lighting Rig
      // 1. Soft White Ambient Light
      const ambientLight = new THREE.AmbientLight(0xF8FAFC, 1.2);
      scene.add(ambientLight);

      // 2. Directional Accent Light 1: Electric Cobalt Blue (top-left for subtle blue metallic rim reflections)
      const dirLight1 = new THREE.DirectionalLight(0x2563EB, 2.5);
      dirLight1.position.set(-12, 14, 10);
      scene.add(dirLight1);

      // 3. Directional Accent Light 2: Crimson Ruby (bottom-right for microscopic warm metallic highlight)
      const dirLight2 = new THREE.DirectionalLight(0xE11D48, 0.8);
      dirLight2.position.set(12, -10, 8);
      scene.add(dirLight2);

      // 4. Pure white specular highlight light
      const topRimLight = new THREE.DirectionalLight(0xFFFFFF, 1.2);
      topRimLight.position.set(0, 16, 8);
      scene.add(topRimLight);

      // Group for dual interlocking rings and mouse parallax
      const luxuryGroup = new THREE.Group();
      scene.add(luxuryGroup);

      // Luxury Material: MeshPhysicalMaterial with Platinum White / Silver Slate sheen
      const metallicMaterial = new THREE.MeshPhysicalMaterial({
        color: 0xCBD5E1,       // Platinum White / Silver Slate
        roughness: 0.15,       // High-gloss reflective sheen
        metalness: 0.85,       // Luxury brushed chrome finish
        clearcoat: 0.9,        // Gloss clearcoat layer
        clearcoatRoughness: 0.1,
        transmission: 0.1,     // Ultra-subtle light transmittance
        opacity: 0.22,         // Delicate studio presence
        transparent: true,
        wireframe: false       // Solid smooth luxury chrome (NO wireframe)
      });

      // Ring 1: Primary Precision Torus Ring
      const torusGeo = new THREE.TorusGeometry(3.2, 0.28, 32, 100);
      const ring1 = new THREE.Mesh(torusGeo, metallicMaterial);
      ring1.rotation.x = Math.PI / 4;
      luxuryGroup.add(ring1);

      // Ring 2: Interlocking Counter-Angle Precision Ring
      const ring2 = new THREE.Mesh(torusGeo, metallicMaterial);
      ring2.rotation.y = Math.PI / 2.8;
      ring2.rotation.x = -Math.PI / 5;
      luxuryGroup.add(ring2);

      // Autonomous Motion & Damped Mouse Parallax Tracking
      let targetRotX = 0;
      let targetRotY = 0;
      let curRotX = 0;
      let curRotY = 0;

      window.addEventListener('pointermove', (e) => {
        const normX = (e.clientX / window.innerWidth) * 2 - 1;
        const normY = -(e.clientY / window.innerHeight) * 2 + 1;
        targetRotY = normX * 0.35;
        targetRotX = -normY * 0.25;
      }, { passive: true });

      window.addEventListener('deviceorientation', (e) => {
        if (e.beta !== null && e.gamma !== null) {
          targetRotX = (e.beta - 45) * 0.004;
          targetRotY = e.gamma * 0.006;
        }
      }, { passive: true });

      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }, { passive: true });

      function animate() {
        requestAnimationFrame(animate);

        // Slowly rotate metallic rings on dual axes at ultra-low drift speed
        ring1.rotation.x += 0.0015;
        ring1.rotation.y += 0.0020;

        ring2.rotation.y += 0.0018;
        ring2.rotation.z += 0.0012;

        // Damped Mouse Parallax with smooth lerping (linear interpolation factor: 0.03)
        curRotX += (targetRotX - curRotX) * 0.03;
        curRotY += (targetRotY - curRotY) * 0.03;

        luxuryGroup.rotation.x = curRotX;
        luxuryGroup.rotation.y = curRotY;

        renderer.render(scene, camera);
      }
      animate();
    })();
  </script>

  """

html = html[:idx_script_start] + new_metallic_script + html[idx_script_end:]
print("Replaced Three.js background script with Luxury Metallic Studio Shader.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Length:", len(html))
