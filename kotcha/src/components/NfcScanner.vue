<template>
    <div class="nfc-scanner-overlay" @click.self="$emit('close')">
      <div class="nfc-scanner-content">
        <h3>Scan Collectible</h3>
        <p>{{ statusMessage }}</p>
        <div class="nfc-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="80" height="80"><path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H4V4h16v16zM18 6h-5c-1.1 0-2 .9-2 2v2.28c-.6.35-1 .98-1 1.72 0 1.1.9 2 2 2s2-.9 2-2c0-.74-.4-1.38-1-1.72V8h3v8H8V8h2V6H8c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2v- воспалительных.02c.63-.33 1.02-1.01 1-1.73v-2.25h1V6z"/></svg>
        </div>
        <button @click="$emit('close')" class="cancel-button">Cancel</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  const emit = defineEmits(['close', 'scan-success']);
  const statusMessage = ref('Ready to scan. Hold your phone near the collectible.');
  let ndef = null;
  
  const startScan = async () => {
    if ('NDEFReader' in window) {
      try {
        ndef = new NDEFReader();
        await ndef.scan();
        statusMessage.value = 'Scan active! Waiting for a tag...';
  
        ndef.addEventListener('reading', handleReading);
        ndef.addEventListener('readingerror', handleReadingError);
  
      } catch (error) {
        statusMessage.value = `Error: ${error.message}`;
        console.error("NFC Error:", error);
      }
    } else {
      statusMessage.value = 'Web NFC is not supported on this device.';
    }
  };
  
  const handleReading = ({ serialNumber }) => {
    statusMessage.value = `Success! Scanned: ${serialNumber}`;
    emit('scan-success', serialNumber);
    emit('close'); // Automatically close the scanner on success
  };
  
  const handleReadingError = () => {
    statusMessage.value = 'Could not read the tag. Please try again.';
  };
  
  onMounted(() => {
    startScan();
  });
  
  onUnmounted(() => {
    if (ndef) {
      // Clean up listeners when the component is destroyed
      ndef.removeEventListener('reading', handleReading);
      ndef.removeEventListener('readingerror', handleReadingError);
    }
  });
  </script>
  
  <style scoped>
  .nfc-scanner-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(5px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    animation: fadeInOverlay 0.3s ease;
  }
  
  .nfc-scanner-content {
    background: white;
    color: #333;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    max-width: 90%;
    width: 320px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  }
  
  h3 {
    margin-top: 0;
    font-size: 1.5rem;
    color: #1a1a1a;
  }
  
  p {
    font-size: 1rem;
    color: #555;
    min-height: 40px;
  }
  
  .nfc-icon {
    margin: 2rem 0;
    color: #007bff;
    opacity: 0.8;
  }
  
  .cancel-button {
    width: 100%;
    padding: 12px;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    background: #e9ecef;
    color: #495057;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .cancel-button:hover {
    background-color: #dee2e6;
  }
  
  @keyframes fadeInOverlay {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  </style>