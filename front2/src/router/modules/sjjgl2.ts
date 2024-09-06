import { sjjgl2 } from "@/router/enums";


export default {
  path: "/aqcs/sjjgl2",
  meta: {
    title: "数据集管理",
    rank: sjjgl2
  },
  children: [
    {
      path: "/aqcs/sjjgl2",
      name: "sjjgl2",
      component: () => import("@/views/aqcs/sjjgl2.vue"),
      meta: {
        title: "数据集管理"
      }
    }
  ]
} satisfies RouteConfigsTable;
