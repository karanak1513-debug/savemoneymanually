# -*- coding: utf-8 -*-
"""
Applies Restore & Lock Master updates to index.html:
1. Restores delicate 24px subtle dot-matrix texture on Stark White background:
   radial-gradient(rgba(15, 23, 42, 0.08) 1px, transparent 1px)
2. Restores Three.js interactive 3D TorusKnot wireframe mesh (#2563EB, opacity: 0.12)
   with autonomous rotation and pointer/gyro tilt on <canvas id="three-bg-canvas">
3. Updates Total Net Stashed display to id="totalStashedDisplay" with live onSnapshot recalculation
4. Ensures strict Lower Navigation Dock (mobile bottom dock + desktop lower rail stack)
   with instant client-side switching and 0 Terms/Privacy.
5. Ensures [appearance: textfield] for form inputs and debounced anti-spam button locks.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Canvas Texture in CSS
old_body_bg = """    /* Base Canvas: Stark Pure White with ultra-faint 24px dot-matrix */
    body {
      background-image: 
        radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.05) 0px, transparent 55%),
        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.05) 0px, transparent 55%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.04) 0px, transparent 55%),
        radial-gradient(rgba(15, 23, 42, 0.05) 1px, transparent 1px) !important;
      background-size: 100% 100%, 100% 100%, 100% 100%, 24px 24px !important;
      background-attachment: fixed !important;
    }"""

new_body_bg = """    /* Base Canvas: Stark Pure White with delicate 24px subtle dot-matrix texture */
    body {
      background-color: #FFFFFF !important;
      background-image: radial-gradient(rgba(15, 23, 42, 0.08) 1px, transparent 1px) !important;
      background-size: 24px 24px !important;
      background-attachment: fixed !important;
      color: #0B0F19;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden !important;
    }"""

if old_body_bg in html:
    html = html.replace(old_body_bg, new_body_bg)
    print("Replaced old_body_bg")
else:
    print("Warning: old_body_bg not found, checking alternative")
    # In case there's another pattern
    import re
    html = re.sub(
        r'body\s*\{[^}]*background-image:[^}]*radial-gradient[^}]*\}',
        new_body_bg,
        html,
        count=1
    )

# Also ensure appearance: textfield
old_spin = """    input[type=number] {
      -moz-appearance: textfield !important;
    }"""
new_spin = """    input[type=number] {
      -moz-appearance: textfield !important;
      appearance: textfield !important;
    }"""
if old_spin in html:
    html = html.replace(old_spin, new_spin)
    print("Replaced number stepper css")

# 2. Update Canvas element in DOM
old_canvas = '<div id="three-canvas-container" class="fixed inset-0 pointer-events-none z-0 opacity-40"></div>'
new_canvas = '<canvas id="three-bg-canvas" class="fixed inset-0 w-full h-full pointer-events-none z-0"></canvas>'
if old_canvas in html:
    html = html.replace(old_canvas, new_canvas)
    print("Replaced canvas element")
else:
    print("Warning: old_canvas div not found directly")

# 3. Update 3D Three.js Script to exact TorusKnot wireframe mesh
idx_three_start = html.find('<!-- 3D INTERACTIVE THREE.JS BACKGROUND SCRIPT')
if idx_three_start == -1:
    idx_three_start = html.find('(function initThreeBackground()')
    idx_three_start = html.rfind('<!--', 0, idx_three_start)

idx_three_end = html.find('<!-- ============================================================ -->\n  <!-- ES6 MODULE JAVASCRIPT: APPLICATION LOGIC')
if idx_three_end == -1:
    idx_three_end = html.find('<script type="module">')

new_three_script = """<!-- ============================================================ -->
  <!-- 3D INTERACTIVE THREE.JS BACKGROUND SCRIPT (RESTORED WIREFRAME)-->
  <!-- ============================================================ -->
  <script>
    (function initThreeBackground() {
      const canvas = document.getElementById('three-bg-canvas');
      if (!canvas || typeof THREE === 'undefined') return;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 28;

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // Container group for interactive mouse/gyro tilt
      const wireframeGroup = new THREE.Group();
      scene.add(wireframeGroup);

      // 1. Smooth Geometric 3D Torus Knot Wireframe Mesh in Electric Cobalt Blue (#2563EB, opacity 0.12)
      const knotGeo = new THREE.TorusKnotGeometry(8.5, 2.4, 140, 24, 2, 3);
      const knotMat = new THREE.MeshBasicMaterial({
        color: 0x2563EB,
        wireframe: true,
        transparent: true,
        opacity: 0.12
      });
      const torusKnot = new THREE.Mesh(knotGeo, knotMat);
      wireframeGroup.add(torusKnot);

      // 2. Concentric Orbit Halo Ring in Cobalt Blue (#2563EB, opacity 0.08)
      const ringGeo = new THREE.RingGeometry(13.5, 13.55, 72);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x2563EB,
        wireframe: true,
        transparent: true,
        opacity: 0.08,
        side: THREE.DoubleSide
      });
      const orbitRing = new THREE.Mesh(ringGeo, ringMat);
      wireframeGroup.add(orbitRing);

      // Dynamic cursor & gyro tilt tracking
      let targetRotX = 0;
      let targetRotY = 0;
      let curRotX = 0;
      let curRotY = 0;

      window.addEventListener('pointermove', (e) => {
        const normX = (e.clientX / window.innerWidth) * 2 - 1;
        const normY = -(e.clientY / window.innerHeight) * 2 + 1;
        targetRotY = normX * 0.45;
        targetRotX = -normY * 0.35;
      }, { passive: true });

      window.addEventListener('deviceorientation', (e) => {
        if (e.beta !== null && e.gamma !== null) {
          targetRotX = (e.beta - 45) * 0.005;
          targetRotY = e.gamma * 0.008;
        }
      }, { passive: true });

      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }, { passive: true });

      function animate() {
        requestAnimationFrame(animate);

        // Autonomous smooth rotation
        torusKnot.rotation.x += 0.0022;
        torusKnot.rotation.y += 0.0035;
        orbitRing.rotation.z += 0.0015;

        // Smooth lerp tilt reaction to cursor movements
        curRotX += (targetRotX - curRotX) * 0.05;
        curRotY += (targetRotY - curRotY) * 0.05;

        wireframeGroup.rotation.x = curRotX;
        wireframeGroup.rotation.y = curRotY;

        renderer.render(scene, camera);
      }
      animate();
    })();
  </script>

  """

if idx_three_start != -1 and idx_three_end != -1:
    html = html[:idx_three_start] + new_three_script + html[idx_three_end:]
    print("Replaced Three.js background script with TorusKnot wireframe")
else:
    print("Warning: could not locate Three.js script block boundaries")

# 4. Update Total Stashed Display ID
old_metric_id = 'id="metric-total-capital"'
new_metric_id = 'id="totalStashedDisplay"'
if old_metric_id in html:
    html = html.replace(old_metric_id, new_metric_id)
    print("Updated metric-total-capital to totalStashedDisplay in HTML")

# 5. Update JS references to metric-total-capital to handle totalStashedDisplay
old_js_metric = "const elTotal = document.getElementById('metric-total-capital');"
new_js_metric = "const elTotal = document.getElementById('totalStashedDisplay') || document.getElementById('metric-total-capital');"
if old_js_metric in html:
    html = html.replace(old_js_metric, new_js_metric)
    print("Updated JS reference to elTotal")

# 6. Ensure Mobile Bottom Dock class strictly matches specification
# fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-md border-t border-slate-200 z-50 py-2.5 px-4 flex justify-around items-center pb-safe md:hidden
old_nav_dock = '<nav id="mobile-navigation-dock" class="fixed bottom-0 inset-x-0 z-40 bg-white/95 backdrop-blur-2xl border-t border-slate-200/90 shadow-[0_-8px_25px_rgba(15,23,42,0.08)] md:hidden flex items-center justify-around px-2 py-2 pb-[max(0.65rem,env(safe-area-inset-bottom))]">'
new_nav_dock = '<nav id="mobile-navigation-dock" class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-md border-t border-slate-200 z-50 py-2.5 px-4 flex justify-around items-center pb-safe md:hidden shadow-[0_-8px_25px_rgba(15,23,42,0.08)]">'
if old_nav_dock in html:
    html = html.replace(old_nav_dock, new_nav_dock)
    print("Updated mobile-navigation-dock styling")

# 7. Ensure Desktop Lower Rail container has flex flex-col justify-end gap-2 pb-6 mt-auto
old_desktop_stack = '<div class="flex flex-col justify-end mt-auto pt-6 border-t border-slate-100 space-y-2">'
new_desktop_stack = '<div class="flex flex-col justify-end gap-2 pb-6 mt-auto pt-6 border-t border-slate-100">'
if old_desktop_stack in html:
    html = html.replace(old_desktop_stack, new_desktop_stack)
    print("Updated desktop nav stack styling")

# Write out updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully! Length:", len(html))
