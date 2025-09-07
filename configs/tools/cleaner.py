from typing import List, Dict, Any
import re
from datetime import datetime
from pydantic import Field
from nat.data_models.function import FunctionBaseConfig
from nat.cli.register_workflow import register_function  # 修正导入路径
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder

# 配置类（需继承仓库中的FunctionBaseConfig）
class DataCleanerConfig(FunctionBaseConfig, name="data_cleaner"):
    """数据清洗工具配置"""
    date_pattern: str = Field(default=r"\b202\d-[01]\d-[0-3]\d\b", 
                             description="日期提取正则表达式")
    company_pattern: str = Field(default=r"\b[A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*\b", 
                                description="公司名称提取正则表达式")

@register_function(config_type=DataCleanerConfig)
async def extract_structured_data(config: DataCleanerConfig, builder: Builder):
    """从原始新闻文本中提取结构化数据（公司、日期、事件类型）"""
    
    # 输入数据模型（符合仓库中Pydantic规范）
    class InputSchema(FunctionBaseConfig):
        raw_news: List[str] = Field(description="原始新闻文本列表")
    
    # 清洗逻辑实现
    def _clean_single_news(text: str) -> Dict[str, Any]:
        # 提取日期
        dates = re.findall(config.date_pattern, text)
        # 提取公司名称
        companies = re.findall(config.company_pattern, text)
        # 简单分类事件类型
        event_type = "product_launch" if "发布" in text or "推出" in text else \
                     "funding" if "融资" in text or "投资" in text else \
                     "partnership" if "合作" in text or "联盟" in text else "other"
        
        return {
            "text": text[:200] + "...",  # 截断长文本
            "dates": list(set(dates)),
            "companies": list(set(companies)),
            "event_type": event_type
        }
    
    # 工具执行函数
    async def clean_data(raw_news: List[str]) -> List[Dict[str, Any]]:
        return [_clean_single_news(text) for text in raw_news]
    
    # 返回工具元信息（符合仓库中FunctionInfo格式）
    yield FunctionInfo.from_fn(
        fn=clean_data,
        input_schema=InputSchema,
        description="清洗原始新闻数据，提取结构化信息（日期、公司、事件类型）"
    )
    