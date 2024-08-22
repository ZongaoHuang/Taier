<template>
  <div>
    <h1>数据集测试</h1>
    <el-form :model="form" label-width="100px">
      <el-form-item label="名称">
        <el-input v-model="form.name" placeholder="请输入名称"></el-input>
      </el-form-item>
      <el-form-item label="规模">
        <el-input v-model="form.scale" placeholder="请输入规模"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchData">获取数据集</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="date" label="日期" width="180" />
      <el-table-column prop="name" label="名称" width="180" />
      <el-table-column prop="id" label="ID" width="180" />
      <el-table-column prop="scale" label="规模" width="180" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getSjj } from "@/api/sjj";

// 表单数据
const form = ref({
  name: "",
  scale: ""
});

// 表格数据
const tableData = ref([]);

// 获取数据集
const fetchData = async () => {
  const response = await getSjj({ name: form.value.name, scale: form.value.scale });
  if (response.success) {
    tableData.value = response.data?.list || [];
  } else {
    console.error("获取数据失败");
  }
};
</script>
