import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import axios from "axios";

/** 测试 */


export const test11 = (data?: object) => {
  return http.request<any>("post", baseUrlApi("/api/test"), { data })
    .then(response => {
      console.log('Response:', response.data);
    })
    .catch(error => {
      console.error('Request failed:', error.message);
    });
};
