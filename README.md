# 电商智能客服 Agent

<div align="center">

🛒 基于 LangChain + LangGraph + RAG 的智能客服解决方案

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📖 项目简介

电商智能客服 Agent 是一个基于 **ReAct（Reasoning and Acting）框架** 的智能化客服系统，专为电商场景设计。该系统集成了 **RAG（检索增强生成）** 技术，能够自主理解用户意图、调用工具获取信息，并提供专业、准确的客服响应。

### ✨ 核心特性

- 🧠 **ReAct 推理引擎**：基于 LangGraph 的 Thought-Action-Observation 循环，实现自主决策
- 📚 **RAG 知识库**：支持 TXT/PDF 格式的商品目录、退换货政策、物流说明等专业知识库
- 🔧 **工具调用能力**：
  - `rag_summarize`：智能检索并总结知识库内容
  - `query_order`：订单状态查询（订单号、物流、金额等）
  - `submit_return`：退货申请提交（自动校验签收时间）
- 💬 **流式对话界面**：基于 Streamlit 的实时流式响应 UI
- 🔄 **上下文记忆**：支持多轮对话，保持会话上下文
- 📊 **日志监控**：完整的工具调用和模型交互日志
- 🎯 **中间件机制**：支持工具监控、模型日志等扩展功能

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI                        │
│                  (用户交互界面层)                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   ReactAgent (控制层)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ReAct Loop: 思考 → 行动 → 观察 → 再思考             │  │
│  │  - 意图识别                                         │  │
│  │  - 工具选择与参数生成                               │  │
│  │  - 结果评估与补充查询                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│            ┌──────────────┴──────────────┐                 │
│            ▼                             ▼                 │
│  ┌────────────────┐          ┌──────────────────┐         │
│  │ Middleware     │          │ Checkpointer     │         │
│  │ - monitor_tool │          │ - InMemorySaver  │         │
│  │ - log_before_  │          │ - 会话状态管理   │         │
│  │   model        │          └──────────────────┘         │
│  └────────────────┘                                         │
└──────────────┬─────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Tool Layer (工具层)                       │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────┐     │
│  │ rag_sum    │  │ query_     │  │ submit_          │     │
│  │ marize     │  │ order      │  │ return           │     │
│  └─────┬──────┘  └─────┬──────┘  └────────┬─────────┘     │
│        │               │                   │               │
└────────┼───────────────┼───────────────────┼───────────────┘
         │               │                   │
         ▼               ▼                   ▼
┌────────────────┐ ┌────────────┐   ┌──────────────────┐
│ Vector Store   │ │ orders.json│   │ 外部数据源       │
│ (Chroma)       │ │ 订单数据库 │   │                  │
│                │ └────────────┘   │                  │
│ - 知识库检索   │                  │                  │
│ - 语义匹配    │                  │                  │
│ - 文档分片    │                  │                  │
└────────────────┘                  └──────────────────┘
```

## 🛠️ 技术栈

### 核心框架
| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 主语言 |
| **LangChain** | 0.2+ | LLM 应用框架 |
| **LangGraph** | 0.1+ | ReAct 状态机引擎 |
| **Streamlit** | 1.30+ | Web UI 框架 |
| **Chroma** | 0.4+ | 向量数据库 |

### 模型服务
| 服务 | 提供商 | 型号 |
|------|--------|------|
| **聊天模型** | 阿里 DashScope | qwen3.7-flash |
| **Embedding** | 阿里 DashScope | qwen3.7-text-embedding |

### 数据处理
- **文档解析**：TXT、PDF 格式支持
- **文本分割**：RecursiveCharacterTextSplitter（chunk_size=1500, overlap=100）
- **去重机制**：MD5 哈希文件指纹

## 📦 安装部署

### 1. 环境要求

- Python 3.8+
- 阿里 DashScope API Key（用于模型和 Embedding 服务）

### 2. 克隆仓库

```bash
git clone <your-repo-url>
cd 电商智能客服Agent
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> 📝 **requirements.txt 示例**（请根据实际使用情况调整）：
> ```text
> langchain>=0.2.0
> langchain-openai>=0.1.0
> langgraph>=0.1.0
> langchain-chroma>=0.1.0
> langchain-text-splitters>=0.2.0
> streamlit>=1.30.0
> dashscope>=1.0.0
> chromadb>=0.4.0
> pypdf>=3.0.0
> ```

### 4. 配置环境变量

创建 `.env` 文件或修改 `config/rag.yml`：

```yaml
# config/rag.yml
chat_model_name: qwen3.7-flash
embedding_model_name: qwen3.7-text-embedding
```

> ⚠️ **注意**：确保已设置环境变量 `DASHSCOPE_API_KEY`

### 5. 准备知识库数据

将知识库文件放入 `data/` 目录，支持格式：
- `.txt` - 纯文本文件
- `.pdf` - PDF 文档

