<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);

const cameraPositions = [
  {x: -0.14, y: 1.00, z: 1.89, rotY: 1.6},
  {x: -0.52, y: 1.30, z: 4.61, rotY: -0.67},
  {x: 3.19, y: 1.30, z: 4.26, rotY: 0.54},
  {x: 3.71, y: 1, z: 1.50, rotY: 0.67},
  {x: -3.11, y: 1.60, z: 2.34, rotY: -0.42},
];
const currentIndex = ref(0);
const textDisplay = ["Broodjes", "Donuts", "Donuts", "Vers uit de oven", "Stokbrood"];

// Popup state
const showPopup = ref(false);
const popupText = ref("");
const popupFadeOut = ref(false);

// Video overlay state
const showVideo = ref(false);
const videoKey = ref(0); // To force reload video
const videoSrc = ref(''); // Dynamic video source
let camera, scene, renderer;
let targetPosition = { ...cameraPositions[0] };
let targetRotY = cameraPositions[0].rotY ?? 0;

// Store references to loaded models
let stokbroodMesh = null;
let donutMesh = null;

const moveToIndex = (idx) => {
  if (idx >= 0 && idx < cameraPositions.length) {
    currentIndex.value = idx;
    targetPosition = {...cameraPositions[idx]};
    targetRotY = cameraPositions[idx].rotY ?? 0;
  }
};

const nextPosition = () => {
  // Always allow next, wrap to first if at end
  if (currentIndex.value < cameraPositions.length - 1) {
    moveToIndex(currentIndex.value + 1);
  } else {
    moveToIndex(0); // wrap to first
  }
};

const prevPosition = () => {
  // Always allow back, wrap to last if at start
  if (currentIndex.value > 0) {
    moveToIndex(currentIndex.value - 1);
  } else {
    moveToIndex(cameraPositions.length - 1); // wrap to last
  }
};

function closePopup() {
  popupFadeOut.value = true;
  setTimeout(() => {
    showPopup.value = false;
    popupFadeOut.value = false;
  }, 400); // match fade-out duration
}

let pendingModelSwap = null;

function playVideoAndSwapModel(swapType) {
  if (swapType === 'u') {
    videoSrc.value = '/src/assets/donut.mp4';
  } else if (swapType === 'p') {
    videoSrc.value = '/src/assets/stokbrood.mp4';
  }
  showVideo.value = true;
  videoKey.value++;
  pendingModelSwap = swapType;
}

function onVideoEnded() {
  showVideo.value = false;
  if (pendingModelSwap === 'u') {
    // Remove donut_black.glb if present
    if (donutMesh) {
      scene.remove(donutMesh);
      donutMesh = null;
    }
    // Load donut.glb and assign to donutMesh
    const loader = new GLTFLoader();
    loader.load(
      '/src/assets/donut.glb',
      (gltf) => {
        const object = gltf.scene;
        object.name = 'donut';
        donutMesh = object;
        scene.add(object);
      },
      undefined,
      (error) => {
        console.error('Error loading donut.glb:', error);
      }
    );
  } else if (pendingModelSwap === 'p') {
    // Remove stokbrood_black.glb if present
    if (stokbroodMesh) {
      scene.remove(stokbroodMesh);
      stokbroodMesh = null;
    }
    // Load stokbrood.glb and assign to stokbroodMesh
    const loader = new GLTFLoader();
    loader.load(
      '/src/assets/stokbrood.glb',
      (gltf) => {
        const object = gltf.scene;
        object.name = 'stokbrood';
        stokbroodMesh = object;
        scene.add(object);
      },
      undefined,
      (error) => {
        console.error('Error loading stokbrood.glb:', error);
      }
    );
  }
  pendingModelSwap = null;
}

let backgroundAudio = null;

