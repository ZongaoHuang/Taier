<template>
  <div>
    <el-button type="primary" @click="fetchData1">测试</el-button>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { test11 } from "@/api/test"; // 引入之前定义的test函数

// 点击按钮手动触发获取数据
async function fetchData1() {
  try {
    const response = await test11();
    if (response && response.data) {
      console.log('Response:', response.data);
    } else {
      console.error('Response is undefined or missing data');
    }
  } catch (error) {
    console.error('Request failed:', error.message);
  }
}


// 页面加载时自动调用 fetchData1
onMounted(() => {
  fetchData1();
});
</script>
