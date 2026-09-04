from utils.config_handler import prompts_conf
from utils.config_data import root_path
from utils.logger_handler import logger


# 加载系统提示词
def load_system_prompts():
    try:
        system_prompt_path = root_path(prompts_conf["main_prompt_path"])
        with open(system_prompt_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词出错,{str(e)}")
        return ""


# 加载RAG提示词
def load_rag_prompts():
    try:
        rag_prompt_path = root_path(prompts_conf["rag_summarize_prompt_path"])
        with open(rag_prompt_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG提示词出错,{str(e)}")
        return ""