onMounted(() => {
  // Play and loop background audio
  if (!backgroundAudio) {
    backgroundAudio = new Audio('/src/sounds/theme.wav');
    backgroundAudio.loop = true;
    backgroundAudio.volume = 0.5;
    backgroundAudio.autoplay = true;
    backgroundAudio.play().catch(e => {
      // Some browsers require user interaction before playing audio
      console.warn('Audio playback failed:', e);
      // Try to resume on first user interaction
      const resumeAudio = () => {
        backgroundAudio.play().catch(() => {});
        window.removeEventListener('click', resumeAudio);
        window.removeEventListener('keydown', resumeAudio);
      };
      window.addEventListener('click', resumeAudio);
      window.addEventListener('keydown', resumeAudio);
    });
  }

  // Play click sound on any click in the app
  const playClick = () => {
    const clickAudio = new Audio('/src/sounds/click.wav');
    clickAudio.volume = 0.7;
    clickAudio.play();
  };
  window.addEventListener('click', playClick);

  const canvas = canvasRef.value;

  scene = new THREE.Scene();

  const width = window.innerWidth;
  const height = window.innerHeight;

  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(width, height);

  renderer.setPixelRatio(window.devicePixelRatio);

  // Add light
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(10, 10, 10);
  scene.add(light);

  // Add bakery.gltf model
  const loader = new GLTFLoader();
  loader.load(
    '/src/assets/bakery_3.gltf',
    (gltf) => {
      const object = gltf.scene;
      object.position.set(0, 0, 0);
      object.scale.set(1, 1, 1);
      scene.add(object);
    },
    undefined,
    (error) => {
      console.error('Error loading bakery.gltf:', error);
      alert('Failed to load bakery.gltf.');
    }
  );

  // Add donut.glb model
  loader.load(
    '/src/assets/donut_black.glb',
    (gltf) => {
      const object = gltf.scene;
      donutMesh = object;
      scene.add(object);
    },
    undefined,
    (error) => {
      console.error('Error loading donut.glb:', error);
    }
  );

  // Add stokbrood.glb model
  loader.load(
    '/src/assets/stokbrood_black.glb',
    (gltf) => {
      const object = gltf.scene;
      stokbroodMesh = object;
      scene.add(object);
    },
    undefined,
    (error) => {
      console.error('Error loading stokbrood.glb:', error);
    }
  );

  // --- KEYBOARD SWAP LOGIC ---
  window.addEventListener('keydown', (event) => {
    if ((event.key === 'u' || event.key === 'U') && !showVideo.value) {
      playVideoAndSwapModel('u');
      return;
    }
    if ((event.key === 'p' || event.key === 'P') && !showVideo.value) {
      playVideoAndSwapModel('p');
      return;
    }
    // ...existing code for other keys if any...
  });

  // Set initial camera position and rotation
  camera.position.set(targetPosition.x, targetPosition.y, targetPosition.z);
  camera.rotation.y = targetRotY;

  // Animation loop
  const animate = () => {
    requestAnimationFrame(animate);

    // Smoothly interpolate camera position to target
    camera.position.x += (targetPosition.x - camera.position.x) * 0.1;
    camera.position.y += (targetPosition.y - camera.position.y) * 0.1;
    camera.position.z += (targetPosition.z - camera.position.z) * 0.1;

    // Smoothly interpolate camera rotation.y to targetRotY
    let delta = targetRotY - camera.rotation.y;
    // Keep delta in [-PI, PI] for shortest path
    if (delta > Math.PI) delta -= 2 * Math.PI;
    if (delta < -Math.PI) delta += 2 * Math.PI;
    camera.rotation.y += delta * 0.1;

    renderer.render(scene, camera);
  };

  animate();

  window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  });

  // Raycaster for click detection
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  function onCanvasClick(event) {
    // Get canvas bounds
    const rect = canvas.getBoundingClientRect();
    // Convert mouse position to normalized device coordinates (-1 to +1)
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    // Check intersection with donut and stokbrood
    const clickableMeshes = [];
    if (donutMesh) clickableMeshes.push(donutMesh);
    if (stokbroodMesh) clickableMeshes.push(stokbroodMesh);
    let found = false;
    clickableMeshes.forEach(mesh => {
      // If the mesh is a group, check its children
      const intersects = raycaster.intersectObject(mesh, true);
      if (intersects.length > 0 && !found) {
        found = true;
        if (mesh === donutMesh) {
          popupText.value = 'Een donut met een geheim! Van buiten lekker fluffy, van binnen gevuld met romige custard én een knapperig suikerlaagje on top, net als z’n chique Franse broer. Een toetje en een snack in één. Tip: breek de bovenkant met je lepel voor de ultieme crack! (Of gewoon met je tanden, we zeggen niks.)';
        } else if (mesh === stokbroodMesh) {
          popupText.value = 'Altijd in de stemming voor een crunch? Dit Franse icoon is knapperig van buiten, zacht van binnen en perfect om te dippen, beleggen of gewoon stiekem zo op te eten. Wist je dat ‘baguette’ in het Frans gewoon ‘stok’ betekent? Bijt erin en voel je even in een Parijse bistro... of gewoon bij Appie op de hoek.';
        }
        showPopup.value = true;
      }
    });
  }
  canvas.addEventListener('click', onCanvasClick);
});
</script>

