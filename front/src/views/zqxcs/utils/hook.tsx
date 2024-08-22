import "./reset.css";
import dayjs from "dayjs";
import editForm from "../form/index.vue";
import { message } from "@/utils/message";
import { addDialog } from "@/components/ReDialog";
import type { PaginationProps } from "@pureadmin/table";
import type { FormItemProps} from "../utils/types";
import {
  getKeyList,
  deviceDetection
} from "@pureadmin/utils";
import {
  getSjj
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
    id: "",
    name: "",
    scale: "",
    data: ""
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
      label: "数据集ID",
      prop: "id",
      width: 90
    },
    {
      label: "数据集名称",
      prop: "name",
      minWidth: 130
    },
    {
      label: "数据集规模",
      prop: "scale",
      minWidth: 130
    },
    {
      label: "创建时间",
      minWidth: 90,
      prop: "createTime",
      formatter: ({ createTime }) =>
        dayjs(createTime).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "操作",
      fixed: "right",
      width: 180,
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
  function handleUpdate(row) {
    console.log(row);
  }

  function handleDelete(row) {
    message(`您删除了用户编号为${row.id}的这条数据`, { type: "success" });
    onSearch();
  }

  function handleSizeChange(val: number) {
    console.log(`${val} items per page`);
  }

  function handleCurrentChange(val: number) {
    console.log(`current page: ${val}`);
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
  function onbatchDel() {
    // 返回当前选中的行
    const curSelected = tableRef.value.getTableRef().getSelectionRows();
    // 接下来根据实际业务，通过选中行的某项数据，比如下面的id，调用接口进行批量删除
    message(`已删除用户编号为 ${getKeyList(curSelected, "id")} 的数据`, {
      type: "success"
    });
    tableRef.value.getTableRef().clearSelection();
    onSearch();
  }

  async function onSearch() {
    loading.value = true;
    const { data } = await getSjj(toRaw(form));
    dataList.value = data.list;
    pagination.total = data.total;
    pagination.pageSize = data.pageSize;
    pagination.currentPage = data.currentPage;

    setTimeout(() => {
        loading.value = false;
      }, 500);
  }


  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    form.id = "";
    onSearch();
  };

  function openDialog(row?: FormItemProps) {
    addDialog({
      props: {
        formInline: {
          id: row?.id ?? "",
          name: row?.name ?? "",
          scale: row?.scale ?? "",
          data: row?.data ?? "",
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
        function chores() {
          message(`您增加了数据集名称为${curData.name}的这条数据`, {
            type: "success"
          });
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
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
    openDialog
  };
}
