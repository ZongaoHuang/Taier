<template>
  <section class="app-main" :style="{ minHeight: minHeight }">
    <router-view>
      <!-- <component :is="Component" :key="task_name" /> -->
      <p>{{ task_name }}</p>
    </router-view>
  </section>
</template>

<script setup>
// defineProps({
//   task_name: String,
// });
const minHeight = computed(() => {
  if (useSettingsStore().tagsView) {
    return `calc(100vh - ${variables["navbar-height"]} - ${variables["tags-view-height"]})`;
  } else {
    return `calc(100vh - ${variables["navbar-height"]})`;
  }
});
// onMounted(() => {
//   console.info("task_name", task_name);
// });
</script>
