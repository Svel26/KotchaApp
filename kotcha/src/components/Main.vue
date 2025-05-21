<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);

const cameraPositions = [
  { x: -3.94, y: 1.10, z: 4.19, rotY: -0.34 },
  { x: 0.99, y: 0.60, z: 4.89, rotY: 0.09 },
  { x: 0, y: 5, z: 0, rotY: 0 },
  { x: -5, y: 2, z: 0, rotY: 0 },
  { x: 0, y: 2, z: -5, rotY: 0 },
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
  <canvas ref="canvasRef" style="width: 375px; height: 667px;"></canvas>
  <div style="position: absolute; top: 50%; transform: translateY(-50%); width: 375px; display: flex; justify-content: space-between; padding: 0 0px;">
    <button @click="prevPosition" :disabled="currentIndex === 0">Back</button>
    <button @click="nextPosition" :disabled="currentIndex === cameraPositions.length - 1">Next</button>
  </div>
</template>

<style scoped>
canvas {
  display: block;
}

button {
  padding: 10px 18px;
  font-size: 16px;
  cursor: pointer;
}
</style>