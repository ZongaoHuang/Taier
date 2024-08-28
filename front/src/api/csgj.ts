import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export interface TestData {
    name: string;
    model: string;
    dataset: string;
    type: string;
    state: string;
    escape_rate: string;
    created_at: string;
  }
  
  export interface TestResponse {
    ret: number;
    tests?: TestData[];
    msg?: string;
  }
  
  export const getTestList = () => {
    return http.request<TestResponse>("get", baseUrlApi("/api/TestShow"));
  };

  export const getRecentTests = () => {
    return http.request<TestResponse>("get", baseUrlApi("/api/RecentTests"));
  };

export const createTest = (data: {
  name: string;
  suite: string;
  dataset: string;
  model: string;
  evaluator: string;
}) => {
  return http.request<TestResponse>("post", baseUrlApi("/api/TestCreate"), { data });
};
  
  export const getDatasets = () => {
    return http.request<{ ret: number; datasets: string[] }>("get", baseUrlApi("/api/DatasetList"));
  };
  
  export const getSuites = () => {
    return http.request<{ ret: number; suites: string[] }>("get", baseUrlApi("/api/SuiteList"));
  };