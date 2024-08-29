// 最简代码，也就是这些字段必须有
import { aqcs } from "@/router/enums";

export default {
  path: "/aqcs",
  meta: {
    title: "安全测试工具",
    rank: aqcs
  },
  children: [
    {
      path: "/aqcs/csgl2",
      name: "csgl2",
      component: () => import("@/views/aqcs/cs/jmcz2.vue"),
      meta: {
        title: "测试工具"
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
    },
    {
      path: "/aqcs/sjjgl2",
      name: "sjjgl2",
      component: () => import("@/views/aqcs/sjjgl2.vue"),
      meta: {
        title: "数据集管理"
      }
    },
  ]
} satisfies RouteConfigsTable;
