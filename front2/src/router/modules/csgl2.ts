import { csgl2 } from "@/router/enums";


export default {
  path: "/aqcs/csgl2",
  name: "csgl2",
  component: () => import("@/views/aqcs/cs/jmcz2.vue"),
  meta: {
    title: "测试工具",
    rank: csgl2
  },
  children: [
    {
      path: "/aqcs/cs/jmcz2",
      name: "jmcz2",
      component: () => import("@/views/aqcs/cs/jmcz2.vue"),
      meta: {
        title: "界面操作"
      },
    },
    {
      path: "/aqcs/cs/jbyx2",
      name: "jbyx2",
      component: () => import("@/views/aqcs/cs/jbyx2.vue"),
      meta: {
        title: "脚本运行"
      }
    }
  ]
} satisfies RouteConfigsTable;
