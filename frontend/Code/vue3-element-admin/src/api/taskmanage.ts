//import request from "@/utils/request";
//import SERVER_URL from "@/App.vue";
import axios, { InternalAxiosRequestConfig, AxiosResponse } from "axios";
const USER_BASE_URL = "api";

const request = axios.create({
  baseURL: "http://127.0.0.1",
  timeout: 50000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
});
class TaskAPI {
  static gettasklist(query: object) {
    return request({
      //url: `${SERVER_URL}/user`,
      url: `${USER_BASE_URL}/TaskShow`,
      method: "get",
      params: query,
    });
  }
  static gettestlist(query: object) {
    return request({
      //url: `${SERVER_URL}/user`,
      url: `${USER_BASE_URL}/TestShow`,
      method: "get",
      params: query,
    });
  }
  static gettaskinfo(query: object) {
    return request({
      //url: `${SERVER_URL}/user`,
      url: `${USER_BASE_URL}/TaskInfo`,
      method: "get",
      params: query,
    });
  }
  static TaskResult(query: object) {
    return request({
      url: `${USER_BASE_URL}/TaskResult`,
      method: "get",
      params: query,
    });
  }
  static TaskExec(query: object) {
    return request({
      url: `${USER_BASE_URL}/TaskExec`,
      method: "post",
      data: query,
    });
  }
  static TaskDele(query: object) {
    return request<any, string>({
      url: `${USER_BASE_URL}/TaskDele`,
      method: "post",
      data: query,
    });
  }
  static TaskCreate(query: object) {
    return request<any, string>({
      url: `${USER_BASE_URL}/TaskCreate`,
      method: "post",
      data: query,
    });
  }
    //add
  static createTestSuite(query: object) {
    return request({
      url: `${USER_BASE_URL}/test_suit_create`,
      method: "post",
      data:query
    });
  }
  static showTestSuites() {
    return request({
      url: `${USER_BASE_URL}/test_suit_show`,
      method: "get",
    });
  }
  static createTest(data: object) {
    return request({
      url: `${USER_BASE_URL}/test_create`,
      method: "post",
      data,
    });
  }
  static deleteTestSuite(data: object) {
    return request({
      url: `${USER_BASE_URL}/test_suite_dele`,
      method: "post",
      data,
    });
  }
  static deleteTest(data: object) {
    return request({
      url: `${USER_BASE_URL}/test_dele`,
      method: "post",
      data,
    });
  }
  static listQuestions() {
    return request({
      url: `${USER_BASE_URL}/list_question`,
      method: "get",
    });
  }
  static addQuestion(data: object) {
    return request({
      url: `${USER_BASE_URL}/add_question`,
      method: "post",
      data,
    });
  }
  static modifyQuestion(data: object) {
    return request({
      url: `${USER_BASE_URL}/modify_question`,
      method: "post",
      data,
    });
  }
}
export default TaskAPI;
export interface Tasklist {
  // 任务名称
  name?: string;
  // 任务状态
  state?: string;
}
export interface TaskInfo {
  name?: string;
  collection?: string;
  model?: string;
  evaluator?: string;
  cate?: string;
  state?: string;
  escapeRate?: string;
}
export interface TestInfo {
  name?: string;
  collection?: string;
  model?: string;
  evaluator?: string;
  cate?: string;
  state?: string;
}
