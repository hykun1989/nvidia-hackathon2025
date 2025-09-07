#!/bin/bash  
  
echo "🚀 启动智能学习助手 - NVIDIA NeMo Agent Toolkit"  
echo "=============================================="  
  
# 创建日志目录  
mkdir -p logs  
  
# 设置环境变量  
export MEM0_API_KEY=you_api_key  
export NVIDIA_API_KEY=you_api_key  
export TAVILY_API_KEY=you_api_key  
export GOOGLE_API_KEY=you_api_key  
  
# 前端UI配置  
export NEXT_PUBLIC_ENABLE_INTERMEDIATE_STEPS=true  
export NEXT_PUBLIC_EXPAND_INTERMEDIATE_STEPS=true  
export NEXT_PUBLIC_INTERMEDIATE_STEP_OVERRIDE=true  
export NEXT_PUBLIC_AUTO_SCROLL=true  
export NEXT_PUBLIC_CLEAR_STORAGE=true  
  
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  
  
# 激活Python虚拟环境  
echo "🔧 激活虚拟环境..."  
source ./NeMo-Agent-Toolkit/.venv/Scripts/activate  
  
# 检查端口占用情况  
echo "🔍 检查端口占用情况..."  
echo "检查8001端口:"  
netstat -ano | findstr :8001 || echo "8001端口未被占用"  
echo "检查5000端口:"  
netstat -ano | findstr :5000 || echo "5000端口未被占用"  
  
# 启动后端服务  
echo "📡 启动智能学习助手后端服务..."  
nat serve --config_file configs/hackathon_configV6.yml --host 0.0.0.0 --port 8001 > logs/backend.log 2>&1 &  
# nat serve --config_file configs/hackathon_configV6.yml --host 0.0.0.0 --port 8001 --step_adaptor '{"mode": "off"}' > logs/backend.log 2>&1 &BACKEND_PID=$!
echo "后端服务PID: $BACKEND_PID"  
  
# 等待后端启动并检查  
echo "⏳ 等待后端服务启动..."  
sleep 15

# 等待后端服务启动并检查 (最多重试 10 次，每次间隔 5 秒)
echo "🔍 检查后端服务状态..."
for i in {1..10}; do
    curl -s http://localhost:8001/health > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ 后端服务启动成功"
        break
    else
        echo "⏳ 后端服务未就绪，等待 5 秒后重试... ($i/10)"
        sleep 5
    fi
done

# 最终检查
curl -s http://localhost:8001/health > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ 后端服务启动失败，检查日志:"
    tail -20 logs/backend.log
    exit 1
fi
  
# 启动前端服务  
echo "🎨 启动前端服务..."  
  
# 检查 frontend_new 目录  
if [ ! -d "frontend_new" ]; then  
    echo "❌ 错误: frontend_new 目录不存在"  
    echo "当前目录内容:"  
    ls -la  
    exit 1  
fi  
  
echo "📁 frontend_new 目录内容:"  
ls -la frontend_new/  
  
# 进入前端目录并启动  
cd frontend_new  
echo "📍 当前目录: $(pwd)"  
echo "📁 当前目录内容:"  
ls -la  
  
echo "🚀 启动Flask前端服务..."  
python server.py > ../logs/frontend.log 2>&1 &  
FRONTEND_PID=$!  
echo "前端服务PID: $FRONTEND_PID"  
  
cd ..  
  
# 等待前端启动  
sleep 5  
  
# 检查前端服务状态  
echo "🔍 检查前端服务状态..."  
curl -s http://localhost:5000/ > /dev/null  
if [ $? -eq 0 ]; then  
    echo "✅ 前端服务启动成功"  
else  
    echo "❌ 前端服务启动失败，检查日志:"  
    tail -20 logs/frontend.log  
fi  
  
echo ""  
echo "✅ 智能学习助手系统启动完成！"  
echo ""  
echo "🌐 访问地址:"  
echo "   前端界面: http://localhost:5000"  
echo "   后端API:  http://localhost:8001"  
echo "   API文档:  http://localhost:8001/docs"  
echo ""  
echo "📋 日志文件:"  
echo "   后端日志: logs/backend.log"  
echo "   前端日志: logs/frontend.log"  
echo "   前端调试: frontend_new/frontend_debug.log"  
echo ""  
  
# 保存进程ID  
echo $BACKEND_PID > .backend.pid  
echo $FRONTEND_PID > .frontend.pid  
  
# 实时显示日志  
echo "📊 实时日志 (Ctrl+C 停止):"  
tail -f logs/frontend.log logs/backend.log