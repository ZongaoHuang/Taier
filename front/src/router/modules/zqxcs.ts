// 最简代码，也就是这些字段必须有
import { zqxcs } from "@/router/enums";

export default {
  path: "/zqxcs",
  redirect: "/zqxcs/index",
  meta: {
    title: "准确性测试工具",
    rank: zqxcs
  },
  children: [
    {
      path: "/zqxcs/csgl1",
      name: "csgl1",
      component: () => import("@/views/zqxcs/test1.vue"),
      meta: {
        title: "测试工具"
      },
      children: [
        {
          path: "/zqxcs/cs/jmcz",
          name: "jmcz",
          component: () => import("@/views/zqxcs/cs/jmcz.vue"),
          meta: {
            title: "界面操作"
          },
        },
        {
          path: "/zqxcs/cs/jbyx",
          name: "jbyx",
          component: () => import("@/views/zqxcs/cs/jbyx.vue"),
          meta: {
            title: "脚本运行"
          }
        }
      ]
    },
    {
      path: "/zqxcs/sjjgl1",
      name: "sjjgl1",
      component: () => import("@/views/zqxcs/sjjgl1.vue"),
      meta: {
        title: "数据集管理"
      }
    },
    {
      path: "/zqxcs/test1",
      name: "test1",
      component: () => import("@/views/zqxcs/test1.vue"),
      meta: {
        title: "测试"
      }
    }
  ]
} satisfies RouteConfigsTable;
