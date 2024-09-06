import { sjjgl1 } from "@/router/enums";


export default {
  path: "/zqxcs/sjjgl1",
  meta: {
    title: "数据集管理",
    rank: sjjgl1
  },
  children: [
    {
      path: "/zqxcs/sjjgl1",
      name: "sjjgl1",
      component: () => import("@/views/zqxcs/sjjgl1.vue"),
      meta: {
        title: "数据集管理"
      }
    }
  ]
} satisfies RouteConfigsTable;
