<script setup lang='ts'>
import { onMounted, ref } from 'vue';
import { Terminal } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';

defineOptions({
  name: 'jbcz'
})

const terminalRef = ref(null);

onMounted(() => {
  const term = new Terminal();
  term.open(terminalRef.value);
  term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ');
});
</script>

<template>
  <div>
    <div ref="terminalRef" class="terminal-container"></div>
  </div>
</template>

<style lang='scss' scoped>
.terminal-container {
  width: 100%;
  height: 400px; /* 你可以根据需要调整终端的高度 */
}
</style>
