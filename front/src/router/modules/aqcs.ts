// 最简代码，也就是这些字段必须有
import { aqcs } from "@/router/enums";

export default {
  path: "/aqcs",
  redirect: "/aqcs/index",
  meta: {
    title: "安全测试工具",
    rank: aqcs
  },
  children: [
    {
      path: "/aqcs/csgl",
      name: "csgl",
      component: () => import("@/views/aqcs/csgl.vue"),
      meta: {
        title: "测试管理"
      }
    },
    {
      path: "/aqcs/test",
      name: "test",
      component: () => import("@/views/aqcs/test.vue"),
      meta: {
        title: "测试"
      }
    }
  ]
} satisfies RouteConfigsTable;
