<script setup lang='ts'>
import { ref, onMounted, computed, h, defineComponent } from "vue";
import ReCol from "@/components/ReCol";

import { ReNormalCountTo } from "@/components/ReCountTo";

import { ChartBar, ChartLine, ChartRound, ChartPie, ChartGauge } from "./components/charts";

import GroupLine from "@iconify-icons/ep/document";
import Question from "@iconify-icons/ep/document-checked";
import CheckLine from "@iconify-icons/ep/data-board";
import Smile from "@iconify-icons/ri/star-smile-line";
import CreateTestForm from '../form/createTestForm.vue';

import {
  getTestList,
  TestData,
  getRecentTests,
  createTest,
  getDatasets,
  getSuites,
  getTestDetails,
  executeTest,
  deleteTest,
  downloadTestResults,
  getTestStatus
} from "@/api/csgj2";

import { ElMessageBox, ElMessage, ElPagination, ElNotification } from "element-plus";
defineOptions({
  name: 'jmcz2'
})


// 图表展示
const chartData = ref([
  {
    icon: GroupLine,
    bgColor: "#effaff",
    color: "#41b6ff",
    duration: 2200,
    name: "测试例数",
    value: 0,
    data: [2101, 5288, 4239, 4962, 6752, 5208, 7450]
  },
  {
    icon: Question,
    bgColor: "#fff5f4",
    color: "#e85f33",
    duration: 1600,
    name: "测试完成条数",
    value: 0,
    data: [2101, 5288, 4239, 4962, 6752, 5208, 7450]
  },
  {
    icon: CheckLine,
    bgColor: "#eff8f4",
    color: "#26ce83",
    duration: 4,
    name: "测试类型",
    value: 4,
    data: [
      { label: "越狱测试", value: 40 },
      { label: "目标劫持测试", value: 30 },
      { label: "泄露测试", value: 20 },
      { label: "等效绕过测试", value: 20 },
    ] // 饼状图数据
  },
  {
    icon: Smile,
    bgColor: "#f6f4fe",
    color: "#7846e5",
    duration: 1000 ,
    name: "平均攻击成功率",
    value: (0).toFixed(2),
    data: [],
    suffix: '%'
  }
]);


// 测试总览
const testData = ref<TestData[]>([]);
const currentPage = ref(1);
const pageSize = ref(7);

const paginatedTestData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return testData.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(testData.value.length / pageSize.value));

const updateChartData = () => {
  if (testData.value.length > 0) {
    chartData.value[0].value = testData.value.length;
    chartData.value[1].value = testData.value.filter(test => test.state === 'finished').length;

    const uniqueTypes = [...new Set(testData.value.map(test => test.type))];
    chartData.value[2].value = uniqueTypes.length;
    chartData.value[2].data = uniqueTypes.map(type => ({
      label: type,
      value: testData.value.filter(test => test.type === type).length
    }));

    const finishedTests = testData.value.filter(test => test.state === 'finished');
    if (finishedTests.length > 0) {
      const avgAccuracy = finishedTests.reduce((sum, test) => {
        const escapeRate = parseFloat(test.escape_rate);
        return isNaN(escapeRate) ? sum : sum + (escapeRate);
      }, 0) / finishedTests.length;
      chartData.value[3].value = avgAccuracy.toFixed(2);
    } else {
      chartData.value[3].value = "0.00";
    }
  }
};

const fetchTestData = async () => {
  try {
    const response = await getTestList();
    if (response.ret === 0 && response.tests) {
      testData.value = response.tests
        .filter(item =>
          ["越狱测试", "目标劫持测试", "泄露测试", "等效绕过测试"].includes(item.type)
        )
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .map(test => ({
          ...test,
          accuracy: (100 - parseFloat(test.escape_rate)).toFixed(2)
        }));
      updateChartData();
    } else {
      ElMessage.error(response.msg || "Failed to fetch test data");
    }
  } catch (error) {
    console.error("Error fetching test data:", error);
    ElMessage.error("Error fetching test data");
  }
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
};

// 近期测试
const recentTests = ref<TestData[]>([]);

const fetchRecentTests = async () => {
  try {
    const response = await getRecentTests();
    if (response.ret === 0 && response.tests) {
      recentTests.value = response.tests
        .filter(item => ["越狱测试", "目标劫持测试", "泄露测试", "等效绕过测试"].includes(item.type))
        .slice(0, 3);
    } else {
      ElMessage.error(response.msg || "Failed to fetch recent tests");
    }
  } catch (error) {
    console.error("Error fetching recent tests:", error);
    ElMessage.error("Error fetching recent tests");
  }
};

