// 最简代码，也就是这些字段必须有
import { adbcs } from "@/router/enums";

export default {
  path: "/adbcs/adbcs1",
  name: "adbcs1",
  component: () => import("@/views/adbcs/adbcs1.vue"),
  meta: {
    title: "手机测试工具",
    rank: adbcs
  }
} satisfies RouteConfigsTable;
