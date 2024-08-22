<template>
  <div class="background">
    <div class="titlebar">
      <p class="title">任务管理</p>
      <div class="titlebarrightbutton">
        <button @click="handleTaskCreate" class="taskCreateButton">
          任务创建
        </button>
      </div>
    </div>
    <div class="taskbar">
      <div class="tasklistbar">
        <p class="tasktitle">任务名称</p>
        <p class="tasktitle">任务状态</p>
        <el-table
          :show-header="false"
          v-loading="loading"
          :data="TaskListData"
          @row-click="handleRowClick"
        >
          <el-table-column
            class="task"
            key="taskname"
            align="center"
            prop="name"
          />
          <el-table-column
            class="task"
            key="taskstate"
            align="center"
            prop="state"
            border-style:hidden
          />
        </el-table>
      </div>
      <div class="taskInfobar">
        <router-view v-if="taskIsSelected">
          <div class="basic-container">
            <p class="taskInfoTitle">任务详情：</p>
            <div class="taskInfobarrightbutton">
              <button @click="taskexec" class="taskCreateButton">
                任务执行
              </button>
              <button @click="handleTaskDelete" class="taskdeleteButton">
                删除
              </button>
            </div>
          </div>
          <div class="taskInfo">
            <div class="taskInfoUp">
              <p class="span1">{{ Task_name }}</p>
              <p class="span2">当前状态：{{ taskInfo?.state || "" }}</p>
              <p class="span3">越狱率：{{ taskInfo?.escapeRate || "" }}</p>
              <div class="span4" v-if="finished">
                <button @click="resultDownload">结果下载</button>
              </div>
            </div>
            <div class="divide-lightgrey"></div>
            <div class="taskInfoDown">
              <div class="taskModel">
                <thead font-550>目标模型</thead>
                <td>{{ taskInfo?.model || "" }}</td>
              </div>
              <div class="taskDataset">
                <thead font-550>数据集</thead>
                <td>{{ taskInfo?.collection || "" }}</td>
              </div>
              <div v-bind="taskInfo" class="taskEval">
                <thead font-550>评估器</thead>
                <td>{{ taskInfo?.evaluator || "" }}</td>
              </div>
              <div class="taskAttackType">
                <thead font-550>攻击类型</thead>
                <td>{{ taskInfo?.cate || "" }}</td>
              </div>
            </div>
          </div>
        </router-view>
      </div>
    </div>
    <el-dialog
      v-model="TaskDeleDialog.visible"
      :title="TaskDeleDialog.title"
      width="500px"
      @close="CloseTaskDeleDialog"
    >
      <div class="makesure">
        <p>是否确定删除任务：{{ Task_name }} ?</p>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="taskdele">确 定</el-button>
          <el-button @click="CloseTaskDeleDialog">取 消</el-button>
        </div>
      </template>
    </el-dialog>
    <el-dialog
      v-model="TaskCreateDialog.visible"
      :title="TaskCreateDialog.title"
      width="600px"
      @close="CloseTaskDeleDialog"
    >
      <el-form
        ref="TaskFormRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="taskname">
          <el-input
            v-model="formData.taskname"
            placeholder="请输入任务名称"
            maxlength="15"
          />
        </el-form-item>
        <el-form-item label="测试名称" prop="testname">
          <el-select v-model="formData.testname">
            <el-option
              v-for="test in Test_list"
              :key="test.name"
              :label="test.name"
              :value="test.name"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <!-- <el-table :data="Test_list">
        <el-table-column key="model" align="center" prop="model" />
        <el-table-column key="collection" align="center" prop="evaluator" />
        <el-table-column key="evaluator" align="center" prop="evaluator" />
      </el-table> -->
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="taskcreate">确 定</el-button>
          <el-button @click="CloseTaskCreateDialog">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "TaskManage",
  inheritAttrs: false,
});
import { ref } from "vue";
import MenuAPI, { MenuQuery, MenuForm, MenuVO } from "@/api/menu";
import { MenuTypeEnum } from "@/enums/MenuTypeEnum";
import TaskAPI, { TaskInfo, Tasklist, TestInfo } from "@/api/taskmanage";
//import { useSettingsStore, useTagsViewStore } from "@/store";
//const cachedViews = computed(() => useTagsViewStore().cachedViews); // 缓存页面
const TaskListData = ref<Tasklist[]>();
const loading = ref(false);
const taskIsSelected = ref(false);
const taskInfo = ref<TaskInfo>();
const Task_name = ref<string | undefined>();
const Suite_name = "testSuite";
const Test_name = "test1";
const finished = ref(false);
const resultDownloadURL = ref<string | undefined>();
const TaskFormRef = ref(ElForm);
const Test_list = ref<TestInfo[] | undefined>();
const Test_list_length = ref<number>();
const formData = reactive({
  taskname: "",
  testname: "",
});
const rules = reactive({
  taskname: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
  testname: [{ required: true, message: "请选择测试名称", trigger: "blur" }],
});
function taskcreate() {
  TaskFormRef.value.validate((valid: any) => {
    if (valid) {
      TaskAPI.TaskCreate({
        Suite_name: Suite_name,
        Test_name: formData.testname,
        Task_name: formData.taskname,
      })
        .then((response: any) => {
          CloseTaskCreateDialog();
          ElMessage.success("任务创建成功");
          fetchData();
        })
        .catch((err: any) => {
          console.info("TaskDele error", err);
          ElMessage.error("任务创建失败！");
        });
    }
  });
}
function taskdele() {
  TaskAPI.TaskDele({ Task_name: Task_name.value })
    .then((response: any) => {
      console.info("TaskDele result:", response);
      ElMessage.success("任务删除成功");
      fetchData();
    })
    .catch((err: any) => {
      console.info("TaskDele error", err);
      ElMessage.error("任务删除失败！");
    })
    .finally(() => {
      CloseTaskDeleDialog();
    });
}
function taskexec() {
  TaskAPI.TaskExec({ Task_name: Task_name.value })
    .then((response: any) => {
      ElMessage.success("任务执行成功");
      console.info("TaskExec result:", response);
    })
    .catch((err: any) => {
      ElMessage.error("任务执行失败！");
      console.info("TaskExec error", err);
    });
}
async function resultDownload() {
  await TaskAPI.TaskResult({ Task_name: Task_name.value })
    //.then((URL) => {
    //resultDownloadURL.value = URL;
    //console.info("TaskResultDownloadURL： ", URL.data);
    //URL.data.text();
    // const link = document.createElement("a");
    // link.href = resultDownloadURL.value || "";
    // link.download = Task_name.value || "";
    // document.body.appendChild(link);
    // link.click();
    // document.body.removeChild(link);
    // // Download_Name.value = Task_name.value + ".html";
    //fetch(resultDownloadURL.value || "")
    //.then((response) => response.data.text()) // 获取页面内容
    .then((response: { data: any; }) => {
      const json = response.data;
      const blob = new Blob([JSON.stringify(json)], {
        type: "application/json",
      });
      const link = document.createElement("a");
      const url = window.URL.createObjectURL(blob);
      link.href = url;
      link.download = Task_name.value + ".json" || "download.json"; // 设置下载文件名
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    })
    .catch((err: any) => {
      ElMessage.error("下载失败！");
      console.info("Fetch error", err);
    });
  //})
  // .catch((err) => {
  //   ElMessage.error("下载失败！");
  //   console.info("TaskResultDownload error", err);
  // });
}