const createNewTest = async () => {
  try {
    const datasetsResponse = await getDatasets();
    console.log('datasetsResponse:', datasetsResponse);

    if (datasetsResponse.ret !== 0) {
      ElMessage.error("Failed to fetch datasets");
      return;
    }

    const datasets = datasetsResponse.datasets || [];
    console.log('datasets:', datasets);

    if (datasets.length === 0) {
      ElMessage.error("No datasets available");
      return;
    }

    let formData = null;

    ElMessageBox({
      title: '创建新测试',
      message: h(CreateTestForm, {
        datasetOptions: datasets,
        onSubmit: (data) => {
          formData = data;
        }
      }),
      showCancelButton: true,
      confirmButtonText: '创建',
      cancelButtonText: '取消',
      beforeClose: (action, instance, done) => {
        if (action === 'confirm') {
          if (!formData || !formData.name || !formData.dataset || !formData.suite) {
            ElMessage.warning('请填写所有必要信息');
            return;
          }
          instance.confirmButtonLoading = true;
          console.log('Form data before creating test:', formData);
          createTest({
            name: formData.name,
            suite: formData.suite,
            dataset: formData.dataset,
            model: 'gpt-3.5-turbo',
            evaluator: 'gpt-3.5-turbo'
          }).then(response => {
            instance.confirmButtonLoading = false;
            if (response.ret === 0) {
              ElMessage.success('测试创建成功');
              fetchRecentTests();
              fetchTestData();
              done();
            } else {
              ElMessage.error(response.msg || '测试创建失败');
            }
          }).catch(error => {
            instance.confirmButtonLoading = false;
            ElMessage.error('Error creating test: ' + error.message);
          });
        } else {
          done();
        }
      }
    }).catch(() => {
      ElMessage.info('取消创建测试');
    });
  } catch (error) {
    console.error('Error creating test:', error);
    ElMessage.error('Error creating test');
  }
};

onMounted(() => {
  fetchRecentTests();
  fetchTestData();
});

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
    label: "算法攻击成功率",
    prop: "escape_rate"
  }
];

const columns2: TableColumnList = [
  {
    label: "创建时间",
    prop: "created_at"
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
    label: "算法攻击成功率（%）",
    prop: "escape_rate"
  }
];

// 用于存储当前选中的测试详情
const selectedTest = ref(null);
const testDetails = ref(null);

