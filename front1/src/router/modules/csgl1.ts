import { csgl1 } from "@/router/enums";


export default {
  path: "/zqxcs/csgl1",
  name: "csgl1",
  component: () => import("@/views/zqxcs/cs/jmcz1.vue"),
  meta: {
    title: "测试工具",
    rank: csgl1
  },
  children: [
    {
      path: "/zqxcs/cs/jmcz1",
      name: "jmcz1",
      component: () => import("@/views/zqxcs/cs/jmcz1.vue"),
      meta: {
        title: "界面操作"
      },
    },
    {
      path: "/zqxcs/cs/jbyx1",
      name: "jbyx1",
      component: () => import("@/views/zqxcs/cs/jbyx1.vue"),
      meta: {
        title: "脚本运行"
      }
    }
  ]
} satisfies RouteConfigsTable;
