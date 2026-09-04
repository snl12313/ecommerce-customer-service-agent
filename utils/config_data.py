import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def root_path(*relative: str) -> str:
    """生成项目根目录下的绝对路径"""
    return os.path.join(BASE_DIR, *relative)