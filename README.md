# LLM + MCP + RAG 项目

这是一个结合了大型语言模型（LLM）、模型上下文协议（MCP）和检索增强生成（RAG）技术的智能代理系统。该项目展示了如何构建一个能够使用工具、访问外部数据并生成智能响应的AI系统。

## 🌟 项目特性

- **🤖 智能代理系统**：基于LLM的自主代理，能够理解用户意图并执行复杂任务
- **🔧 MCP工具集成**：支持多种MCP工具，包括文件系统操作和网络数据获取
- **📚 RAG检索增强**：通过向量存储和相似度搜索提供上下文增强的响应
- **🌐 多模型支持**：支持通义千问等主流LLM模型
- **🔄 异步架构**：完全基于异步编程，提供高性能的并发处理能力

## 🏗️ 系统架构

项目采用模块化设计，主要组件包括：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LLM Agent     │────│   MCP Tools     │────│  Vector Store   │
│                 │    │                 │    │                 │
│ • 通义千问模型   │    │ • 文件系统工具  │    │ • 文档嵌入      │
│ • 工具调用      │    │ • 网络获取工具  │    │ • 相似度搜索    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Knowledge Base │
                     │                 │
                     │ • 用户数据      │
                     │ • 文档存储      │
                     └─────────────────┘
```

## 📁 项目结构

```
├── src/
│   ├── agent.py              # 核心代理类
│   ├── chat_openai.py        # LLM聊天接口
│   ├── mcp_client.py         # MCP客户端实现
│   ├── mcp_tools.py          # MCP工具配置
│   ├── embedding_retriever.py # 文档嵌入和检索
│   ├── vector_store.py       # 向量存储实现
│   ├── index.py              # 主程序入口
│   └── utils/                # 工具函数
├── knowledge/                # 知识库数据
├── output/                   # 输出目录
├── .env                      # 环境变量配置
└── README.md                 # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- 通义千问API密钥
- Node.js和npm（用于MCP工具）
- uv（Python包管理器）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd llm+mcp+rag
   ```

2. **配置环境变量**
   复制 `.env` 文件并根据需要修改配置：
   ```bash
   DASHSCOPE_API_KEY="你的API密钥"
   DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
   MODEL_NAME="qwen-plus"
   EMBEDDING_MODEL="text-embedding-v4"
   PROXY_URL="http://127.0.0.1:7890"  # 可选，用于网络代理
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行项目**
   ```bash
   python src/index.py
   ```

## 🔧 核心组件详解

### Agent（智能代理）

`Agent` 类是系统的核心，负责：
- 协调LLM和MCP工具
- 管理对话历史
- 处理工具调用循环
- 整合RAG上下文

```python
agent = Agent(
    model="qwen-plus",
    mcp_clients=[filesystem_client, fetch_client],
    context="检索到的相关文档"
)
```

### MCP客户端

支持多种MCP工具：
- **文件系统工具**：读取、写入、列出文件
- **网络获取工具**：爬取网页内容

```python
# 文件系统工具
filesystem_tool = PresetMcpTools.filesystem.append_mcp_params("/path/to/directory")

# 网络获取工具  
fetch_tool = PresetMcpTools.fetch
```

### RAG检索系统

`EembeddingRetriever` 负责：
- 文档嵌入向量化
- 相似度搜索
- 上下文检索

```python
retriever = EembeddingRetriever("text-embedding-v4")
context = await retriever.retrieve("查询问题")
```

## 📖 使用示例

### 基本使用

```python
from src.agent import Agent
from src.mcp_client import MCPClient

# 创建代理
agent = Agent(model="qwen-plus", mcp_clients=[])
await agent.init()

# 执行任务
response = await agent.invoke("帮我总结今天的新闻")
print(response)

# 清理资源
await agent.cleanup()
```

### RAG增强查询

```python
# 准备知识库
await prepare_knowledge_data()

# 检索相关文档
context = await retrieve_context("关于Bret的信息")

# 使用RAG进行问答
agent = Agent(model="qwen-plus", context=context)
response = await agent.invoke("根据Bret的信息创作一个故事")
```

## 🛠️ 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `DASHSCOPE_API_KEY` | 通义千问API密钥 | 必填 |
| `DASHSCOPE_BASE_URL` | API基础URL | 必填 |
| `MODEL_NAME` | LLM模型名称 | `qwen-plus` |
| `EMBEDDING_MODEL` | 嵌入模型名称 | `text-embedding-v4` |
| `PROXY_URL` | HTTP代理URL | 可选 |
| `USE_CN_MIRROR` | 使用国内镜像 | 可选 |

### MCP工具配置

项目支持通过环境变量配置MCP工具的行为：

- `USE_CN_MIRROR`: 启用国内镜像加速包下载
- `PROXY_URL`: 设置网络代理用于数据获取

## 📊 数据流

1. **知识库准备**：
   ```
   用户请求 → Agent → MCP Fetch工具 → 获取外部数据 → 保存到知识库
   ```

2. **RAG检索**：
   ```
   用户查询 → 文档嵌入 → 向量存储 → 相似度搜索 → 相关文档
   ```

3. **智能响应**：
   ```
   用户问题 + 检索文档 → Agent → LLM → 工具调用 → 最终响应
   ```

## 🧪 运行示例

项目包含多个示例脚本：

- `src/index.py`: 完整的RAG演示
- `src/agent.py`: Agent基础用法
- `src/mcp_client.py`: MCP客户端示例
- `src/chat_openai.py`: LLM聊天示例

运行主要示例：
```bash
python src/index.py
```

## 📈 性能优化

### 向量存储优化
- 使用余弦相似度进行快速检索
- 支持批量文档嵌入
- 内存中的向量索引

### 异步处理
- 所有I/O操作都是异步的
- 支持并发工具调用
- 流式响应输出

## 🔒 安全考虑

- API密钥通过环境变量管理
- 支持代理配置避免网络问题
- 错误处理和异常恢复机制
- 资源清理确保无内存泄漏

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [通义千问](https://tongyi.aliyun.com/)
- [OpenAI](https://openai.com/)
- 所有开源贡献者

## 📞 联系方式

如有问题或建议，请提交Issue或联系项目维护者。

---

**注意**: 本项目需要有效的通义千问API密钥才能正常运行。请确保在运行前正确配置环境变量。