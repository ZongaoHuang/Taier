import "./reset.css";
import dayjs from "dayjs";
import editForm from "../form/index.vue";
import createSetForm from "../form/createSetForm.vue";
import { message } from "@/utils/message";
import { addDialog } from "@/components/ReDialog";
import type { PaginationProps } from "@pureadmin/table";
import type { FormItemProps } from "../utils/types";

import {
  getKeyList,
  deviceDetection
} from "@pureadmin/utils";
import {
  getSetList,
  createSet,
  updateSet,
  deleteSet,
  SetData,
  SetResponse,
  uploadJson
} from "@/api/sjj";
import {
  type Ref,
  h,
  ref,
  toRaw,
  computed,
  reactive,
  onMounted
} from "vue";

export function useSjj(tableRef: Ref) {
  const form = reactive({
    name: "",
    suite: ""
  });
  const formRef = ref();
  const dataList = ref([]);
  const loading = ref(true);
  const switchLoadMap = ref({});
  const selectedNum = ref(0);
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 10,
    currentPage: 1,
    background: true
  });
  const columns: TableColumnList = [
    {
      label: "勾选列", // 如果需要表格多选，此处label必须设置
      type: "selection",
      fixed: "left",
      reserveSelection: true // 数据刷新后保留选项
    },
    {
      label: "创建时间",
      prop: "createTime",
      formatter: ({ createTime }) =>
        dayjs(createTime).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "数据集名称",
      prop: "name",
    },
    {
      label: "测试类型",
      prop: "suite_name",
    },
    {
      label: "规模",
      prop: "question_count"
    },
    {
      label: "操作",
      fixed: "right",
      slot: "operation"
    }
  ];
  const buttonClass = computed(() => {
    return [
      "!h-[20px]",
      "reset-margin",
      "!text-gray-500",
      "dark:!text-white",
      "dark:hover:!text-primary"
    ];
  });

  async function handleUpdate(row: SetData) {
    try {
      const { data } = await updateSet(row);
      if (data.list && data.list.length > 0) {
        message(`数据集更新成功`, { type: "success" });
        onSearch();
      } else {
        message(`更新失败: 未能获取更新后的数据`, { type: "error" });
      }
    } catch (error) {
      console.error("Error updating set:", error);
      message(`更新失败`, { type: "error" });
    }
  }

  async function handleDelete(row) {
    try {
      const { data } = await deleteSet({ id: row.id });
      if (data.list && data.list.length === 0) {
        message(`数据集删除成功`, { type: "success" });
        onSearch();
      } else {
        message(`删除失败: 未能删除数据`, { type: "error" });
      }
    } catch (error) {
      console.error("Error deleting set:", error);
      message(`删除失败`, { type: "error" });
    }
  }

  function handleSizeChange(val: number) {
    pagination.pageSize = val;
    onSearch();
  }

  function handleCurrentChange(val: number) {
    pagination.currentPage = val;
    onSearch();
  }

  /** 当CheckBox选择项发生变化时会触发该事件 */
  function handleSelectionChange(val) {
    selectedNum.value = val.length;
    // 重置表格高度
    tableRef.value.setAdaptive();
  }

    /** 取消选择 */
  function onSelectionCancel() {
    selectedNum.value = 0;
    // 用于多选表格，清空用户的选择
    tableRef.value.getTableRef().clearSelection();
  }

    /** 批量删除 */
    async function onbatchDel() {
      const curSelected = tableRef.value.getTableRef().getSelectionRows();
      const ids = getKeyList(curSelected, "id");
      try {
        const { data } = await deleteSet({ id: ids.join(',') });
        if (data.list && data.list.length === 0) {
          message(`已删除选中的��据集`, { type: "success" });
          tableRef.value.getTableRef().clearSelection();
          onSearch();
        } else {
          message(`批量删除失败: ${response.msg || '未知错误'}`, { type: "error" });
        }
      } catch (error) {
        console.error("Error batch deleting sets:", error);
        message(`批量删除失败: ${error instanceof Error ? error.message : '未知错误'}`, { type: "error" });
      }
    }

  async function onSearch() {
    loading.value = true;
    try {
      const response = await getSetList(toRaw(form));
      if (response.ret === 0 && response.data) {
        dataList.value = response.data.list;
        pagination.total = response.data.total || 0;
        pagination.pageSize = response.data.pageSize || 10;
        pagination.currentPage = response.data.currentPage || 1;
      } else {
        message(`获取数据失败: ${response.msg}`, { type: "error" });
      }
    } catch (error) {
      console.error("Error fetching sets:", error);
      message(`获取数据失败`, { type: "error" });
    } finally {
      loading.value = false;
    }
  }


  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  };

function openCreateSetDialog() {
  addDialog({
    title: "新建数据集",
    width: "50%",
    draggable: true,
    fullscreen: deviceDetection(),
    fullscreenIcon: true,
    closeOnClickModal: false,
    contentRenderer: () => h(createSetForm, { ref: formRef }),
    beforeSure: (done, { options }) => {
      const FormRef = formRef.value.getRef();
      FormRef.validate(async (valid) => {
        if (valid) {
          const formData = new FormData();
          const { newFormInline } = formRef.value;
          formData.append('name', newFormInline.name);
          formData.append('suite_name', newFormInline.suite_name);
          formData.append('file', newFormInline.file);

          try {
            const response = await uploadJson(formData);
            if (response.ret === 0) {
              message("数据集创建成功", { type: "success" });
              done();
              onSearch();
            } else {
              message(`创建失败: ${response.msg}`, { type: "error" });
            }
          } catch (error) {
            console.error("Error creating set:", error);
            message("创建失败", { type: "error" });
          }
        }
      });
    }
  });
}

  function openDialog(row?: FormItemProps) {
    addDialog({
      props: {
        formInline: {
          id: row?.id ?? "",
          name: row?.name ?? "",
          suite_name: row?.suite_name ?? "",
        }
      },
      width: "46%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as FormItemProps;
        FormRef.validate(valid => {
          if (valid) {
            if (curData.id) {
              handleUpdate(curData);
            } else {
              createSet(curData);
            }
            done(); // 关闭弹框
            onSearch(); // 刷新表格数据
          }
        });
      }
    });
  }

  onMounted(async () => {
    onSearch();
  });

  return {
    form,
    dataList,
    loading,
    switchLoadMap,
    selectedNum,
    pagination,
    columns,
    buttonClass,
    onbatchDel,
    onSelectionCancel,
    handleSelectionChange,
    resetForm ,
    deviceDetection,
    handleUpdate,
    handleDelete,
    handleSizeChange,
    handleCurrentChange,
    onSearch,
    openDialog,
    openCreateSetDialog
  };
}
