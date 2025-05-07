
<template>
  <div style="text-align: center; padding: 20px;">
    <h1>Testing UI Component</h1>
    <p>If you see this message, the UI component is working!</p>
    <button @click="handleClick">Click Me</button>
  </div>
</template>

<script>
export default {
  name: "Ui",
  methods: {
    handleClick() {
      alert("Button clicked! The UI component is working.");
    },
  },
};
</script>

<style scoped>
h1 {
  color: #646cff;
}
button {
  padding: 10px 20px;
  background-color: #646cff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #535bf2;
}
</style>
  
  <style scoped>
  /* Optional styling for the container */
  </style>