async function handleRowClick(row: Tasklist) {
  Task_name.value = row.name;
  taskIsSelected.value = true;
  await TaskAPI.gettaskinfo({ Task_name: Task_name.value })
    .then((data: { data: { Task_Info: any[]; }; }) => {
      taskInfo.value = data.data.Task_Info[0];
      console.info("taskInfo.value: ", taskInfo.value);
      const finish = taskInfo.value?.state || undefined;
      if (finish == "finished") {
        finished.value = true;
      } else {
        finished.value = false;
      }
    })
    .catch((err: any) => {
      ElMessage.error("任务信息获取失败！");
      console.info(" handleRowClick error", err);
    });
  fetchData();
}

function fetchData() {
  TaskAPI.gettestlist({ Suite_name: Suite_name }).then((data: { data: { Test_list: string|any[]; }; }) => {
    Test_list.value = data.data.Test_list;
    Test_list_length.value = data.data.Test_list.length;
  });
  TaskAPI.gettasklist({ Suite_name: Suite_name })
    .then((data: { data: { Task_list: Tasklist[]; }; }) => {
      loading.value = true;
      TaskListData.value = data.data.Task_list;
      console.info("gettasklist: ", data);
    })
    .catch((err: any) => {
      console.info("gettasklist error", err);
      ElMessage.error("系统错误！");
      loading.value = false;
    })
    .finally(() => {
      loading.value = false;
    });
}
const queryFormRef = ref(ElForm);

const TaskDeleDialog = reactive({
  title: "任务删除",
  visible: false,
});
const TaskCreateDialog = reactive({
  title: "任务创建",
  visible: false,
});
// 打开任务删除弹窗
function handleTaskDelete() {
  try {
    TaskDeleDialog.visible = true;
  } catch (err) {
    console.info("error:", err);
  }
}
// 关闭任务删除弹窗
function CloseTaskDeleDialog() {
  TaskDeleDialog.visible = false;
}
// 打开任务创建弹窗
function handleTaskCreate() {
  TaskCreateDialog.visible = true;
}
// 关闭任务创建弹窗
function CloseTaskCreateDialog() {
  TaskCreateDialog.visible = false;
  TaskFormRef.value.resetFields();
  TaskFormRef.value.clearValidate();
  formData.taskname = "";
  formData.testname = "";
}
// 查询参数
const queryParams = reactive<MenuQuery>({});
// 菜单表格数据
const menuTableData = ref<MenuVO[]>([]);
// 顶级菜单下拉选项
const menuOptions = ref<OptionType[]>([]);

// 初始菜单表单数据
const initialMenuFormData = ref<MenuForm>({
  id: undefined,
  parentId: 0,
  visible: 1,
  sort: 1,
  type: MenuTypeEnum.MENU, // 默认菜单
  alwaysShow: 0,
  keepAlive: 1,
  params: [],
});

// 查询
function handleQuery() {
  loading.value = true;
  MenuAPI.getList(queryParams)
    .then((data: any[]) => {
      menuTableData.value = data;
    })
    .finally(() => {
      loading.value = false;
    });
}

onMounted(() => {
  fetchData();
});
</script>

<style>
.el-table .el-table__row > td {
  border-bottom: none;
}
.basic-container {
  padding-left: 30px;
  padding-right: 15px;
  padding-top: 15px;
}
p {
  margin: 0;
  display: inline-block;
}
td {
  padding-top: 20px;
  padding-right: 10px;
  padding-bottom: 10px;
  max-width: 100%;
  word-wrap: break-word;
  word-break: break-all;
  max-height: 100%;
}
.el-dialog__title {
  font-size: 14px;
  color: grey;
}
.makesure {
  color: rgb(77, 76, 76);
  font-size: 16px;
  text-align: center;
}
.el-form-item {
  margin-right: 50px;
}
</style>
