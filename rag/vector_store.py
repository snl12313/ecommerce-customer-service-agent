import os.path
import re
from utils.logger_handler import logger
from langchain_core.documents import Document
from utils.config_data import root_path
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex


class VectorStoreServices:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=root_path(chroma_conf["persist_directory"])
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_keyword={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的md5做去重
        :return: None
        """

        def check_md5_hex(md5_for_chack: str):
            if not os.path.exists(root_path(chroma_conf["md5_hex_store"])):
                open(root_path(chroma_conf["md5_hex_store"]), 'w', encoding="utf-8").close()
                return False
            with open(root_path(chroma_conf["md5_hex_store"]), 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_chack:
                        return True
                return False

        def save_md5_hex(md5_for_save: str):
            with open(root_path(chroma_conf["md5_hex_store"]), 'a', encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            elif read_path.endswith("pdf"):
                return pdf_loader(read_path)
            return []

        def clean_text(text: str) -> str:
            text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
            text = re.sub(r'[\ufffe\uffff]', '', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

        allowed_files_path = listdir_with_allowed_type(root_path(chroma_conf["data_path"]),
                                                       tuple(chroma_conf["allow_knowledge_file_type"]))
        logger.info(
            f"[加载知识库]数据目录: {root_path(chroma_conf['data_path'])}, 扫描到文件数: {len(allowed_files_path)}, 文件列表: {allowed_files_path}")

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.splitter.split_documents(documents)
                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                for doc in split_document:
                    doc.page_content = clean_text(doc.page_content)

                split_document = [doc for doc in split_document
                                  if isinstance(doc.page_content, str)
                                  and len(doc.page_content) >= 10]
                if not split_document:
                    logger.warning(f"[加载知识库]{path}过滤后没有有效文本内容，跳过")
                    continue

                for doc in split_document:
                    try:
                        self.vector_store.add_documents([doc])
                    except Exception as e:
                        logger.error(f"[加载知识库]分片嵌入失败: {e}, 内容前50字: {repr(doc.page_content[:50])}")
                        continue

                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path} 内容加载失败:{str(e)}", exc_info=True)
                continue
