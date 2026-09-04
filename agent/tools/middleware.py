from langchain.agents import AgentState
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime
from typing import Callable
from langchain.agents.middleware import wrap_tool_call, before_model
from langchain.agents.middleware.types import ToolCallRequest
from utils.logger_handler import logger


@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 处理请求的函数
        handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具执行结果：{request.tool_call['name']}调用成功")

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败,原因：{str(e)}")
        raise e


@before_model
def log_before_model(
        # 整个Agent智能体中的状态记录
        state: AgentState,
        # 记录了整个执行过程中的上下文信息
        runtime: Runtime
):
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息")
    content = state['messages'][-1].content
    content_text = content.strip() if isinstance(content, str) else str(content)
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__}{content_text}")
    return None
