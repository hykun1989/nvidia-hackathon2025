# from flask import Flask, send_from_directory, jsonify, request  
# import os  
# import requests  
# import logging  
# import sys  
# from datetime import datetime  
  
# # 配置详细的日志记录  
# logging.basicConfig(  
#     level=logging.DEBUG,  
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
#     handlers=[  
#         logging.FileHandler('frontend_debug.log'),  
#         logging.StreamHandler(sys.stdout)  
#     ]  
# )  
  
# app = Flask(__name__)  
# logger = logging.getLogger(__name__)  
  
# # 启动时记录基本信息  
# logger.info("=" * 50)  
# logger.info("Flask 前端服务器启动")  
# logger.info(f"当前工作目录: {os.getcwd()}")  
# logger.info(f"Flask应用目录: {os.path.dirname(os.path.abspath(__file__))}")  
# logger.info(f"启动时间: {datetime.now()}")  
# logger.info("=" * 50)  
  
# @app.before_request  
# def log_request_info():  
#     logger.info(f"收到请求: {request.method} {request.url}")  
#     logger.info(f"请求头: {dict(request.headers)}")  
#     if request.method == 'POST':  
#         logger.info(f"请求体: {request.get_data()}")  
  
# @app.after_request  
# def log_response_info(response):  
#     logger.info(f"响应状态: {response.status_code}")  
#     logger.info(f"响应头: {dict(response.headers)}")  
#     return response  
  
# @app.route('/')  
# def serve_index():  
#     try:  
#         logger.info("尝试提供 index.html 文件")  
#         index_path = os.path.join('.', 'index.html')  
#         logger.info(f"查找文件路径: {os.path.abspath(index_path)}")  
          
#         if os.path.exists(index_path):  
#             logger.info("index.html 文件存在，正在提供")  
#             return send_from_directory('.', 'index.html')  
#         else:  
#             logger.error(f"index.html 文件不存在于路径: {os.path.abspath(index_path)}")  
#             # 列出当前目录的所有文件  
#             files = os.listdir('.')  
#             logger.info(f"当前目录文件列表: {files}")  
#             return jsonify({'error': 'index.html not found', 'files': files}), 404  
              
#     except Exception as e:  
#         logger.error(f"提供 index.html 时发生错误: {str(e)}")  
#         logger.exception("详细错误信息:")  
#         return jsonify({'error': str(e)}), 500  
  
# @app.route('/<path:path>')  
# def serve_static(path):  
#     try:  
#         logger.info(f"尝试提供静态文件: {path}")  
#         full_path = os.path.abspath(path)  
#         logger.info(f"完整文件路径: {full_path}")  
          
#         if os.path.exists(path):  
#             logger.info(f"文件存在，正在提供: {path}")  
#             return send_from_directory('.', path)  
#         else:  
#             logger.warning(f"文件不存在: {path}，回退到 index.html")  
#             return send_from_directory('.', 'index.html')  
              
#     except Exception as e:  
#         logger.error(f"提供静态文件 {path} 时发生错误: {str(e)}")  
#         logger.exception("详细错误信息:")  
#         return jsonify({'error': str(e)}), 500  
  
# @app.route('/chat/stream', methods=['POST'])  
# def proxy_chat():  
#     try:  
#         logger.info("收到 /chat/stream 请求")  
          
#         # 获取请求数据  
#         request_data = request.get_json()  
#         logger.info(f"请求数据: {request_data}")  
          
#         # 检查后端服务是否可用  
#         backend_url = 'http://localhost:8001/chat/stream'  
#         logger.info(f"尝试连接后端服务: {backend_url}")  
          
#         # 发送请求到后端  
#         response = requests.post(  
#             backend_url,  
#             json=request_data,  
#             headers={'Content-Type': 'application/json'},  
#             stream=True,  
#             timeout=30  # 添加超时设置  
#         )  
          
#         logger.info(f"后端响应状态码: {response.status_code}")  
#         logger.info(f"后端响应头: {dict(response.headers)}")  
          
#         return response.content, response.status_code, response.headers.items()  
          
#     except requests.exceptions.ConnectionError as e:  
#         logger.error(f"无法连接到后端服务 (8001端口): {str(e)}")  
#         return jsonify({  
#             'error': '无法连接到后端服务',  
#             'details': '请确保后端服务在8001端口正常运行',  
#             'backend_url': 'http://localhost:8001/chat/stream'  
#         }), 503  
          
#     except requests.exceptions.Timeout as e:  
#         logger.error(f"后端服务请求超时: {str(e)}")  
#         return jsonify({'error': '后端服务请求超时'}), 504  
          
#     except Exception as e:  
#         logger.error(f"代理请求时发生错误: {str(e)}")  
#         logger.exception("详细错误信息:")  
#         return jsonify({'error': str(e)}), 500  
  
# @app.errorhandler(404)  
# def not_found(error):  
#     logger.error(f"404错误: {request.url}")  
#     return jsonify({'error': 'Page not found', 'url': request.url}), 404  
  
# @app.errorhandler(500)  
# def internal_error(error):  
#     logger.error(f"500错误: {str(error)}")  
#     return jsonify({'error': 'Internal server error'}), 500  
  
# if __name__ == '__main__':  
#     try:  
#         logger.info("准备启动Flask应用")  
#         logger.info("检查端口5000是否可用...")  
          
