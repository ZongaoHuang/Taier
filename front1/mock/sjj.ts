import { defineFakeRoute } from "vite-plugin-fake-server/client";

export default defineFakeRoute([
  // 数据集列表
  {
    url: "/sjj",
    method: "post",
    response: ({ body }) => {
      let list = [
        {
          date: "2016-05-07",
          name: "Tom",
          id: "1",
          scale: "1000"
        },
        {
          date: "2016-05-07",
          name: "Jerry",
          id: "2",
          scale: "2000"
        },
        {
          date: "2016-05-07",
          name: "Spike",
          id: "3",
          scale: "3000"
        },
        {
          date: "2016-05-07",
          name: "Tyke",
          id: "4",
          scale: "4000"
        }
      ]; // 生成数据
      list = list.filter(item => item.name.includes(body?.name));
      if(body.scale) list = list.filter(item => item.scale === body.scale);
      return {
        success: true,
        data: {
          list,
          total: list.length,
          pageSize: 10,
          currentPage: 1
        }
      };
    }
  },
]);

