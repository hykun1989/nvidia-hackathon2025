#!/bin/bash  
  
echo "🚀 启动智能学习助手 - NVIDIA NeMo Agent Toolkit"  
echo "=============================================="  
  
# 设置环境变量
# Mem0 AI记忆平台API密钥 - 用于智能记忆管理和长期记忆存储功能  
export MEM0_API_KEY=you_api_key  
# NVIDIA API密钥 - 用于访问NVIDIA NIM服务、嵌入模型和RAG文档处理功能    
export NVIDIA_API_KEY=you_api_key  
# Tavily搜索API密钥 - 用于实时网络搜索和获取最新研究信息  
export TAVILY_API_KEY=you_api_key  
# Google Gemini API密钥 - 用于大语言模型推理和对话生成功能  
# export GOOGLE_API_KEY=AIzaSyD_KDqGcbBhiB3GCOmGzG7dMDFuSSNO6OQ
# 阿里百炼 API密钥 - 用于大语言模型推理和对话生成功能  
export ALIYUN_API_KEY=you_api_key

# 前端UI配置  
# 启用中间步骤显示功能 - 控制是否在UI中显示AI处理过程的中间步骤  
export NEXT_PUBLIC_ENABLE_INTERMEDIATE_STEPS=true    
# 默认展开中间步骤 - 控制中间步骤是否默认展开显示，而不是折叠状态  
export NEXT_PUBLIC_EXPAND_INTERMEDIATE_STEPS=true    
# 覆盖相同ID的中间步骤 - 当收到相同ID的步骤时，是否覆盖之前的步骤内容  
export NEXT_PUBLIC_INTERMEDIATE_STEP_OVERRIDE=true    
# 启用自动滚动 - 当有新消息或中间步骤时，自动滚动到最新内容  
export NEXT_PUBLIC_AUTO_SCROLL=true
# export NEXT_PUBLIC_CLEAR_STORAGE=false  

# 启用中间步骤显示功能  
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export NEXT_PUBLIC_WORKFLOW="智能研究助手"

# 激活Python虚拟环境  
echo "🔧 激活虚拟环境..."  
source ./NeMo-Agent-Toolkit/.venv/Scripts/activate  
  
# 直接启动后端服务（使用内置工具）  
echo "📡 启动智能学习助手后端服务..."  
nat serve --config_file configs/hackathon_configV6.yml --host 0.0.0.0 --port 8001 &  
# nat serve --config_file configs/hackathon_configV6.yml --host 0.0.0.0 --port 8001 --step_adaptor "{\"mode\": \"off\"}" > logs/backend.log 2>&1 &BACKEND_PID=$!
BACKEND_PID=$!  
  
# 等待后端启动  
echo "⏳ 等待后端服务启动..."  
sleep 10  
  
# 启动前端服务  
echo "🎨 启动前端服务..."  
cd external/aiqtoolkit-opensource-ui  
npm run dev &  
FRONTEND_PID=$!  
cd ../..  
  
echo ""  
echo "✅ 智能学习助手系统启动完成！"  
echo ""  
echo "🌐 访问地址:"  
echo "   前端界面: http://localhost:3000"  
echo "   API文档:  http://localhost:8001/docs"  
echo ""  
  
# 保存进程ID  
echo $BACKEND_PID > .backend.pid  
echo $FRONTEND_PID > .frontend.pid  
  
# 等待用户中断  
wait