#         # 检查当前目录结构  
#         logger.info(f"当前目录内容: {os.listdir('.')}")  
          
#         # 启动应用  
#         logger.info("启动Flask应用在 0.0.0.0:5000")  
#         app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)  
          
#     except Exception as e:  
#         logger.error(f"启动Flask应用时发生错误: {str(e)}")  
#         logger.exception("详细错误信息:")


from flask import Flask, send_from_directory, jsonify, request, Response
import os
import requests
import logging
import sys
import json # 添加这一行
from datetime import datetime

# 配置详细的日志记录（强制UTF-8编码）
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('frontend_debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 让jsonify输出中文
app.config['PREFERRED_URL_SCHEME'] = 'http' # 明确设置URL scheme

logger = logging.getLogger(__name__)

# 启动时记录基本信息
logger.info("=" * 50)
logger.info("Flask 前端服务器启动")
logger.info(f"当前工作目录: {os.getcwd()}")
logger.info(f"Flask应用目录: {os.path.dirname(os.path.abspath(__file__))}")
logger.info(f"启动时间: {datetime.now()}")
logger.info("=" * 50)

@app.before_request
def log_request_info():
    logger.info(f"收到请求: {request.method} {request.url}")
    logger.info(f"请求头: {dict(request.headers)}")
    if request.method == 'POST':
        logger.info(f"请求体: {request.get_data().decode('utf-8', errors='replace')}")

@app.after_request
def log_response_info(response):
    logger.info(f"响应状态: {response.status_code}")
    logger.info(f"响应头: {dict(response.headers)}")
    return response

@app.route('/')
def serve_index():
    try:
        logger.info("尝试提供 index.html 文件")
        index_path = os.path.join('.', 'index.html')
        logger.info(f"查找文件路径: {os.path.abspath(index_path)}")
        if os.path.exists(index_path):
            logger.info("index.html 文件存在，正在提供")
            return send_from_directory('.', 'index.html')
        else:
            logger.error(f"index.html 文件不存在于路径: {os.path.abspath(index_path)}")
            files = os.listdir('.')
            logger.info(f"当前目录文件列表: {files}")
            return jsonify({'error': 'index.html not found', 'files': files}), 404
    except Exception as e:
        logger.error(f"提供 index.html 时发生错误: {str(e)}")
        logger.exception("详细错误信息:")
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.info(f"尝试提供静态文件: {path}")
        full_path = os.path.abspath(path)
        logger.info(f"完整文件路径: {full_path}")
        if os.path.exists(path):
            logger.info(f"文件存在，正在提供: {path}")
            return send_from_directory('.', path)
        else:
            logger.warning(f"文件不存在: {path}，回退到 index.html")
            return send_from_directory('.', 'index.html')
    except Exception as e:
        logger.error(f"提供静态文件 {path} 时发生错误: {str(e)}")
        logger.exception("详细错误信息:")
        return jsonify({'error': str(e)}), 500

@app.route('/chat/stream', methods=['POST'])
def proxy_chat():
    try:
        logger.info("收到 /chat/stream 请求")
        # 尝试手动解码请求体
        raw_data = request.get_data()
        try:
            request_data = raw_data.decode('utf-8')
            logger.info(f"请求数据 (UTF-8 解码): {request_data}")
            request_data = json.loads(request_data) # 将解码后的字符串解析为JSON
        except Exception as e:
            logger.error(f"请求体解码或JSON解析失败: {e}")
            logger.info(f"原始请求体: {raw_data}")
            return jsonify({'error': '请求体解码或JSON解析失败', 'details': str(e)}), 400
        backend_url = 'http://localhost:8001/chat/stream'
        logger.info(f"尝试连接后端服务: {backend_url}")
        response = requests.post(
            backend_url,
            json=request_data,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            stream=True,
            timeout=30
        )
        logger.info(f"后端响应状态码: {response.status_code}")
        logger.info(f"后端响应头: {dict(response.headers)}")
        # 用 Flask Response 保证流式和编码
        return Response(
            response.iter_content(chunk_size=4096),
            status=response.status_code,
            content_type=response.headers.get('content-type', 'text/event-stream; charset=utf-8')
        )
    except requests.exceptions.ConnectionError as e:
        logger.error(f"无法连接到后端服务 (8001端口): {str(e)}")
        return jsonify({
            'error': '无法连接到后端服务',
            'details': '请确保后端服务在8001端口正常运行',
            'backend_url': 'http://localhost:8001/chat/stream'
        }), 503
    except requests.exceptions.Timeout as e:
        logger.error(f"后端服务请求超时: {str(e)}")
        return jsonify({'error': '后端服务请求超时'}), 504
    except Exception as e:
        logger.error(f"代理请求时发生错误: {str(e)}")
        logger.exception("详细错误信息:")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404错误: {request.url}")
    return jsonify({'error': 'Page not found', 'url': request.url}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500错误: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        logger.info("准备启动Flask应用")
        logger.info("检查端口5000是否可用...")
        logger.info(f"当前目录内容: {os.listdir('.')}")
        logger.info("启动Flask应用在 0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except Exception as e:
        logger.error(f"启动Flask应用时发生错误: {str(e)}")
        logger.exception("详细错误信息:")