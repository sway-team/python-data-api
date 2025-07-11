# DataApi 管理系统

一个可以快速配置数据和进行页面APP开发的数据配置系统，您也可以认为它是一个自用轻量级的低代码平台，在AI时代的表现会更加出彩。以下是AI自行整理的说明。欢迎大家试用。

一个基于 Flask + Vite + Tailwind CSS 的现代化数据管理系统，提供用户认证、数据管理、API 服务等功能。

## 🚀 项目特性

### 后端功能 (Flask)
- **用户管理**: 用户注册、登录、认证
- **数据集管理**: 数据的增删改查、过滤、组合查询
- **API 服务**: 提供简单易用的 API 接口，支持复杂数据查询
- **数据库操作**: 基于 SQLAlchemy 的 ORM 操作
- **日志记录**: 完整的操作日志记录
- **CORS 支持**: 跨域请求支持

### 前端功能 (Vite + Tailwind CSS)
- **现代化 UI**: 基于 Tailwind CSS 的响应式设计
- **用户界面**: 登录、注册、用户中心、数据管理页面
- **组件化**: 模块化的前端组件系统
- **热更新**: Vite 开发服务器支持实时热更新
- **动画效果**: 使用 Animate.css 的流畅动画

## 📁 项目结构

```
python-data-api-open/
├── api/                    # API 路由模块
│   ├── dataset.py         # 数据集管理 API
│   ├── frame.py           # 框架相关 API
│   ├── service.py         # 服务 API
│   └── user.py            # 用户管理 API
├── comp/                   # 核心组件
│   ├── base.py            # 基础类
│   ├── cache.py           # 缓存组件
│   ├── datalogic.py       # 数据逻辑
│   ├── db.py              # 数据库操作
│   ├── emaillogic.py      # 邮件逻辑
│   ├── smsJDlogic.py      # 短信逻辑
│   └── tool.py            # 工具函数
├── conf/                   # 配置文件
│   └── workflow.py        # 工作流配置
├── static/                 # 前端静态资源
│   ├── app/               # 应用页面
│   │   ├── login.html     # 登录页面
│   │   ├── datamanage.html # 数据管理页面
│   │   └── usercenter.html # 用户中心页面
│   ├── assets/            # 静态资源
│   │   ├── css/           # 样式文件
│   │   ├── js/            # JavaScript 文件
│   │   ├── images/        # 图片资源
│   │   └── template/      # 模板文件
│   ├── package.json       # 前端依赖配置
│   ├── vite.config.js     # Vite 配置
│   └── tailwind.config.js # Tailwind CSS 配置
├── app.py                  # Flask 应用入口
├── env.py                  # 环境配置
├── requirements.txt        # Python 依赖
├── init.py             # 数据库初始化脚本
├── start.sh               # 启动脚本
├── stop.sh                # 停止脚本
└── README.md              # 项目说明
```

## 🛠️ 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd python-data-api-open
```

### 2. 配置环境
编辑 `env.py` 文件，配置数据库连接信息：
```python
# 数据库配置
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "your_username"
DB_PWD = "your_password"
DB_NAME = "your_database"

# Flask 配置
FLASK_RUN_PORT = 5070
SECRET_KEY = "your_secret_key"

# 页面配置
PAGE_HOST = "http://localhost:5173"
```

### 3. 运行初始化脚本
```bash
python init.py
```
此脚本会自动：
- 安装 Python 依赖 (`pip install -r requirements.txt`)
- 安装前端依赖 (`cd static && npm install`)
- 初始化数据库表结构
- 导入初始数据

### 4. 启动服务

#### 方式一：使用脚本启动（推荐）
```bash
# 启动服务（前后端同时启动）
./start.sh

# 停止服务
./stop.sh

# 新开终端，启动前端服务
cd static
npm run dev
```

#### 方式二：手动启动
```bash
# 启动后端服务
python app.py

# 新开终端，启动前端服务
cd static
npm run dev
```

## 🎯 使用指南

### 访问应用
- **前端地址**: http://localhost:5173
- **后端 API**: http://localhost:5070

### 主要功能

#### 1. 用户管理
- 访问 `/app/login` 进行用户登录/注册
- 支持手机号验证码注册
- 用户认证和会话管理

#### 2. 数据管理
- 访问 `/app/datamanage` 进行数据管理
- 支持数据的增删改查操作
- 提供高级过滤和搜索功能
- 支持数据组合查询

#### 3. API 接口
- `/dataset/*` - 数据集管理接口（外部系统访问使用）
- `/user/*` - 用户管理接口（本系统认证使用）
- `/frame/*` - 配置框架相关接口
- `/service/*` - 服务接口（本系统访问使用）

### 开发模式

#### 前端开发
```bash
cd static
npm run dev          # 启动 Vite 开发服务器
```

#### 后端开发
```bash
python app.py        # 启动 Flask 开发服务器
```

## 🔧 技术栈

### 后端
- **Flask**: Web 框架
- **SQLAlchemy**: ORM 数据库操作
- **PyMySQL**: MySQL 数据库驱动
- **Flask-CORS**: 跨域支持
- **Gunicorn**: WSGI 服务器

### 前端
- **Vite**: 现代化构建工具
- **Tailwind CSS**: 实用优先的 CSS 框架
- **jQuery**: JavaScript 库
- **Animate.css**: CSS 动画库
- **Font Awesome**: 图标库
- **jQuery AppManager**: 自研页面程序管理器

## 📝 配置说明

### 数据库配置
在 `env.py` 中配置数据库连接参数：
```python
DB_HOST = "localhost"      # 数据库主机
DB_PORT = 3306            # 数据库端口
DB_USER = "root"          # 数据库用户名
DB_PWD = "password"       # 数据库密码
DB_NAME = "datain"        # 数据库名称
```

### 前端配置
在 `static/vite.config.js` 中配置 Vite：
```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
```

## 🚨 注意事项

1. **端口配置**: 确保 5070 和 5173 端口未被占用
2. **数据库**: 确保 MySQL 服务已启动且配置正确
3. **Node.js**: 确保已安装 Node.js (建议 v16+)
4. **Python**: 建议使用 Python 3.8+

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   lsof -i :5070
   lsof -i :5173
   ```

2. **数据库连接失败**
   - 检查 `env.py` 中的数据库配置
   - 确保 MySQL 服务正在运行

3. **前端依赖安装失败**
   ```bash
   cd static
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Python 依赖安装失败**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 后续计划

1、完善模版配置和页面配置功能。
2、增加模版市场，供用户选择页面配置套件。
3、增加MCP能力，可以AI交互。

---

**开发团队**: Sway Team  
**版本**: 1.0.0  
**最后更新**: 2025年