<template>
  <div class="container-fluid p-0 position-relative">

    <div class="logo"/>

    <div class="position-absolute start-50 translate-middle text-light" style="top: 8%">
      <div class="col-12">
        <p class="m-0 text-display-bordered">{{ textDisplay[currentIndex] }}</p>
      </div>
    </div>

    <canvas ref="canvasRef" style="width: 100vw; height: 100vh; display: block;"></canvas>

    <div
        style="position: absolute; top: 50%; transform: translateY(-50%); width: 100vw; display: flex; justify-content: space-between; padding: 0 0px;">
      <button @click="prevPosition">Back</button>
      <button @click="nextPosition">Next</button>
    </div>

    <!-- Model/video swap buttons -->
    <div style="position: absolute; bottom: 32px; right: 32px; display: flex; flex-direction: column; gap: 12px; z-index: 1200;">
      <button @click="playVideoAndSwapModel('u')" class="swap-btn">Donut</button>
      <button @click="playVideoAndSwapModel('p')" class="swap-btn">Stokbrood</button>
    </div>

    <div v-if="showPopup" class="popup-overlay" :class="{ 'fade-out': popupFadeOut }" @click="closePopup">
      <div class="popup-content" :class="{ 'fade-out': popupFadeOut }">
        <span>{{ popupText }}</span>
        <button @click.stop="closePopup" style="margin-top: 12px;">Sluiten</button>
      </div>
    </div>

    <div v-if="showVideo" class="video-overlay">
      <video
        :key="videoKey"
        :src="videoSrc"
        @ended="onVideoEnded"
        autoplay
        style="max-width: 90vw; max-height: 90vh; border-radius: 18px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); background: #000;"
        controlslist="nodownload nofullscreen noremoteplayback noplaybackrate"
        disablePictureInPicture
        :controls="false"
      ></video>
    </div>
  </div>
</template>

<style scoped>
canvas {
  display: block;
}

.logo {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 60px;
  height: 60px;
  background-image: url('https://cdn.brandfetch.io/id74e2GHv4/theme/dark/logo.svg?c=1dxbfHSJFAPEGdCLU4o5B');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  z-index: 10;
}

button {
  padding: 10px 18px;
  font-size: 16px;
  cursor: pointer;
}

.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
  opacity: 0;
  animation: fadeInOverlay 0.4s forwards;
  transition: opacity 0.35s cubic-bezier(0.4,0,0.2,1);
}
.popup-overlay.fade-out {
  opacity: 0 !important;
  pointer-events: none;
  animation: none;
}

.popup-content {
  position: relative;
  background: #fff;
  color: #222;
  padding: 40px 36px 32px 36px;
  margin: 1rem;
  border-radius: 18px;
  min-width: 320px;
  max-width: 375px;
  min-height: 120px;
  max-height: 100%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  text-align: center;
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
  word-break: break-word;
  opacity: 0;
  transform: translateY(30px) scale(0.98);
  animation: fadeInPopup 0.5s 0.1s cubic-bezier(0.4,0,0.2,1) forwards;
  transition: opacity 0.4s cubic-bezier(0.4,0,0.2,1), transform 0.4s cubic-bezier(0.4,0,0.2,1);
}
.popup-content.fade-out {
  opacity: 0 !important;
  transform: translateY(30px) scale(0.98) !important;
  animation: none;
  pointer-events: none;
}
.popup-content button {
  margin-top: 24px;
  padding: 10px 28px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background: #222233;
  color: #fff;
  cursor: pointer;
  /* transition: background 0.2s; */
}
.popup-content button:hover {
  background: #444466;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 18px;
}

@keyframes fadeInOverlay {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInPopup {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.text-display-bordered {
  background: rgba(0,0,0,0.75);
  border-radius: 12px;
  padding: 8px 20px;
  border: 2px solid #111;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
  display: inline-block;
}

.video-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.video-player {
  max-width: 90%;
  max-height: 90%;
  border: 4px solid #fff;
  border-radius: 12px;
}

.swap-btn {
  background: #fff;
  color: #222233;
  border: 2px solid #222233;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
  cursor: pointer;
  transition: background 0.18s, color 0.18s, border 0.18s;
}
.swap-btn:hover {
  background: #222233;
  color: #fff;
  border-color: #444466;
}
</style>