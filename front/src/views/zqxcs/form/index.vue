<script setup lang="ts">
import { reactive, ref } from "vue";
import ReCol from "@/components/ReCol";
import { FormProps } from "../utils/types";
import { createFormData } from "@pureadmin/utils";
import { formUpload } from "@/api/mock";
import UploadIcon from "@iconify-icons/ri/upload-2-line";
import { message } from "@/utils/message";


const formRef = ref();
const uploadRef = ref();
const validateForm = reactive({
  fileList: [],
  date: ""
});

const submitForm = formEl => {
  if (!formEl) return;
  formEl.validate(valid => {
    if (valid) {
      // 多个 file 在一个接口同时上传
      const formData = createFormData({
        files: validateForm.fileList.map(file => ({ raw: file.raw })), // file 文件
        date: validateForm.date // 别的字段
      });
      formUpload(formData)
        .then(({ success }) => {
          if (success) {
            message("提交成功", { type: "success" });
          } else {
            message("提交失败");
          }
        })
        .catch(error => {
          message(`提交异常 ${error}`, { type: "error" });
        });
    } else {
      return false;
    }
  });
};

const resetForm = formEl => {
  if (!formEl) return;
  formEl.resetFields();
};

const props = withDefaults(defineProps<FormProps>(), {
  formInline: () => ({
    title: "新增",
    name: "",
    data: "",
    scale: ""
  })
});


const ruleFormRef = ref();
const newFormInline = ref(props.formInline);

function getRef() {
  return ruleFormRef.value;
}

defineExpose({ getRef });
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="newFormInline"
    label-width="82px"
  >
    <el-row :gutter="30">
      <re-col :value="12" :xs="24" :sm="24">
        <el-form-item label="数据集ID" prop="id">
          <el-input
            v-model="newFormInline.id"
            clearable
            placeholder="请输入数据集名称"
          />
        </el-form-item>
      </re-col>
      <re-col :value="12" :xs="24" :sm="24">
        <el-form-item label="数据集名称" prop="name">
          <el-input
            v-model="newFormInline.name"
            clearable
            placeholder="请输入数据集名称"
          />
        </el-form-item>
      </re-col>
      <re-col :value="12" :xs="24" :sm="24">
        <el-form-item label="创建时间" prop="data">
          <el-input
            v-model="newFormInline.data"
            clearable
            placeholder="请输入创建时间"
          />
        </el-form-item>
      </re-col>
      <re-col :value="12" :xs="24" :sm="24">
        <el-form-item label="问题规模" prop="scale">
          <el-input
            v-model="newFormInline.scale"
            clearable
            placeholder="请输入规模"
          />
        </el-form-item>
      </re-col>

      <el-form-item
        label="文件"
        prop="fileList"
        :rules="[{ required: true, message: '附件不能为空' }]"
      >
        <el-upload
          ref="uploadRef"
          v-model:file-list="validateForm.fileList"
          drag
          multiple
          action="#"
          class="!w-[200px]"
          :auto-upload="false"
        >
          <div class="el-upload__text">
            <IconifyIconOffline
              :icon="UploadIcon"
              width="26"
              class="m-auto mb-2"
            />
            可点击或拖拽上传数据集文件
          </div>
        </el-upload>
      </el-form-item>
      <re-col :value="24" :xs="24" :sm="24">
        <el-form-item>
          <el-button type="primary" text bg @click="submitForm(formRef)">
            提交
          </el-button>
          <el-button text bg @click="resetForm(formRef)">重置</el-button>
        </el-form-item>
      </re-col>
    </el-row>
  </el-form>
</template>
