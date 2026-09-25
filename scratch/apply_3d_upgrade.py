# -*- coding: utf-8 -*-
"""
Applies the 3D Background Engine Upgrade: Luxury Metallic Precision.
- Replaces wireframe mesh with dual interlocking Smooth Polished Metallic Torus Rings (THREE.TorusGeometry(3.2, 0.28, 32, 100))
- Sets THREE.MeshPhysicalMaterial: Platinum White / Silver Slate (0xCBD5E1), roughness 0.15, metalness 0.85, clearcoat 0.9, transmission 0.1, opacity 0.22, transparent true, wireframe false
- Studio Lighting: Soft White Ambient (0xF8FAFC, 1.2), Directional Electric Cobalt Blue (0x2563EB, 2.5), Directional Crimson Ruby (0xE11D48, 0.8), Key Specular Light (0xFFFFFF, 1.2)
- Camera & Motion: THREE.PerspectiveCamera(40, ...), dual axes drift (0.0015 / 0.0020), damped mouse parallax lerping (0.03)
- Frosted radial gradient overlay with pointer-events: none, z-index: 0
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Canvas DOM element with frosted radial overlay
old_canvas_pattern = r'<canvas id="three-bg-canvas"[^>]*></canvas>'
new_canvas_block = '''<canvas id="three-bg-canvas" class="fixed inset-0 w-full h-full pointer-events-none z-0"></canvas>
  <!-- Subtle radial frosted gradient overlay to ensure 3D chrome stays soft and text remains 100% legible -->
  <div id="three-bg-overlay" class="fixed inset-0 w-full h-full pointer-events-none z-0" style="background: radial-gradient(circle at 50% 45%, rgba(255, 255, 255, 0.45) 0%, rgba(255, 255, 255, 0.82) 75%, rgba(255, 255, 255, 0.96) 100%);"></div>'''

if re.search(old_canvas_pattern, html):
    html = re.sub(old_canvas_pattern, new_canvas_block, html, count=1)
    print("Canvas and frosted overlay updated in DOM.")
else:
    print("Warning: old canvas pattern not matched.")

# 2. Replace Three.js background script
# Locate start of the 3D script block
script_marker = "initThreeBackground"
idx_fn = html.find(script_marker)
if idx_fn != -1:
    # Find the <script> opening tag preceding initThreeBackground
    idx_script_open = html.rfind('<script', 0, idx_fn)
    # Find the comment block preceding that script tag
    idx_block_start = html.rfind('<!-- ===', 0, idx_script_open)
    if idx_block_start == -1:
        idx_block_start = idx_script_open

    # Find the closing </script> tag
    idx_script_close = html.find('</script>', idx_fn) + len('</script>')
    
    new_script_code = """<!-- ============================================================ -->
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

      // 4. Studio Specular Key Light for high-gloss reflection
      const keyLight = new THREE.DirectionalLight(0xFFFFFF, 1.2);
      keyLight.position.set(0, 15, 10);
      scene.add(keyLight);

      // Interactive Group for dual interlocking rings and mouse parallax
      const luxuryGroup = new THREE.Group();
      scene.add(luxuryGroup);

      // Luxury Material: MeshPhysicalMaterial with Platinum White / Silver Slate sheen
      const metallicMaterial = new THREE.MeshPhysicalMaterial({
        color: 0xCBD5E1,          // Platinum White / Silver Slate
        roughness: 0.15,          // High-gloss reflective sheen
        metalness: 0.85,          // Luxury brushed chrome finish
        clearcoat: 0.9,           // Gloss clearcoat layer
        clearcoatRoughness: 0.1,
        transmission: 0.1,        // Ultra-subtle light transmittance
        opacity: 0.22,            // Delicate studio presence
        transparent: true,
        wireframe: false          // Solid smooth luxury chrome (NO wireframe)
      });

      // Precision Ring Geometry: THREE.TorusGeometry(3.2, 0.28, 32, 100)
      const torusGeo = new THREE.TorusGeometry(3.2, 0.28, 32, 100);

      // Ring 1: Primary Precision Torus Ring
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

        // Autonomous Motion: Slowly rotate the metallic rings on dual axes at ultra-low drift speed
        ring1.rotation.x += 0.0015;
        ring1.rotation.y += 0.0020;

        ring2.rotation.y += 0.0018;
        ring2.rotation.z += 0.0012;

        // Damped Mouse Parallax: Softly tilt based on cursor coordinates with smooth lerping (factor: 0.03)
        curRotX += (targetRotX - curRotX) * 0.03;
        curRotY += (targetRotY - curRotY) * 0.03;

        luxuryGroup.rotation.x = curRotX;
        luxuryGroup.rotation.y = curRotY;

        renderer.render(scene, camera);
      }
      animate();
    })();
  </script>"""

    html = html[:idx_block_start] + new_script_code + html[idx_script_close:]
    print("Replaced Three.js background script with Luxury Metallic Studio Shader.")
else:
    print("Error: Could not find Three.js script block.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully! Length:", len(html))