示例数据结构：
```
data/
├── 01_退换货政策.txt
├── 02_商品目录.txt
├── 03_物流配送.txt
├── 04_常见问题FAQ.txt
└── 05_商品尺码推荐指南.txt
```

### 6. 启动应用

```bash
streamlit run app.py
```

默认访问地址：`http://localhost:8501`

## 📚 使用指南

### 对话示例

**示例 1：咨询商品信息**
```
用户：你们有没有黑色的羽绒服？
Agent：🤔 [思考：需要检索商品目录]
       ✅ 已为您找到黑色羽绒服...
```

**示例 2：查询订单**
```
用户：我的订单 ORD20260825011 发货了吗？
Agent：🔍 [正在查询订单信息...]
       订单号：ORD20260825011
       状态：已签收
       物流：中通快递 ZT2026082500654
```

**示例 3：申请退货**
```
用户：我想退货，订单号 ORD20260825011
Agent：✅ 检测到订单已签收，且在 7 天退货期限内
       退货申请已提交！售后单号：RT20260904120001
```

### 工具调用流程

当用户提出问题时，Agent 会按照以下流程处理：

1. **意图分析**：判断是否需要调用工具
2. **工具选择**：选择合适的工具（rag_summarize / query_order / submit_return）
3. **参数生成**：提取关键参数（如订单号、检索词）
4. **执行工具**：调用对应工具获取结果
5. **结果评估**：判断信息是否充足
6. **生成回答**：整合信息，给出专业回复

最多允许 5 次工具调用循环，超时后将建议联系人工客服。

## 📁 项目结构

```
电商智能客服Agent/
├── agent/                      # Agent 核心逻辑
│   ├── react_agent.py          # ReAct Agent 实现
│   ├── tools/                  # 工具定义
│   │   ├── agent_tools.py      # 业务工具（RAG、订单查询等）
│   │   └── middleware.py       # 中间件（监控、日志）
├── config/                     # 配置文件
│   ├── chroma.yml              # 向量库配置
│   ├── rag.yml                 # 模型配置
│   └── prompts.yml             # Prompt 路径配置
├── data/                       # 数据目录
│   ├── external/json/          # JSON 数据（订单等）
│   └── *.txt                   # 知识库文档
├── model/                      # 模型工厂
│   └── factory.py              # 模型初始化
├── prompts/                    # Prompt 模板
│   ├── main_prompt.txt         # 主 Prompt
│   └── rag_summarize.txt       # RAG 汇总 Prompt
├── rag/                        # RAG 服务
│   ├── rag_service.py          # RAG 总结服务
│   └── vector_store.py         # 向量库服务
├── utils/                      # 工具函数
│   ├── config_data.py          # 路径配置
│   ├── config_handler.py       # 配置加载器
│   ├── file_handler.py         # 文件处理器
│   ├── logger_handler.py       # 日志处理器
│   └── prompt_loader.py        # Prompt 加载器
├── app.py                      # Streamlit 入口
└── requirements.txt            # 依赖列表
```

## ⚙️ 配置说明

### 向量库配置 (`config/chroma.yml`)

```yaml
collection_name: agent              # Chroma 集合名称
persist_directory: chroma_db        # 本地持久化路径
k: 10                               # 检索返回的文档数量
chunk_size: 1500                    # 文档分片大小
chunk_overlap: 100                  # 分片重叠
separators: ["\n\n","\n","。","！","？",...]  # 分隔符
```

### Prompt 配置

- **主 Prompt**：`prompts/main_prompt.txt` - Agent 系统指令
- **RAG Prompt**：`prompts/rag_summarize.txt` - 知识库总结模板

## 🧪 测试

可通过 Streamlit UI 进行功能测试：

1. **知识库问答**：输入商品、政策相关问题
2. **订单查询**：使用测试订单号查询
3. **退货申请**：模拟退货流程

查看 `log/` 目录获取详细运行日志。

## 📊 性能优化

- **MD5 去重**：避免重复加载相同知识库文件
- **文本清洗**：过滤特殊字符和空白字符
- **分片策略**：自适应分割符，保持语义完整性
- **最小长度过滤**：跳过小于 10 字符的分片

## 🔮 未来计划

- [ ] 集成更多数据源（数据库、API）
- [ ] 支持多语言客服
- [ ] 人工客服接管机制
- [ ] 对话情感分析
- [ ] 用户行为追踪与分析
- [ ] Docker 容器化部署
- [ ] RESTful API 接口

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目采用 MIT 协议开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://github.com/streamlit/streamlit)
- [Chroma](https://github.com/chroma-core/chroma)
- [阿里通义千问](https://tongyi.aliyun.com/)

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: snl12313@users.noreply.github.com
- 💬 Issues: [GitHub Issues](https://github.com/snl12313/ecommerce-customer-service-agent)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by Python + LangChain + RAG

</div>
