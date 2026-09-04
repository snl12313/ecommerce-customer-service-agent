import os
import hashlib
from langchain_core.documents import Document
from utils.logger_handler import logger


def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是一个文件")
        return None
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files = []
    if not os.path.exists(path):
        logger.error(f"[文件列表获取]路径{path}不存在")
        return files
    if not os.path.isdir(path):
        logger.error(f"[文件列表获取]路径{path}不是一个目录")
        return files
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.split('.')[-1] in allowed_types]



def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    from pypdf import PdfReader
    docs = []
    reader = PdfReader(filepath, password=passwd)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text or not text.strip():
            continue
        text = ''.join(ch for ch in text if ch == '\n' or (ord(ch) >= 32))
        docs.append(Document(page_content=text, metadata={"source": filepath, "page": i}))
    return docs


def txt_loader(filepath: str) -> list[Document]:
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": filepath})]
