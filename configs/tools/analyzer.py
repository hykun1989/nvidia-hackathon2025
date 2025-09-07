from typing import List, Dict, Any, Tuple
import pandas as pd
from pydantic import Field
from nat.data_models.function import FunctionBaseConfig
from nat.cli.register_workflow import register_function  # 修正导入路径
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder

# 配置类（适配仓库基类）
class TrendAnalyzerConfig(FunctionBaseConfig, name="trend_analyzer"):
    """趋势分析工具配置"""
    top_n_trends: int = Field(default=3, description="提取的顶级趋势数量")
    event_type_weights: Dict[str, float] = Field(
        default={"product_launch": 1.5, "funding": 1.2, "partnership": 1.0, "other": 0.5},
        description="不同事件类型的权重"
    )

@register_function(config_type=TrendAnalyzerConfig)
async def generate_trend_insights(config: TrendAnalyzerConfig, builder: Builder):
    """基于结构化数据生成市场趋势洞察"""
    
    class InputSchema(FunctionBaseConfig):
        structured_data: List[Dict[str, Any]] = Field(description="清洗后的结构化数据列表")
    
    # 统计事件类型分布
    def _count_event_types(data: List[Dict[str, Any]]) -> Dict[str, int]:
        df = pd.DataFrame(data)
        return df["event_type"].value_counts().to_dict()
    
    # 识别热门公司（出现次数加权）
    def _identify_top_companies(data: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
        company_scores = {}
        for item in data:
            weight = config.event_type_weights.get(item["event_type"], 0.5)
            for company in item["companies"]:
                if company in company_scores:
                    company_scores[company] += weight
                else:
                    company_scores[company] = weight
        # 按分数排序
        return sorted(company_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # 生成趋势洞察
    async def analyze_trends(structured_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not structured_data:
            return {"error": "无结构化数据可分析"}
        
        event_counts = _count_event_types(structured_data)
        top_companies = _identify_top_companies(structured_data)
        
        # 生成趋势描述
        trends = []
        if event_counts.get("product_launch", 0) > event_counts.get("funding", 0):
            trends.append("市场以产品发布为主要动态，技术迭代活跃")
        else:
            trends.append("融资事件频发，资本对行业关注度高")
        
        return {
            "event_distribution": event_counts,
            "top_companies": top_companies,
            "key_trends": trends[:config.top_n_trends],
            "total_analyzed_items": len(structured_data)
        }
    
    yield FunctionInfo.from_fn(
        fn=analyze_trends,
        input_schema=InputSchema,
        description="基于结构化数据识别市场趋势、热门公司和事件分布"
    )
    