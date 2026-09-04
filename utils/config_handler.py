import yaml
from utils.config_data import root_path


def _load_yaml(config_path: str, encoding: str = "utf-8") -> dict:
    with open(config_path, encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_rag_config(config_path: str = root_path("config/rag.yml"), encoding: str = "utf-8"):
    return _load_yaml(config_path, encoding)


def load_chroma_config(config_path: str = root_path("config/chroma.yml"), encoding: str = "utf-8"):
    return _load_yaml(config_path, encoding)


def load_prompts_config(config_path: str = root_path("config/prompts.yml"), encoding: str = "utf-8"):
    return _load_yaml(config_path, encoding)


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
