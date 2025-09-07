#!/bin/bash  
  
echo "🛑 停止智能学习助手 - NVIDIA NeMo Agent Toolkit"  
echo "=============================================="  
  
# 停止后端服务  
if [ -f .backend.pid ]; then  
    BACKEND_PID=$(cat .backend.pid)  
    if ps -p $BACKEND_PID > /dev/null; then  
        echo "停止后端服务 (PID: $BACKEND_PID)..."  
        kill $BACKEND_PID  
    fi  
    rm -f .backend.pid  
fi  
  
# 停止前端服务  
if [ -f .frontend.pid ]; then  
    FRONTEND_PID=$(cat .frontend.pid)  
    if ps -p $FRONTEND_PID > /dev/null; then  
        echo "停止前端服务 (PID: $FRONTEND_PID)..."  
        kill $FRONTEND_PID  
    fi  
    rm -f .frontend.pid  
fi  
  
# 停止MCP Omnisearch服务  
if [ -f .omnisearch.pid ]; then  
    OMNISEARCH_PID=$(cat .omnisearch.pid)  
    if ps -p $OMNISEARCH_PID > /dev/null; then  
        echo "停止MCP Omnisearch服务 (PID: $OMNISEARCH_PID)..."  
        kill $OMNISEARCH_PID  
    fi  
    rm -f .omnisearch.pid  
fi  
  
# 清理其他相关进程  
pkill -f "nat serve" 2>/dev/null || true  
pkill -f "node.*mcp-omnisearch" 2>/dev/null || true  
pkill -f "npm run dev" 2>/dev/null || true  
  
echo "✅ 所有服务已停止"