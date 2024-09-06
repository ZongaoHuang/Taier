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

  export const getTestDetails = (testName: string) => {
    return http.request<TestResponse>("get", baseUrlApi("/api/TestDetails"), { params: { name: testName } });
  };

  export const executeTest = (testName: string) => {
    return http.request<TestResponse>("post", baseUrlApi("/api/TestExec"), { data: { Test_name: testName } });
  };

  export const deleteTest = (testName: string) => {
    return http.request<TestResponse>("post", baseUrlApi("/api/TestDele"), { data: { Test_name: testName } });
  };

  export const downloadTestResults = (testName: string) => {
    return http.request<Blob>("get", baseUrlApi("/api/DownloadTestResult"), {
      params: { Test_name: testName },
      responseType: 'blob'
    });
  };

  export interface TestStatusResponse {
    ret: number;
    state?: string;
    escape_rate?: string;
    msg?: string;
  }

  export const getTestStatus = (testName: string) => {
    return http.request<TestStatusResponse>("get", baseUrlApi("/api/TestStatus"), { params: { Test_name: testName } });
  };

  export const getRandomDataset = (testType: string) => {
    return http.request<{ ret: number; dataset: string; id: string }>("get", baseUrlApi("/api/RandomDataset"), { params: { type: testType } });
  };
