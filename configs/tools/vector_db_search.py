import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import Field, HttpUrl
from typing import List, Dict, Any, Optional
from nat.data_models.function import FunctionBaseConfig
from nat.cli.register_workflow import register_function  # 修正导入路径
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder

# 配置类（兼容仓库格式）
class VectorDBSearchConfig(FunctionBaseConfig, name="vector_db_search"):
    """向量数据库检索工具配置"""
    db_path: str = Field(default="./knowledge_base", description="向量数据库存储路径")
    model_name: str = Field(default="nvidia/nv-embedqa-e5-v5", description="嵌入模型名称")
    top_k: int = Field(default=3, description="返回的最相关结果数量")

@register_function(config_type=VectorDBSearchConfig)
async def vector_db_search(config: VectorDBSearchConfig, builder: Builder):
    """从向量数据库中检索与查询相关的文档"""
    
    class InputSchema(FunctionBaseConfig):
        query: str = Field(description="检索查询文本")
        filter: Optional[Dict[str, Any]] = Field(default=None, description="检索过滤条件")
    
    # 加载模型和数据库（确保与仓库中模型加载逻辑兼容）
    def _load_resources():
        # 加载嵌入模型（使用仓库推荐的NVIDIA嵌入模型）
        model = SentenceTransformer(config.model_name)
        # 加载FAISS索引
        index_path = os.path.join(config.db_path, "index.faiss")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"向量数据库不存在：{index_path}")
        index = faiss.read_index(index_path)
        # 加载文档元数据
        meta_path = os.path.join(config.db_path, "metadata.npy")
        metadata = np.load(meta_path, allow_pickle=True).tolist()
        return model, index, metadata
    
    # 检索逻辑
    async def search(query: str, filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        model, index, metadata = _load_resources()
        
        # 生成查询向量
        query_embedding = model.encode([query])
        # 检索相似向量
        distances, indices = index.search(query_embedding, config.top_k)
        
        # 整理结果
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0:
                continue  # 无效索引
            doc = metadata[idx]
            # 应用过滤条件（如果有）
            if filter and not all(doc.get(k) == v for k, v in filter.items()):
                continue
            results.append({
                "title": doc.get("title", "未知标题"),
                "content": doc.get("content", "")[:300] + "...",  # 截断内容
                "distance": float(distances[0][i]),  # 相似度（越小越相似）
                "source": doc.get("source", "unknown")
            })
        return results
    
    yield FunctionInfo.from_fn(
        fn=search,
        input_schema=InputSchema,
        description="从向量数据库中检索与查询相关的文档，支持过滤条件"
    )
    