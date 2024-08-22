import { http } from "@/utils/http";

export type Sjj = {
  /** 日期 */
  date: string;
  /** 名称 */
  name: string;
  /** ID */
  id: string;
  /** 规模 */
  scale: string;
};

export type SjjTable = {
  success: boolean;
  data?: {
    /** 列表数据 */
    list: Array<any>;
    /** 总条目数 */
    total?: number;
    /** 每页显示条目个数 */
    pageSize?: number;
    /** 当前页数 */
    currentPage?: number;
  };
};

export const getSjj = (data?: object) => {
  return http.request<SjjTable>("post", "/sjj", { data });
};