// 处理表格行点击事件
async function handleRecentTestClick(row) {
  try {
    // Assuming the row object has a 'name' property instead of 'id'
    const response = await getTestDetails(row.name);
    if (response.ret === 0) {
      selectedTest.value = [response.data];
    } else {
      ElMessage.error(response.msg || "Failed to fetch test details");
    }
  } catch (error) {
    console.error("Error fetching test details:", error);
    ElMessage.error("Error fetching test details");
  }
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

const checkTestStatus = async (testName: string) => {
  try {
    const response = await getTestStatus(testName);
    if (response.ret === 0) {
      if (response.state === 'finished') {
        ElNotification({
          title: '测试执行完成',
          message: `测试已完成，逃逸率: ${response.escape_rate}`,
          type: 'success'
        });
        await fetchTestData();
        await fetchRecentTests();
        return true;
      } else if (response.state === 'running') {
        return false;
      } else {
        ElNotification({
          title: '测试执行失败',
          message: '测试执行过程中出现错误',
          type: 'error'
        });
        return true;
      }
    }
    return true;
  } catch (error) {
    console.error('Error checking test status:', error);
    ElNotification({
      title: '错误',
      message: '检查测试状态时发生错误',
      type: 'error'
    });
    return true;
  }
};

// 执行测试
const executeTestFunction = async () => {
  if (selectedTest.value) {
    try {
      const notification = ElNotification({
        title: '测试执行中',
        message: '请稍候...',
        duration: 0,
        type: 'info'
      });

      const response = await executeTest(selectedTest.value[0].name);

      if (response.ret === 0) {
        // Update the test status in the frontend
        selectedTest.value[0].state = 'running';
        await fetchTestData();
        await fetchRecentTests();

        const checkStatus = async () => {
          const isCompleted = await checkTestStatus(selectedTest.value[0].name);
          if (!isCompleted) {
            setTimeout(checkStatus, 5000); // Check every 5 seconds
          } else {
            notification.close();
            await fetchTestData();
            await fetchRecentTests();
          }
        };
        checkStatus();
      } else {
        notification.close();
        ElNotification({
          title: '测试执行失败',
          message: response.msg || '执行测试失败',
          type: 'error'
        });
      }
    } catch (error) {
      console.error('Error executing test:', error);
      ElNotification({
        title: '错误',
        message: '执行测试时发生错误',
        type: 'error'
      });
    }
  } else {
    ElMessage.warning('请先选择一个测试');
  }
};

// 删除测试
const deleteTestFunction = async () => {
  if (selectedTest.value) {
    try {
      const confirmResult = await ElMessageBox.confirm(
        `确定要删除测试 "${selectedTest.value[0].name}" 吗？`,
        '删除测试',
        {
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'warning',
        }
      );

      if (confirmResult === 'confirm') {
        const response = await deleteTest(selectedTest.value[0].name);
        if (response.ret === 0) {
          ElMessage.success(response.msg || '测试删除成功');
          selectedTest.value = null;
          await fetchTestData();
          await fetchRecentTests();
        } else {
          ElMessage.error(response.msg || '删除测试失败');
        }
      }
    } catch (error) {
      if (error !== 'cancel') {
        console.error('Error deleting test:', error);
        ElMessage.error('删除测试时发生错误');
      }
    }
  } else {
    ElMessage.warning('请先选择一个测试');
  }
};

const exportTestResult = async () => {
  if (selectedTest.value) {
    try {
      const response = await downloadTestResults(selectedTest.value[0].name);
      const blob = new Blob([response], { type: 'application/json' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${selectedTest.value[0].name}_result.json`;
      link.click();
      URL.revokeObjectURL(link.href);
      ElMessage.success('测试结果已成功导出');
    } catch (error) {
      console.error('Error exporting test result:', error);
      ElMessage.error('导出测试结果时发生错误');
    }
  } else {
    ElMessage.warning('请先选择一个测试');
  }
};



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
            >
              <IconifyIconOffline
                :icon="item.icon"
                :color="item.color"
                width="18"
              />
            </div>
          </div>
          <div class="flex justify-between items-start mt-3">
            <div class="w-1/3 flex flex-col justify-center">
              <ReNormalCountTo
                :duration="item.duration"
                :fontSize="'1.6em'"
                :startVal="0"
                :endVal="item.value"
                :suffix="item.suffix"
              />
            </div>
            <div class="w-2/3 flex justify-center items-center">
              <ChartLine
                v-if="index < 2"
                class="!w-full"
                :color="item.color"
                :data="item.data"
              />
              <ChartPie
                v-else-if="index === 2"
                class="!w-full"
                :color="item.color"
                :data="item.data"
              />
              <ChartGauge
                v-else
                class="!w-full"
                :data="item.data"
                :value="item.value"
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
        <el-card shadow="never" class="mt-4">
          <div class="flex justify-between mb-4">
            <span class="text-md font-bold">近期测试列表</span>
            <el-button type="primary" @click="createNewTest">创建测试</el-button>
          </div>
          <el-card shadow="never" class="h-[160px]">
          <el-table :data="recentTests" style="width: 100%" @row-click="handleRecentTestClick">
            <el-table-column prop="name" label="测试名称" />
            <el-table-column prop="state" label="测试状态" />
          </el-table>
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
            delay: 480
          }
        }"
      >
        <el-card class="mt-4" shadow="never">
          <div class="flex justify-between mb-4">
            <span class="text-md font-bold">测试详情</span>
          </div>
          <el-card shadow="never" class="h-[168px]">
            <div v-if="selectedTest && selectedTest.length > 0">
              <pure-table :data="selectedTest" :columns="columns1" />
            </div>
            <div v-else>
              <p>请选择一个测试来查看详情。</p>
            </div>

            <div class="flex justify-start items-center gap-2 mt-4"> <!-- 将按钮放在表格下方 -->
              <el-button type="primary" @click="executeTestFunction">执行测试</el-button>
              <el-button type="danger" @click="deleteTestFunction">删除测试</el-button>
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
      <el-card shadow="never" class="h-[460px] overflow-hidden">
  <div class="flex justify-between mb-4">
    <span class="text-md font-bold">测试总览</span>
  </div>
  <div class="overflow-auto" style="max-height: 400px;">
    <pure-table
      :data="paginatedTestData"
      :columns="columns2"
      :header-cell-style="{
        background: 'var(--el-fill-color-light)',
        color: 'var(--el-text-color-primary)'
      }"
    />
  </div>
  <div class="flex justify-center mt-4">
    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="testData.length"
      @current-change="handlePageChange"
      layout="prev, pager, next"
    />
  </div>
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

:deep(.pure-table) {
  width: 100%;
  table-layout: auto;
}

:deep(.pure-table .el-table__body) {
  width: 100% !important;
}
</style>

@/api/csgj1
