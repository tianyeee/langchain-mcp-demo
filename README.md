# MCP (Model Context Protocol) 框架演示 - 使用 Qwen 模型

本项目包含 MCP 框架的演示代码，展示了如何使用 Qwen 模型通过 MCP 协议与各种工具进行交互。

## 文件结构

- `mcp_qwen_server.py` - MCP 服务器，提供心愿列表和当前时间工具
- `mcp_qwen_demo.py` - MCP 客户端 Python 脚本，演示如何调用服务器提供的工具
- `mcp_qwen_demo.ipynb` - MCP 客户端 Jupyter Notebook，与演示脚本功能相同，但提供交互式运行环境

## 功能说明

### 1. MCP 服务器 (`mcp_qwen_server.py`)

MCP 服务器提供以下工具：

- **get_current_time** - 获取当前时间，支持自定义时间格式
- **query_wish_list** - 查询心愿列表，支持关键词搜索

服务器会自动初始化心愿列表数据库，包含以下心愿项目：
- 天定山滑雪
- 南湖公园钓鱼
- 南溪湿地公园搭帐篷露营
- 伪满皇宫博物院参观
- 长春动植物园看雪饼猴
- 夜游新民大街
- 净月潭看蓝冰

### 2. MCP 客户端 (`mcp_qwen_demo.py` 和 `mcp_qwen_demo.ipynb`)

客户端演示了如何：
- 创建 MCP 客户端并连接到本地和远程 MCP 服务
- 获取可用工具列表
- 配置 Qwen 模型并创建代理
- 使用代理调用各种工具：
  - 计算器工具
  - 天气工具
  - 当前时间工具
  - 心愿列表查询工具
  - 综合旅游规划（结合天气和心愿列表）

## 安装依赖

```bash
uv pip install langchain-mcp-adapters langchain langchain-openai fastmcp
```

## 使用方法

### 1. 启动 MCP 服务器

```bash
cd d:\ProgramData\langchain-demo\newfolder2
python mcp_qwen_server.py
```

服务器将在 `http://localhost:8000/mcp` 上运行。

### 2. 运行 MCP 客户端

#### 使用 Python 脚本

```bash
cd d:\ProgramData\langchain-demo\newfolder2
python mcp_qwen_demo.py
```

#### 使用 Jupyter Notebook

```bash
cd d:\ProgramData\langchain-demo\newfolder2
jupyter notebook mcp_qwen_demo.ipynb
```

然后在浏览器中打开 Notebook 并运行所有单元格。

## 配置说明

### API 密钥配置

客户端需要配置以下 API 密钥：

1. **Qwen 模型 API 密钥**：用于调用 Qwen 模型
2. **天气工具 API 密钥**：用于查询天气信息

这些密钥在代码中已经预配置，但建议根据实际情况进行修改。

### 服务器配置

服务器默认配置：
- 传输协议：streamable-http
- 主机地址：0.0.0.0
- 端口：8000
- MCP 路径：/mcp

可以在 `mcp_qwen_server.py` 文件末尾修改服务器配置。

## 日志系统

所有文件都使用 Python 的 `logging` 模块进行日志记录，日志格式如下：

```
YYYY-MM-DD HH:MM:SS - LOG_LEVEL - MESSAGE
```

日志级别设置为 `INFO`，可以在代码中修改。

## 注意事项

1. 确保在运行客户端之前先启动服务器
2. 确保网络连接正常，以便调用远程 MCP 服务
3. 如果端口 8000 已被占用，可以修改服务器的端口配置
4. API 密钥可能会过期，请及时更新

## 扩展建议

1. 添加更多自定义工具到 MCP 服务器
2. 集成更多 AI 模型到客户端
3. 实现更复杂的工具调用逻辑
4. 添加用户认证和权限管理

## 许可证

本项目采用 MIT 许可证。
