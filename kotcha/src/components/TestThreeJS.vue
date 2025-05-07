<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';

const canvasRef = ref(null);
const cameraRotation = ref(0);
const targetRotation = ref(0); // Target rotation for smooth animation

const rotateCamera = (direction) => {
  const angle = direction === 'left' ? -Math.PI / 4 : Math.PI / 4; // 45 degrees
  targetRotation.value += angle; // Update target rotation
};

onMounted(() => {
  const canvas = canvasRef.value;

  // Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000); // Aspect ratio for mobile resolution
  const renderer = new THREE.WebGLRenderer({ canvas });

  // Set renderer size and pixel ratio for high resolution
  renderer.setSize(375, 667); // Mobile resolution
  renderer.setPixelRatio(window.devicePixelRatio);

  // Walls (House)
  const wallMaterial = new THREE.MeshBasicMaterial({ color: 0x8b4513, side: THREE.DoubleSide }); // Wooden color
  const wallGeometry = new THREE.PlaneGeometry(10, 10);

  const frontWall = new THREE.Mesh(wallGeometry, wallMaterial);
  frontWall.position.set(0, 0, -5);

  const backWall = new THREE.Mesh(wallGeometry, wallMaterial);
  backWall.position.set(0, 0, 5);
  backWall.rotation.y = Math.PI;

  const leftWall = new THREE.Mesh(wallGeometry, wallMaterial);
  leftWall.position.set(-5, 0, 0);
  leftWall.rotation.y = Math.PI / 2;

  const rightWall = new THREE.Mesh(wallGeometry, wallMaterial);
  rightWall.position.set(5, 0, 0);
  rightWall.rotation.y = -Math.PI / 2;

  scene.add(frontWall, backWall, leftWall, rightWall);

  // Light (Sun)
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(10, 10, 10);
  scene.add(light);

  camera.position.z = 0; // Center the camera in the house
  camera.position.y = 2; // Slightly elevate the camera

  // Animation loop
  const animate = () => {
    requestAnimationFrame(animate);

    // Smooth rotation animation
    cameraRotation.value += (targetRotation.value - cameraRotation.value) * 0.1; // Interpolation
    camera.rotation.y = cameraRotation.value;

    renderer.render(scene, camera);
  };

  animate();

  // Handle window resize to maintain aspect ratio and resolution
  window.addEventListener('resize', () => {
    camera.aspect = 375 / 667; // Update aspect ratio for mobile resolution
    camera.updateProjectionMatrix();
    renderer.setSize(375, 667);
    renderer.setPixelRatio(window.devicePixelRatio);
  });
});
</script>

<template>
  <canvas ref="canvasRef" style="width: 375px; height: 667px;"></canvas>
  <div style="position: absolute; top: 50%; transform: translateY(-50%); width: 375px; display: flex; justify-content: space-between; padding: 0 0px;">
    <button @click="rotateCamera('right')">Left</button>
    <button @click="rotateCamera('left')">Right</button>
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