<script setup>
import {onMounted, ref} from 'vue';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);

const cameraPositions = [
  {x: -0.14, y: 1.00, z: 1.89, rotY: 1.6},
  {x: -0.52, y: 1.30, z: 4.61, rotY: -0.67},
  {x: 3.19, y: 1.30, z: 4.26, rotY: 0.54},
  {x: 3.71, y: 1, z: 1.50, rotY: 0.67},
  {x: -3.11, y: 1.60, z: 2.34, rotY: -0.42},
];
const currentIndex = ref(0);

const textDisplay = ["broodjes", "bagels", "stokbrood", "vers uit de oven"];

let camera, scene, renderer;
let targetPosition = {...cameraPositions[0]};
let targetRotY = cameraPositions[0].rotY ?? 0;

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

onMounted(() => {
  // Play and loop background audio
  const audio = new Audio('/src/sounds/theme.wav');
  audio.loop = true;
  audio.volume = 0.5; // Optional: set volume
  audio.play().catch(e => {
    // Some browsers require user interaction before playing audio
    console.warn('Audio playback failed:', e);
  });

  // Play click sound on any click in the app
  const playClick = () => {
    const clickAudio = new Audio('/src/sounds/click.wav');
    clickAudio.volume = 0.7;
    clickAudio.play();
  };
  window.addEventListener('click', playClick);

  const canvas = canvasRef.value;

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({canvas});

  renderer.setSize(375, 667);
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
      '/src/assets/donut.glb',
      (gltf) => {
        const object = gltf.scene;
        scene.add(object);
      },
      undefined,
      (error) => {
        console.error('Error loading donut.glb:', error);
      }
  );

  // Add stokbrood.glb model
  loader.load(
      '/src/assets/stokbrood.glb',
      (gltf) => {
        const object = gltf.scene;
        scene.add(object);
      },
      undefined,
      (error) => {
        console.error('Error loading stokbrood.glb:', error);
      }
  );

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
    camera.aspect = 375 / 667;
    camera.updateProjectionMatrix();
    renderer.setSize(375, 667);
    renderer.setPixelRatio(window.devicePixelRatio);
  });
});
</script>

<template>
  <div class="container-fluid p-0 position-relative">

    <div class="logo"/>

    <div class="position-absolute start-50 translate-middle text-light" style="top: 8%">
      <div class="col-12">
        <p class="m-0">{{ textDisplay[currentIndex] }}</p>
      </div>
    </div>

    <canvas ref="canvasRef" style="width: 375px; height: 667px;"></canvas>

    <div
        style="position: absolute; top: 50%; transform: translateY(-50%); width: 375px; display: flex; justify-content: space-between; padding: 0 0px;">
      <button @click="prevPosition">Back</button>
      <button @click="nextPosition">Next</button>
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
</style>