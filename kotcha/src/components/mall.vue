<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';

const canvasRef = ref(null);

onMounted(() => {
  const canvas = canvasRef.value;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x222233);

  const camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000);
  camera.position.set(0, 2, 5);

  const renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(375, 667);
  renderer.setPixelRatio(window.devicePixelRatio);

  // Add some ambient light
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  // Add a grid helper for orientation
  const gridHelper = new THREE.GridHelper(100, 100);
  scene.add(gridHelper);

  // Add the malltest.fbx model in the middle of the scene
  const loader = new FBXLoader();
  loader.load(
    '/src/assets/winter/source/winter/winter.fbx', // Make sure malltest.fbx is in the public folder (not src/assets or ./assets)
    (object) => {
      object.position.set(0, 0, 0); // Center the model in the scene
      object.scale.set(0.1, 0.1, 0.1); // Adjust scale if needed
      scene.add(object);
    },
    undefined,
    (error) => {
      console.error('Error loading FBX:', error);
      // Add a user-friendly message
      alert('Failed to load malltest.fbx. Make sure the file is a valid FBX (binary or ASCII, version 7.4 or lower) and is placed in the public folder.');
    }
  );

  // PointerLockControls for flying
  const controls = new PointerLockControls(camera, renderer.domElement);

  // Movement state
  const move = { forward: false, backward: false, left: false, right: false, up: false, down: false };
  const velocity = new THREE.Vector3();

  // Listen for pointer lock
  canvas.addEventListener('click', () => {
    controls.lock();
  });

  // Keyboard controls
  const onKeyDown = (event) => {
    switch (event.code) {
      case 'KeyS': move.forward = true; break;
      case 'KeyW': move.backward = true; break;
      case 'KeyA': move.left = true; break;
      case 'KeyD': move.right = true; break;
      case 'Space': move.up = true; break;
      case 'ShiftLeft': move.down = true; break;
    }
  };
  const onKeyUp = (event) => {
    switch (event.code) {
      case 'KeyS': move.forward = false; break;
      case 'KeyW': move.backward = false; break;
      case 'KeyA': move.left = false; break;
      case 'KeyD': move.right = false; break;
      case 'Space': move.up = false; break;
      case 'ShiftLeft': move.down = false; break;
    }
  };
  window.addEventListener('keydown', onKeyDown);
  window.addEventListener('keyup', onKeyUp);

  // Animation loop
  const animate = () => {
    requestAnimationFrame(animate);

    // Simple fly movement
    const speed = 0.1;
    velocity.set(0, 0, 0);
    if (move.forward) velocity.z -= speed;
    if (move.backward) velocity.z += speed;
    if (move.left) velocity.x -= speed;
    if (move.right) velocity.x += speed;
    if (move.up) velocity.y += speed;
    if (move.down) velocity.y -= speed;

    controls.moveRight(velocity.x);
    controls.moveForward(velocity.z);
    camera.position.y += velocity.y;

    renderer.render(scene, camera);
  };

  animate();

  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = 375 / 667;
    camera.updateProjectionMatrix();
    renderer.setSize(375, 667);
    renderer.setPixelRatio(window.devicePixelRatio);
  });
});
</script>

<template>
  <canvas ref="canvasRef" style="width: 375px; height: 667px; background: #222233; cursor: pointer;"></canvas>
  <div style="position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 6px 12px; border-radius: 6px;">
    Click canvas, then use mouse to look and WASD + Space/Shift to fly
  </div>
</template>

<style scoped>
canvas {
  display: block;
}
</style>
