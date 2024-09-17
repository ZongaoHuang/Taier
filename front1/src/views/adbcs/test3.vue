<script setup lang="ts">
import { useColumns } from "./components/header-renderer/columns";
import Calendar from "@iconify-icons/ri/calendar-2-line";
import { ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus"; // 引入消息框组件和消息提示组件

const { columns, filterTableData } = useColumns();
const datasetForm = ref({
  name: "",
  id: ""
});
const loading = ref(false);
// const TaskListData = ref<Tasklist[]>();

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
        <h1>任务管理</h1>
        <el-button type="primary" @click="createDataset">创建任务</el-button>
      </div>
    </template>
    <!-- <div class="taskbar">
    <div class="tasklistbar">
      <p class="tasktitle">任务名称</p>
      <p class="tasktitle">任务状态</p>
      <el-table
        :show-header="false"
        v-loading="loading"
        :data="TaskListData"
        @row-click="handleRowClick"
      >
        <el-table-column
          class="task"
          key="taskname"
          align="center"
          prop="name"
        />
        <el-table-column
          class="task"
          key="taskstate"
          align="center"
          prop="state"
          border-style:hidden
        />
      </el-table>
    </div> -->
  </el-card>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-table .el-table__row > td {
  border-bottom: none;
}
.basic-container {
  padding-left: 30px;
  padding-right: 15px;
  padding-top: 15px;
}
p {
  margin: 0;
  display: inline-block;
}
td {
  padding-top: 20px;
  padding-right: 10px;
  padding-bottom: 10px;
  max-width: 100%;
  word-wrap: break-word;
  word-break: break-all;
  max-height: 100%;
}
.el-dialog__title {
  font-size: 14px;
  color: grey;
}
.makesure {
  color: rgb(77, 76, 76);
  font-size: 16px;
  text-align: center;
}
.el-form-item {
  margin-right: 50px;
}
</style>
