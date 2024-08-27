# 文件目录

- backend：后端代码
- front：前端代码
- frontend：本科生写的前端，可参考

## 后端启动方法

后端采用Django框架, 进入backend目录后, 使用conda或者env创建**python 3.10**环境，然后运行

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

安装好依赖后，运行如下指令启动后端服务

```bash
# 进入jailbreak目录
cd jailbreak
# 运行Django服务
python manage.py runserver 0.0.0.0:80
```

注意，如果改变启动的端口，要在前端请求的位置改变相应的端口，具体步骤：
在front文件夹下的*vite.config.ts*中，把 *http://127.0.0.1:8888* 的端口修改为后端启动的端口

```bash
// 服务端渲染
    server: {
      // 端口号
      port: VITE_PORT,
      host: "0.0.0.0",
      // 本地跨域代理 https://cn.vitejs.dev/config/server-options.html#server-proxy
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8888",
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, "")
        }
      },
      // 预热文件以提前转换和缓存结果，降低启动期间的初始页面加载时长并防止转换瀑布
      warmup: {
        clientFiles: ["./index.html", "./src/{views,components}/*"]
      }
    },
```

## front前端启动方法

进入到front文件夹下
首先安装node
官网：<https://nodejs.org/en/download/package-manager>

```powershell
# installs fnm (Fast Node Manager)
winget install Schniz.fnm
# configure fnm environment
fnm env --use-on-cd | Out-String | Invoke-Expression
# download and install Node.js
fnm use --install-if-missing 18
# verifies the right Node.js version is in the environment
node -v # should print `v18.20.4`
# verifies the right npm version is in the environment
npm -v # should print `10.7.0`
```

安装 pnpm

```bash
npm install -g pnpm
```

安装@pureadmin/cli 脚手架

```bash
npm install -g @pureadmin/cli
```

安装依赖

```bash
pnpm install
```

启动平台

```bash
pnpm dev
```

项目打包

```bash
pnpm build
```

## frontend启动方法

安装完node后，

```bash
# 切换到项目目录
cd vue3-element-admin

# 安装 pnpm
npm install pnpm -g

# 安装依赖
pnpm install

# 启动运行
pnpm run dev

```
