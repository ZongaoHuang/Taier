<script setup lang="ts">
import { ref, reactive } from "vue";

const props = defineProps<{
  setId: number
}>();

const ruleFormRef = ref();
const newFormInline = reactive({
  file: null
});

const rules = {
  file: [{ required: true, message: "请上传文件", trigger: "change" }]
};

const handleFileChange = (file) => {
  newFormInline.file = file.raw;
};

function getRef() {
  return ruleFormRef.value;
}

defineExpose({ getRef, newFormInline });
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="newFormInline"
    :rules="rules"
    label-width="100px"
  >
    <el-form-item label="上传文件" prop="file">
      <el-upload
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".csv,.json"
      >
        <el-button type="primary">选择文件</el-button>
        <template #tip>
          <div class="el-upload__tip">只能上传 CSV 或 JSON 文件</div>
        </template>
      </el-upload>
    </el-form-item>
  </el-form>
</template>