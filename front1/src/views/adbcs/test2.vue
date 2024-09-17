<script setup lang="ts">
import { useColumns } from "./components/header-renderer/columns";
import Calendar from "@iconify-icons/ri/calendar-2-line";
import { ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus"; // 引入消息框组件和消息提示组件
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";

const { columns, filterTableData } = useColumns();
const datasetForm = ref({
  name: "",
  id: ""
});

function createDataset() {
  ElMessageBox.prompt("请输入数据集名称", "新建数据集", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    inputValidator: value => {
      if (!value) return "数据集名称不能为空";
      return true;
    },
    inputPlaceholder: "数据集名称"
  })
    .then(({ value }) => {
      datasetForm.value.name = value;
      requestDatasetID();
    })
    .catch(() => {
      ElMessage.info("取消创建数据集");
    });
}

function requestDatasetID() {
  ElMessageBox.prompt("请输入数据集ID", "新建数据集", {
    confirmButtonText: "创建并配置",
    cancelButtonText: "取消",
    inputValidator: value => {
      if (!value) return "数据集ID不能为空";
      return true;
    },
    inputPlaceholder: "数据集ID"
  })
    .then(({ value }) => {
      datasetForm.value.id = value;
      ElMessage.success("数据集创建成功");
      // 跳转到配置页面
      redirectToConfigPage();
    })
    .catch(() => {
      ElMessage.info("取消创建数据集");
    });
}

function redirectToConfigPage() {
  // 假设配置页面的路径是 "/config"
  window.location.href = `/config?name=${encodeURIComponent(datasetForm.value.name)}&id=${encodeURIComponent(datasetForm.value.id)}`;
}
</script>

<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header flex justify-between items-center">
        <h1>数据集管理</h1>
        <el-button type="primary" @click="createDataset">创建数据集</el-button>
      </div>
    </template>
    <pure-table :data="filterTableData" :columns="columns">
      <template #nameHeader>
        <span class="flex items-center">
          <IconifyIconOffline :icon="Calendar" />
          创建时间
        </span>
      </template>
    </pure-table>
  </el-card>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
