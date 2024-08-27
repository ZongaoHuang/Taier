import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export interface SetData {
  id?: string;
  name: string;
  suite_name: string;
  created_at?: string;
  question_count?: number;
  cate?: string;
}

export type SetResponse = {
  ret: number;
  msg?: string;
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

// export const getSjj = (data?: object) => {
//   return http.request<SjjTable>("post", baseUrlApi("Sjj"), { data });
// };

export const getSetList = (params?: object) => {
  return http.request<SetResponse>("get", baseUrlApi("/api/SetShow"), { params });
};

export const createSet = (data: SetData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/SetCreate"), { data });
};

export const updateSet = (data: SetData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/SetUpdate"), { data });
};

export const deleteSet = (data: { id: string }) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/SetDelete"), { data });
};

export const uploadJson = (data: FormData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/upload_json"), { data });
};
