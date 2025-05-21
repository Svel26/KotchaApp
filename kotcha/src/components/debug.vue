<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);
const selectedModel = ref('Bakerij.glb');
const models = [
  { name: 'Bakery (glb)', file: 'Bakerij.glb', type: 'glb', path: '/src/assets/Bakerij.glb' },
  { name: 'Bakery', file: 'bakery.gltf', type: 'gltf', path: '/src/assets/bakery.gltf' },
];

const cameraCoords = ref({ x: 0, y: 0, z: 0 });

let scene, camera, renderer, controls;
let currentModel = null;

function loadModel(model) {
  // Remove previous model if exists
  if (currentModel) {
    scene.remove(currentModel);
    currentModel.traverse?.((child) => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach((m) => m.dispose());
        } else {
          child.material.dispose();
        }
      }
    });
    currentModel = null;
  }
  // Use GLTFLoader for both gltf and glb
  if (model.type === 'gltf' || model.type === 'glb') {
    const loader = new GLTFLoader();
    loader.load(
      model.path,
      (gltf) => {
        const object = gltf.scene;
        object.position.set(0, 0, 0);
        object.scale.set(1, 1, 1);
        scene.add(object);
        currentModel = object;
      },
      undefined,
      (error) => {
        console.error('Error loading GLTF/GLB:', error);
        alert(`Failed to load ${model.file}.`);
      }
    );
  }
}

function onSwitchModel() {
  const model = models.find(m => m.file === selectedModel.value);
  if (model) loadModel(model);
}

onMounted(() => {
  const canvas = canvasRef.value;
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x222233);

  camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000);
  camera.position.set(0, 2, 5);

  renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(375, 667);
  renderer.setPixelRatio(window.devicePixelRatio);

  // Add some ambient light
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  // Add a grid helper for orientation
  const gridHelper = new THREE.GridHelper(100, 100);
  scene.add(gridHelper);

  // Load initial model
  loadModel(models[0]);

  // PointerLockControls for flying
  controls = new PointerLockControls(camera, renderer.domElement);

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

    // Update camera coordinates for UI
    cameraCoords.value = {
      x: camera.position.x.toFixed(2),
      y: camera.position.y.toFixed(2),
      z: camera.position.z.toFixed(2),
      rotY: camera.rotation.y.toFixed(2),
    };

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
  <div style="position: relative; width: 375px; margin: 0 auto;">
    <canvas ref="canvasRef" style="width: 375px; height: 667px; background: #222233; cursor: pointer;"></canvas>
    <div style="position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 6px 12px; border-radius: 6px;">
      Click canvas, then use mouse to look and WASD + Space/Shift to fly
    </div>
    <div style="position: absolute; top: 60px; left: 10px; background: rgba(0,0,0,0.7); padding: 8px 12px; border-radius: 6px;">
      <select v-model="selectedModel" style="margin-right: 8px;">
        <option v-for="model in models" :key="model.file" :value="model.file">{{ model.name }}</option>
      </select>
      <button @click="onSwitchModel">Switch Model</button>
    </div>
    <div style="position: absolute; top: 110px; left: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 14px;">
      Camera: X: {{ cameraCoords.x }}<br>
      Y: {{ cameraCoords.y }}<br>
      Z: {{ cameraCoords.z }} <br>
      RotY: {{ cameraCoords.rotY }}<br>

    </div>
  </div>
</template>

<style scoped>
canvas {
  display: block;
}
button {
  padding: 4px 12px;
  font-size: 14px;
  cursor: pointer;
}
select {
  font-size: 14px;
  padding: 2px 6px;
}
</style>
