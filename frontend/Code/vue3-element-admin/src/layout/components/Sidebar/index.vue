<template>
  <div :class="{ 'has-logo': sidebarLogo }">
    <!-- layout mix-->
    <div class="flex w-full" v-if="layout == LayoutEnum.MIX">
      <!-- 宸︿笂瑙掑浘鏍� -->
      <SidebarLogo v-if="sidebarLogo" :collapse="!appStore.sidebar.opened" />
      <SidebarMixTopMenu class="flex-1" />
      <NavbarAction />
    </div>
    <!-- layout left || layout top -->
    <template v-else>
      <SidebarLogo v-if="sidebarLogo" :collapse="!appStore.sidebar.opened" />
      <el-scrollbar>
        <SidebarMenu :menu-list="data" base-path="" />
      </el-scrollbar>
      <NavbarAction v-if="layout === LayoutEnum.TOP" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore, usePermissionStore, useAppStore } from "@/store";
import { LayoutEnum } from "@/enums/LayoutEnum";

const appStore = useAppStore();
const settingsStore = useSettingsStore();
// const permissionStore = usePermissionStore();
const data = [
  {
    path: "/system",
    component: "Layout",
    redirect: "/system/user",
    name: "/system",
    meta: {
      title: "系统管理",
      icon: "system",
      hidden: false,
      alwaysShow: false,
      params: null,
    },
    children: [
      {
        path: "user",
        component: "system/user/index",
        name: "User",
        meta: {
          title: "用户管理",
          icon: "el-icon-User",
          hidden: false,
          keepAlive: true,
          alwaysShow: false,
          params: null,
        },
      },
      {
        path: "role",
        component: "system/role/index",
        name: "Role",
        meta: {
          title: "角色管理",
          icon: "role",
          hidden: false,
          keepAlive: true,
          alwaysShow: false,
          params: null,
        },
      },
    ],
  },
  {
    path: "/TestManage",
    component: "Layout",
    meta: {
      icon: "el-icon-ElementPlus",
      hidden: false,
      alwaysShow: false,
      params: null,
    },
    children: [
      {
        path: "testmanage",
        meta: {
          title: "测试管理",
          icon: "el-icon-ElementPlus",
          hidden: false,
          alwaysShow: false,
          params: null,
        },
      },
    ],
  },
  {
    path: "/ResultDisplay",
    component: "Layout",
    meta: {
      icon: "el-icon-ElementPlus",
      hidden: false,
      alwaysShow: false,
      params: null,
    },
    children: [
      {
        path: "resultdisplay",
        meta: {
          title: "任务管理",
          icon: "el-icon-ElementPlus",
          hidden: false,
          alwaysShow: false,
          params: null,
        },
      },
    ],
  },
  {
    path: "/DatasetManage",
    component: "Layout",
    meta: {
      icon: "el-icon-ElementPlus",
      hidden: false,
      alwaysShow: false,
      params: null,
    },
    children: [
      {
        path: "datasetmanage",
        meta: {
          title: "数据管理",
          icon: "el-icon-ElementPlus",
          hidden: false,
          alwaysShow: false,
          params: null,
        },
      },
    ],
  },
];
const sidebarLogo = computed(() => settingsStore.sidebarLogo);
const layout = computed(() => settingsStore.layout);
</script>

<style lang="scss" scoped>
.has-logo {
  .el-scrollbar {
    height: calc(100vh - $navbar-height);
  }
}
</style>
