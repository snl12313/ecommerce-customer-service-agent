from langchain_openai import ChatOpenAI
from utils.config_handler import rag_conf


def create_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=rag_conf["chat_model_name"],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


class DashScopeEmbeddings:
    """使用DashScope原生SDK的嵌入模型，兼容Chroma的embedding_function接口"""

    def __init__(self, model: str):
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        import dashscope
        resp = dashscope.TextEmbedding.call(
            model=self.model,
            input=[str(t) for t in texts]
        )
        if resp.status_code != 200:
            raise RuntimeError(f"DashScope嵌入调用失败: {resp.code} - {resp.message}")
        return [item["embedding"] for item in resp.output["embeddings"]]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.embed_documents(input)


chat_model = create_chat_model()
embed_model = DashScopeEmbeddings(model=rag_conf["embedding_model_name"])