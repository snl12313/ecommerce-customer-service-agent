from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import rag_summarize, query_order,submit_return
from agent.tools.middleware import monitor_tool, log_before_model


class ReactAgent:
    def __init__(self):
        self.checkpointer = InMemorySaver()
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, query_order, submit_return],
            middleware=[monitor_tool, log_before_model],
            checkpointer=self.checkpointer
        )

    def execute_stream(self, query: str, thread_id: str = "default"):
        input_dict = {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        config = {"configurable": {"thread_id": thread_id}}
        for chunk in self.agent.stream(input_dict, stream_mode="values", config=config, context={"report": False}):
            latest_message = chunk['messages'][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"
