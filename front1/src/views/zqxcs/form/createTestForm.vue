<template>
    <el-form
      id="createTestForm"
      ref="ruleFormRef"
      :model="newFormInline"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="测试名称" prop="name">
        <el-input v-model="newFormInline.name" placeholder="请输入测试名称" @input="emitFormData" />
      </el-form-item>
      <el-form-item label="数据集" prop="dataset">
        <el-select v-model="newFormInline.dataset" placeholder="请选择数据集" @change="handleDatasetChange">
          <el-option
            v-for="item in datasetOptions"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="测试类型" prop="suite">
        <el-input v-model="newFormInline.suite" disabled />
      </el-form-item>
    </el-form>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, defineProps, defineEmits, watch } from 'vue';
  
  const props = defineProps({
    datasetOptions: {
      type: Array,
      default: () => []
    }
  });
  
  const emit = defineEmits(['submit']);
  
  const newFormInline = reactive({
    name: '',
    suite: '',
    dataset: ''
  });
  
  const rules = {
    name: [{ required: true, message: '请输入测试名称', trigger: 'blur' }],
    dataset: [{ required: true, message: '请选择数据集', trigger: 'change' }]
  };
  
  const handleDatasetChange = (datasetId) => {
  console.log('Selected dataset ID:', datasetId);
  const selectedDataset = props.datasetOptions.find(dataset => dataset.id === datasetId);
  if (selectedDataset) {
    console.log('Selected dataset:', selectedDataset);
    newFormInline.suite = selectedDataset.suite__name;
  }
  emitFormData();
};
  
  const emitFormData = () => {
    emit('submit', { ...newFormInline });
  };
  
  watch(() => props.datasetOptions, (newOptions) => {
    if (newOptions.length > 0 && !newFormInline.dataset) {
      newFormInline.dataset = newOptions[0].id;
      handleDatasetChange(newOptions[0].id);
    }
  }, { immediate: true });
  </script>