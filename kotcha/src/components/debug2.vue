<script setup>
import {onMounted, ref, reactive} from 'vue';
import * as THREE from 'three';
import {PointerLockControls} from 'three/examples/jsm/controls/PointerLockControls';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';

const canvasRef = ref(null);
const selectedModel = ref('Bakerij.glb');
const models = [
  {name: 'Bakery', file: 'bakery.gltf', type: 'gltf', path: '/src/assets/bakery_3.gltf'},
];

// List of available objects to add (add more as needed)
const availableObjects = [
  {name: 'Dog', file: 'dog.glb', path: '/src/assets/dog.glb'},
  {name: 'Bakery', file: 'bakery.gltf', path: '/src/assets/bakery_3.gltf'},
  {name: 'Donut', file: 'donut.gltf', path: '/src/assets/donut.glb'},
  {name: 'Stokbrood', file: 'stokbrood.gltf', path: '/src/assets/stokbrood.glb'},

  // Add more objects here as needed
];
const selectedAddObject = ref(availableObjects[0].file);

// For object manipulation
const objectList = reactive([]);
const selectedObjectIndex = ref(-1);
const objectCoords = ref({x: 0, y: 0, z: 0, rotY: 0});

const cameraCoords = ref({x: 0, y: 0, z: 0, rotY: 0});

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

// Add a new object (glb/gltf) to the scene and select it
function addObject() {
  const objMeta = availableObjects.find(o => o.file === selectedAddObject.value);
  if (!objMeta) return;
  const loader = new GLTFLoader();
  loader.load(
      objMeta.path,
      (gltf) => {
        const object = gltf.scene;
        object.position.set(0, 0, 0);
        object.scale.set(1, 1, 1);
        scene.add(object);
        objectList.push(object);
        selectedObjectIndex.value = objectList.length - 1;
        updateObjectCoords();
      },
      undefined,
      (error) => {
        alert('Failed to load object.');
      }
  );
}

// Move or rotate the selected object
function moveSelectedObject(dx = 0, dy = 0, dz = 0) {
  const obj = objectList[selectedObjectIndex.value];
  if (obj) {
    obj.position.x += dx;
    obj.position.y += dy;
    obj.position.z += dz;
    updateObjectCoords();
  }
}

function rotateSelectedObject(dRotY = 0) {
  const obj = objectList[selectedObjectIndex.value];
  if (obj) {
    obj.rotation.y += dRotY;
    updateObjectCoords();
  }
}

function updateObjectCoords() {
  const obj = objectList[selectedObjectIndex.value];
  if (obj) {
    objectCoords.value = {
      x: obj.position.x.toFixed(2),
      y: obj.position.y.toFixed(2),
      z: obj.position.z.toFixed(2),
      rotY: obj.rotation.y.toFixed(2),
    };
  } else {
    objectCoords.value = {x: 0, y: 0, z: 0, rotY: 0};
  }
}

function selectObject(idx) {
  selectedObjectIndex.value = idx;
  updateObjectCoords();
}

onMounted(() => {
  const canvas = canvasRef.value;
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x222233);

  camera = new THREE.PerspectiveCamera(75, 375 / 667, 0.1, 1000);
  camera.position.set(0, 2, 5);

  renderer = new THREE.WebGLRenderer({canvas: canvasRef.value});
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
  const move = {forward: false, backward: false, left: false, right: false, up: false, down: false};
  const velocity = new THREE.Vector3();

  // Listen for pointer lock
  canvas.addEventListener('click', () => {
    controls.lock();
  });

  // Keyboard controls
  const onKeyDown = (event) => {
    switch (event.code) {
      case 'KeyS':
        move.forward = true;
        break;
      case 'KeyW':
        move.backward = true;
        break;
      case 'KeyA':
        move.left = true;
        break;
      case 'KeyD':
        move.right = true;
        break;
      case 'Space':
        move.up = true;
        break;
      case 'ShiftLeft':
        move.down = true;
        break;
        // Object manipulation (JIKL and Q/E)
      case 'KeyI':
        moveSelectedObject(0, 0, -0.1);
        break; // forward
      case 'KeyK':
        moveSelectedObject(0, 0, 0.1);
        break;  // backward
      case 'KeyJ':
        moveSelectedObject(-0.1, 0, 0);
        break; // left
      case 'KeyL':
        moveSelectedObject(0.1, 0, 0);
        break;  // right
      case 'PageUp':
        moveSelectedObject(0, 0.1, 0);
        break;
      case 'PageDown':
        moveSelectedObject(0, -0.1, 0);
        break;
      case 'KeyQ':
        rotateSelectedObject(-0.1);
        break;
      case 'KeyE':
        rotateSelectedObject(0.1);
        break;
    }
  };
  const onKeyUp = (event) => {
    switch (event.code) {
      case 'KeyS':
        move.forward = false;
        break;
      case 'KeyW':
        move.backward = false;
        break;
      case 'KeyA':
        move.left = false;
        break;
      case 'KeyD':
        move.right = false;
        break;
      case 'Space':
        move.up = false;
        break;
      case 'ShiftLeft':
        move.down = false;
        break;
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
    <div
        style="position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 6px 12px; border-radius: 6px;">
      Click canvas, then use mouse to look and WASD + Space/Shift to fly
    </div>
    <div
        style="position: absolute; top: 60px; left: 10px; background: rgba(0,0,0,0.7); padding: 8px 12px; border-radius: 6px;">
      <select v-model="selectedModel" style="margin-right: 8px;">
        <option v-for="model in models" :key="model.file" :value="model.file">{{ model.name }}</option>
      </select>
      <button @click="onSwitchModel">Switch Model</button>
      <select v-model="selectedAddObject" style="margin-left: 8px;">
        <option v-for="obj in availableObjects" :key="obj.file" :value="obj.file">{{ obj.name }}</option>
      </select>
      <button @click="addObject" style="margin-left: 8px;">Add Object</button>
    </div>
    <div
        style="position: absolute; top: 110px; left: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 14px;">
      Camera: X: {{ cameraCoords.x }}<br>
      Y: {{ cameraCoords.y }}<br>
      Z: {{ cameraCoords.z }} <br>
      RotY: {{ cameraCoords.rotY }}<br>
    </div>
    <div v-if="objectList.length"
         style="position: absolute; top: 200px; left: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 14px;">
      <div>
        <span>Objects:</span>
        <span v-for="(obj, idx) in objectList" :key="idx" style="margin-right: 6px;">
          <button @click="selectObject(idx)"
                  :style="{fontWeight: selectedObjectIndex === idx ? 'bold' : 'normal'}">#{{ idx + 1 }}</button>
        </span>
      </div>
      <div v-if="selectedObjectIndex >= 0">
        <div>Selected Object: #{{ selectedObjectIndex + 1 }}</div>
        <div>X: {{ objectCoords.x }}<br>Y: {{ objectCoords.y }}<br>Z: {{ objectCoords.z }}<br>RotY: {{
            objectCoords.rotY
          }}
        </div>
        <div style="margin-top: 6px;">
          <span>Move: J (left), L (right), I (forward), K (backward), PgUp/PgDn (Y)</span><br>
          <span>Rotate Y: Q/E</span>
        </div>
      </div>
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
