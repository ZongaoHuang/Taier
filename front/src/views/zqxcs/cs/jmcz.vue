<script setup lang='ts'>
import { ref, markRaw } from "vue";
import ReCol from "@/components/ReCol";

import { ReNormalCountTo } from "@/components/ReCountTo";

import { ChartBar, ChartLine, ChartRound, ChartPie } from "./components/charts";

import { chartData, barChartData, progressData, latestNewsData, testData } from "./data";

import { ElMessageBox, ElMessage } from "element-plus";
defineOptions({
  name: 'jmcz'
})

const columns: TableColumnList=[
  {
    label: "测试名称",
    prop: "name"
  },
  {
    label: "测试状态",
    prop: "state"
  }
];

const columns1: TableColumnList=[
  {
    label: "测试名称",
    prop: "name"
  },
  {
    label: "目标模型",
    prop: "model"
  },
  {
    label: "数据集",
    prop: "dataset"
  },
  {
    label: "测试类型",
    prop: "type"
  },
  {
    label: "状态",
    prop: "state"
  },
  {
    label: "测试率",
    prop: "rate"
  }
];

const columns2: TableColumnList=[
  {
    label: "创建时间",
    prop:"date"
  },
  {
    label: "测试名称",
    prop: "name"
  },
  {
    label: "目标模型",
    prop: "model"
  },
  {
    label: "数据集",
    prop: "dataset"
  },
  {
    label: "测试类型",
    prop: "type"
  },
  {
    label: "状态",
    prop: "state"
  },
  {
    label: "测试率",
    prop: "rate"
  }
];

// 用于存储当前选中的测试详情
const selectedTest = ref(null);

// 处理表格行点击事件
function handleRowClick(row) {
  selectedTest.value = [row];
}

// 显示创建测试对话框
function showCreateTestDialog() {
  ElMessageBox.prompt('请填写测试信息', '创建测试', {
    confirmButtonText: '创建',
    cancelButtonText: '取消',
    inputPattern: /\S+/,
    inputErrorMessage: '测试信息不能为空'
  }).then(({ value }) => {
    ElMessage({
      type: 'success',
      message: `测试 "${value}" 已创建`
    });
  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '取消创建测试'
    });
  });
}

// 执行测试
function executeTest() {
  if (selectedTest.value) {
    ElMessage({
      type: 'success',
      message: `测试 "${selectedTest.value[0].name}" 已执行`
    });
  } else {
    ElMessage({
      type: 'warning',
      message: '请先选择一个测试'
    });
  }
}

// 删除测试
function deleteTest() {
  if (selectedTest.value) {
    ElMessageBox.confirm(`确定要删除测试 "${selectedTest.value[0].name}" 吗？`, '删除测试', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(() => {
      ElMessage({
        type: 'success',
        message: `测试 "${selectedTest.value[0].name}" 已删除`
      });
      selectedTest.value = null; // 删除后清空选中的测试
    }).catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除'
      });
    });
  } else {
    ElMessage({
      type: 'warning',
      message: '请先选择一个测试'
    });
  }
}

function exportTestResult() {
  if (selectedTest.value) {
    ElMessage({
      type: 'success',
      message: `测试 "${selectedTest.value[0].name}" 结果已导出`
    });
  } else {
    ElMessage({
      type: 'warning',
      message: '请先选择一个测试'
    });
  }
}
</script>



<template>
  <div>
    <el-row :gutter="24" justify="space-around">
      <re-col
        v-for="(item, index) in chartData"
        :key="index"
        v-motion
        class="mb-[18px]"
        :value="6"
        :md="12"
        :sm="12"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 80 * (index + 1)
          }
        }"
      >
        <el-card class="line-card" shadow="never">
          <div class="flex justify-between">
            <span class="text-md font-medium">
              {{ item.name }}
            </span>
            <div
              class="w-8 h-8 flex justify-center items-center rounded-md"
              :style="{
                backgroundColor: isDark ? 'transparent' : item.bgColor
              }"
            >
              <IconifyIconOffline
                :icon="item.icon"
                :color="item.color"
                width="18"
              />
            </div>
          </div>
          <div class="flex justify-between items-start mt-3">
            <!-- 将宽度减少到1/3 -->
            <div class="w-1/3 flex flex-col justify-center">
              <ReNormalCountTo
                :duration="item.duration"
                :fontSize="'1.6em'"
                :startVal="100"
                :endVal="item.value"
              />
              <p v-if="item.name === '准确度平均值'" class="font-medium text-green-500">
                {{ item.value }}%
              </p>
            </div>

            <!-- 将饼图的宽度增加到2/3 -->
            <div class="w-2/3 flex justify-center items-center">
              <ChartLine
                v-if="item.data.length > 1 && typeof item.data[0] === 'number'"
                class="!w-full"
                :color="item.color"
                :data="item.data"
              />
              <ChartPie
                v-else-if="typeof item.data[0] === 'object'"
                class="!w-full"
                :color="item.color"
                :data="item.data"
              />
              <ChartRound
                v-else
                class="!w-full"
                :data="item.data"
              />
            </div>
          </div>
        </el-card>
      </re-col>


      <re-col
        v-motion
        class="mb-[18px]"
        :value="6"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 480
          }
        }"
      >
        <el-card shadow="never">
          <div class="flex justify-between">
            <span class="text-md font-bold">近期测试列表</span>
            <el-button type="primary" @click="showCreateTestDialog">创建测试</el-button>
          </div>
          <el-card shadow="never" class="h-[200px]">
            <pure-table :data="testData" :columns="columns" @row-click="handleRowClick" />
          </el-card>
        </el-card>
      </re-col>

      <re-col
        v-motion
        class="mb-[18px]"
        :value="18"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 400
          }
        }"
      >
        <el-card class="bar-card" shadow="never">
          <div class="flex justify-between">
            <span class="text-md font-bold">测试详情</span>
          </div>
            <el-card shadow="never" class="h-[200px]">
              <div v-if="selectedTest">
                <pure-table :data="selectedTest" :columns="columns1" />
              </div>
            <div v-else>
              <p>请选择一个测试来查看详情。</p>
            </div>

            <div class="flex justify-start items-center gap-2 mt-4"> <!-- 将按钮放在表格下方 -->
              <el-button type="primary" @click="executeTest">执行测试</el-button>
              <el-button type="danger" @click="deleteTest">删除测试</el-button>
              <el-button type="success" @click="exportTestResult">导出测试结果</el-button>
            </div>
          </el-card>
        </el-card>
      </re-col>



      <re-col
        v-motion
        class="mb-[18px]"
        :value="24"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 560
          }
        }"
      >
        <el-card shadow="never" class="h-[400px]">
          <div class="flex justify-between">
            <span class="text-md font-bold">测试总览</span>
          </div>
          <el-card shadow="never" class="h-[200px]">
            <pure-table :data="testData" :columns="columns2"  />
          </el-card>
        </el-card>
      </re-col>

    </el-row>
  </div>
</template>

<style lang="scss" scoped>

:deep(.el-button:focus-visible) {
  outline: none;
}

:deep(.el-card) {
  --el-card-border-color: none;

  /* 解决概率进度条宽度 */
  .el-progress--line {
    width: 85%;
  }

  /* 解决概率进度条字体大小 */
  .el-progress-bar__innerText {
    font-size: 15px;
  }

  /* 隐藏 el-scrollbar 滚动条 */
  .el-scrollbar__bar {
    display: none;
  }

  /* el-timeline 每一项上下、左右边距 */
  .el-timeline-item {
    margin: 0 6px;
  }
}

.main-content {
  margin: 20px 20px 0 !important;
}
</style>

