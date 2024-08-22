<script setup lang="ts">
import { ref } from "vue";
import { useSjj } from "./utils/hook";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Upload from "@iconify-icons/ri/upload-line";
import Role from "@iconify-icons/ri/admin-line";
import Password from "@iconify-icons/ri/lock-password-line";
import More from "@iconify-icons/ep/more-filled";
import Delete from "@iconify-icons/ep/delete";
import EditPen from "@iconify-icons/ep/edit-pen";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";

defineOptions({
  name: "Sjjgl"
});

const treeRef = ref();
const formRef = ref();
const tableRef = ref();

const {
  form,
  loading,
  columns,
  dataList,
  selectedNum,
  pagination,
  buttonClass,
  deviceDetection,
  resetForm,
  onSearch,
  openDialog,
  handleUpdate,
  handleDelete
} = useSjj(tableRef);
</script>

<template>
  <div :class="['flex', 'justify-between', deviceDetection() && 'flex-wrap']">
    <div
      :class="[deviceDetection() ? ['w-full', 'mt-2'] : 'w-[calc(100%-200px)]']"
    >
      <el-form
        ref="formRef"
        :inline="true"
        :model="form"
        class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
      >
        <el-form-item label="数据集名称：" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入数据集名称"
            clearable
            class="!w-[180px]"
          />
        </el-form-item>
        <el-form-item label="数据集规模：" prop="scale">
          <el-input
            v-model="form.scale"
            placeholder="请输入数据集规模"
            clearable
            class="!w-[180px]"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :icon="useRenderIcon('ri:search-line')"
            :loading=loading
            @click="onSearch"
          >
            搜索
          </el-button>
          <el-button :icon="useRenderIcon(Refresh)" @click="resetForm(formRef)">
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <PureTableBar
        title="数据集管理"
        :columns="columns"
        @refrash="onSearch"
      >
      <template #buttons>
        <el-button
          type="primary"
          :icon="useRenderIcon(AddFill)"
          @click="openDialog()"
        >
          新增数据集
        </el-button>
      </template>
      <pure-table
        ref="tableRef"
        row-key="id"
        adaptive
        :adaptiveConfig="{ offsetBottom: 108 }"
        align-whole="center"
        table-layout="auto"
        :loading="loading"
        :data="dataList"
        :columns="columns"
        :pagination="pagination"
        :selectedNum="selectedNum"
        @update="handleUpdate"
        @delete="handleDelete"
      >
        <template #operation="{ row }">
          <el-button
            class="reset-margin"
              link
              type="primary"
              :icon="useRenderIcon(EditPen)"
              @click="openDialog(row)"
          >
            修改
          </el-button>
          <el-popconfirm
              :title="`是否确认删除编号为${row.id}的这条数据`"
              @confirm="handleDelete(row)"
            >
            <template #reference>
              <el-button
                class="reset-margin"
                link
                type="primary"
                :icon="useRenderIcon(Delete)"
              >
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </pure-table>
      </PureTableBar>
    </div>
  </div>
</template>

<style scoped lang="scss">
:deep(.el-dropdown-menu__item i) {
  margin: 0;
}

:deep(.el-button:focus-visible) {
  outline: none;
}

.main-content {
  margin: 24px 24px 0 !important;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
