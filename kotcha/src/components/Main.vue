<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);

const cameraPositions = [
  { x: -3.94, y: 1.10, z: 4.19, rotY: -0.34 },
  { x: 0.99, y: 0.60, z: 4.89, rotY: 0.09 },
  { x: 3.10, y: 1, z: 4.14, rotY: 0.47 },
  { x: 3.71, y: 1, z: 1.50, rotY: 0.67 },
  { x: 1.06, y: 1.60, z: 0.78, rotY: -0.24 },
];
const currentIndex = ref(0);

let camera, scene, renderer;
let targetPosition = { ...cameraPositions[0] };
let targetRotY = cameraPositions[0].rotY ?? 0;

const moveToIndex = (idx) => {
  if (idx >= 0 && idx < cameraPositions.length) {
    currentIndex.value = idx;
    targetPosition = { ...cameraPositions[idx] };
    targetRotY = cameraPositions[idx].rotY ?? 0;
  }
};

const nextPosition = () => {
  if (currentIndex.value < cameraPositions.length - 1) {
    moveToIndex(currentIndex.value + 1);
  }
};

const prevPosition = () => {
  if (currentIndex.value > 0) {
    moveToIndex(currentIndex.value - 1);
  }
};

onMounted(() => {
  const canvas = canvasRef.value;

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ canvas });

  renderer.setSize(375, 667);
  renderer.setPixelRatio(window.devicePixelRatio);

  // Add light
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(10, 10, 10);
  scene.add(light);

  // Add bakery.gltf model
  const loader = new GLTFLoader();
  loader.load(
      '/src/assets/bakery.gltf',
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
        <p class="m-0">hello world</p>
      </div>
    </div>

    <canvas ref="canvasRef" style="width: 375px; height: 667px;"></canvas>

    <div style="position: absolute; top: 50%; transform: translateY(-50%); width: 375px; display: flex; justify-content: space-between; padding: 0 0px;">
      <button @click="prevPosition" :disabled="currentIndex === 0">Back</button>
      <button @click="nextPosition" :disabled="currentIndex === cameraPositions.length - 1">Next</button>
    </div>
  </div>
</template>

<style scoped>
canvas {
  display: block;
}

.logo { position: absolute;
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