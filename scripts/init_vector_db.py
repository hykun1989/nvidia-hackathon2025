import os
import faiss
import numpy as np
from typing import list, dict, Any, tuple
from sentence_transformers import SentenceTransformer
from nat.utils.logging import setup_logging  # 使用仓库中的日志工具

# 初始化日志（遵循仓库日志配置）
logger = setup_logging(__name__)

def load_documents(doc_dir: str) -> list[dict[str, Any]]:
    """加载知识库文档（示例数据，实际可扩展为读取PDF/Markdown）"""
    # 模拟AI-Q支持相关的FAQ文档
    sample_docs = [
        {
            "title": "NIM服务认证失败解决方案",
            "content": "当AI-Q调用NIM服务出现认证失败时，需检查：1. NVIDIA_API_KEY是否正确；2. 密钥是否有NIM服务权限；3. 网络是否能访问NIM端点（https://api.nvidia.com）。",
            "source": "internal_faq.md",
            "category": "technical"
        },
        {
            "title": "AI-Q工作流配置指南",
            "content": "自定义工作流需在YAML中定义steps，通过{{step_name.output}}传递参数。支持的_type包括react_agent和custom_workflow。",
            "source": "workflow_guide.md",
            "category": "configuration"
        },
        {
            "title": "多代理通信协议",
            "content": "AI-Q多代理通过ACP协议通信，需在general配置中设置event_bus: acp，并在handover_rules中定义代理交接条件。",
            "source": "multi_agent_guide.md",
            "category": "multi_agent"
        }
    ]
    return sample_docs

def init_vector_db(config: dict[str, str]):
    """初始化FAISS向量数据库（兼容仓库工具链）"""
    # 创建存储目录
    os.makedirs(config["db_path"], exist_ok=True)
    
    # 加载模型和文档
    logger.info(f"加载嵌入模型：{config['model_name']}")
    model = SentenceTransformer(config["model_name"])
    documents = load_documents(config["doc_dir"])
    logger.info(f"加载文档数量：{len(documents)}")
    
    # 生成向量
    embeddings = model.encode([doc["content"] for doc in documents])
    dimension = embeddings.shape[1]
    
    # 创建FAISS索引（使用扁平索引，适合中小规模数据）
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # 保存索引和元数据
    faiss.write_index(index, os.path.join(config["db_path"], "index.faiss"))
    np.save(
        os.path.join(config["db_path"], "metadata.npy"),
        np.array(documents, dtype=object)
    )
    logger.info(f"向量数据库初始化完成，存储路径：{config['db_path']}")

if __name__ == "__main__":
    # 配置参数（与工具配置保持一致）
    config = {
        "db_path": "./knowledge_base/aiq_support",
        "model_name": "nvidia/nv-embedqa-e5-v5",
        "doc_dir": "./docs"
    }
    init_vector_db(config)
    