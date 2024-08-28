<script setup lang="ts">
import { ref, reactive } from "vue";
import { FormProps } from "../utils/types";

const props = withDefaults(defineProps<FormProps>(), {
  formInline: () => ({
    name: "",
    suite_name: "",
    file: null
  })
});

const ruleFormRef = ref();
const newFormInline = reactive(props.formInline);

const rules = {
  name: [{ required: true, message: "请输入数据集名称", trigger: "blur" }],
  suite_name: [{ required: true, message: "请选择测试类型", trigger: "change" }],
  file: [{ required: true, message: "请上传JSON文件", trigger: "change" }]
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
    <el-form-item label="数据集名称" prop="name" >
      <el-input v-model="newFormInline.name" placeholder="请输入数据集名称" />
    </el-form-item>
    <el-form-item label="测试类型" prop="suite_name">
      <el-select v-model="newFormInline.suite_name" placeholder="请选择测试类型">
        <el-option label="逻辑错误测试" value="逻辑错误测试" />
        <el-option label="事实错误测试" value="事实错误测试" />
        <el-option label="偏见测试" value="偏见测试" />
      </el-select>
    </el-form-item>
    <!-- <el-form-item label="上传文件" prop="file">
      <el-upload
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".json"
      >
        <el-button type="primary">选择文件</el-button>
        <template #tip>
          <div class="el-upload__tip">只能上传 JSON 文件</div>
        </template>
      </el-upload>
    </el-form-item> -->
  </el-form>
</template>
