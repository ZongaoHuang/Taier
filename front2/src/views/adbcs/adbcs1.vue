<script setup lang="ts">
import { ref, watch } from "vue";
import { ElMessage } from "element-plus";
import axios from "axios";
import { Icon } from "@iconify/vue";
import TestTypeIcon from "@iconify-icons/ep/reading";
import PhoneIcon from "@iconify-icons/ep/phone";

defineOptions({
  name: "TestSelection"
});

const phoneModels = [
  { label: "OPPO Find X7", value: "oppo" },
  { label: "OnePlus 12", value: "oneplus" },
];

const testTypeOptions = [
  { label: "算法安全性测试", value: "security" },
  { label: "算法准确性测试", value: "accuracy" },
  { label: "算法隐私性测试", value: "privacy" },
];

const selectedPhoneModel = ref("");
const selectedTestType = ref("");
const sampleCount = ref(0);
const testSampleCount = ref("");
const phoneModelInfo = ref("");

const testInProgress = ref(false);
const testCompleted = ref(false);

watch(selectedPhoneModel, (newModel) => {
  if (newModel === "oppo") {
    phoneModelInfo.value = "您选择了 OPPO Find X7，请打开至小布助手，并进入对话框，确保键盘选择ADB Keyboard，即可开始测试！";
  } else if (newModel === "oneplus") {
    phoneModelInfo.value = "您选择了 OnePlus 12，请打开至小布助手，并进入对话框，确保键盘选择ADB Keyboard，即可开始测试！";
  } else {
    phoneModelInfo.value = "";
  }
});

const updateSampleCount = () => {
  if (selectedTestType.value === "security") {
    sampleCount.value = 5000;
  } else if (selectedTestType.value === "accuracy") {
    sampleCount.value = 14228;
  } else if (selectedTestType.value === "privacy") {
    sampleCount.value = 5000;
  } else {
    sampleCount.value = 0;
  }
};

const handleSelection = async () => {
  if (!selectedPhoneModel.value) {
    ElMessage.warning("请选择手机型号");
    return;
  }
  if (!selectedTestType.value) {
    ElMessage.warning("请选择测试类型");
    return;
  }
  if (!testSampleCount.value || isNaN(Number(testSampleCount.value)) || Number(testSampleCount.value) <= 0) {
    ElMessage.warning("请输入有效的测试数量");
    return;
  }

  testInProgress.value = true;
  testCompleted.value = false;

  try {
    const response = await axios.post("http://127.0.0.1:8877/api/run-test/", {
      phoneModel: selectedPhoneModel.value,
      testType: selectedTestType.value,
      sampleCount: Number(testSampleCount.value)
    });

    if (response.data.success) {
      testInProgress.value = false;
      testCompleted.value = true;
      ElMessage.success("测试任务已完成！");
    } else {
      ElMessage.error("测试任务提交失败，请稍后重试");
    }
  } catch (error) {
    ElMessage.error("请求失败：" + error.message);
  }
};

const downloadTestLog = async () => {
  if (!selectedTestType.value) {
    ElMessage.warning("请选择测试类型");
    return;
  }

  try {
    const response = await axios.get("http://127.0.0.1:8877/api/download-log/", {
      params: { testType: selectedTestType.value },
      responseType: "blob"
    });

    const blob = new Blob([response.data], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = `${selectedTestType.value}_test_log.txt`;
    link.click();

    ElMessage.success("日志文件下载成功！");
  } catch (error) {
    ElMessage.error("文件下载失败：" + error.message);
  }
};
</script>

<template>
  <div class="main-content">
    <el-card shadow="never" class="mb-6">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <Icon :icon="PhoneIcon" class="mr-2" width="24" />
          <span class="text-md font-bold">选择手机型号</span>
        </div>
      </div>
      <div class="mt-4">
        <el-form :inline="true" class="search-form bg-bg_color w-full pl-8 pt-4">
          <el-form-item label="手机型号：" prop="phoneModel">
            <el-select
              v-model="selectedPhoneModel"
              placeholder="请选择手机型号"
              clearable
              class="!w-[180px]"
            >
              <el-option
                v-for="item in phoneModels"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-form>
        <p v-if="phoneModelInfo">{{ phoneModelInfo }}</p>
      </div>
    </el-card>

    <el-card shadow="never" class="mb-6">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <Icon :icon="TestTypeIcon" class="mr-2" width="24" />
          <span class="text-md font-bold">选择测试类型</span>
        </div>
      </div>
      <div class="mt-4">
        <el-form :inline="true" class="search-form bg-bg_color w-full pl-8 pt-4">
          <el-form-item label="测试类型：" prop="testType">
            <el-select
              v-model="selectedTestType"
              placeholder="请选择测试类型"
              clearable
              class="!w-[180px]"
              @change="updateSampleCount"
            >
              <el-option
                v-for="item in testTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item v-if="selectedTestType">
            <p>数据集中的样本数: {{ sampleCount }}，请输入测试数量：</p>
            <el-input
              v-model.number="testSampleCount"
              placeholder="请输入测试数量"
              class="!w-[180px]"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSelection" :disabled="testInProgress">确认选择</el-button>
            <el-button v-if="testCompleted" type="success" @click="downloadTestLog">下载日志文件</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <div v-if="testInProgress" class="test-status">测试进行中...</div>
    <div v-if="testCompleted && !testInProgress" class="test-status">测试完毕，请点击下载日志文件</div>
  </div>
</template>

<style scoped lang="scss">
.main-content {
  margin: 20px;
}

.search-form {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 8px;
}

.el-button {
  margin-left: 10px;
}

.test-status {
  margin-top: 20px;
  font-size: 18px;
  color: #409EFF;
}
</style>
