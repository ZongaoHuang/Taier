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
  return http.request<SetResponse>("get", baseUrlApi("/api/SetShow1"), { params });
};

export const createSet = (data: SetData) => {
  return http.request<{ ret: number; msg?: string; id?: string }>("post", baseUrlApi("/api/SetCreate"), { data });
};

export const updateSet = (data: SetData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/SetUpdate"), { data });
};

export const deleteSet = (data: { id: string }) => {
  return http.request<{ ret: number; msg?: string }>("post", baseUrlApi("/api/SetDelete"), { data });
};

export const uploadSetFile = (data: FormData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/UploadSetFile"), { data });
};

export const uploadJsonFile = (formData: FormData) => {
  return http.request<SetResponse>("post", baseUrlApi("/api/upload-json"), {
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};
