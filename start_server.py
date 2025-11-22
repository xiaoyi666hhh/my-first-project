import os
import sys
import time
from datetime import datetime
import socket
import traceback

# 设置基础目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"===== 飞机大战游戏服务器启动 =====")
print(f"基础目录: {BASE_DIR}")

# 检查HTML文件
html_file = os.path.join(BASE_DIR, "飞机大战.html")
if os.path.exists(html_file):
    print(f"找到HTML文件: {html_file}, 大小: {os.path.getsize(html_file)}字节")
else:
    print(f"错误: 找不到HTML文件: {html_file}")
    sys.exit(1)

# 导入Flask
from flask import Flask, send_file, make_response, request, jsonify

# 创建Flask应用
app = Flask(__name__, static_folder=None)
server_start_time = datetime.now()

# 全局错误处理
@app.errorhandler(500)
def internal_server_error(error):
    error_info = traceback.format_exc()
    client_ip = request.remote_addr
    print(f"[ERROR] 500错误来自 {client_ip}: {str(error)}")
    print(f"错误详情: {error_info}")
    return jsonify({'error': '服务器内部错误', 'message': '请稍后重试'}), 500

@app.errorhandler(404)
def not_found_error(error):
    client_ip = request.remote_addr
    path = request.path
    print(f"[INFO] 404错误 - {client_ip} 访问: {path}")
    return jsonify({'error': '资源不存在', 'path': path}), 404

# 根路径返回游戏HTML
@app.route('/')
def game_index():
    client_ip = request.remote_addr
    print(f"[INFO] {client_ip} 正在访问飞机大战游戏")
    
    try:
        # 二进制读取HTML文件
        with open(html_file, 'rb') as f:
            content = f.read()
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    except Exception as e:
        print(f"[ERROR] 读取HTML文件失败: {str(e)}")
        return jsonify({'error': '文件读取失败', 'message': str(e)}), 500

# 静态文件服务 - 支持图片和音乐
@app.route('/<path:filename>')
def serve_static(filename):
    client_ip = request.remote_addr
    print(f"[INFO] {client_ip} 请求文件: {filename}")
    
    # 多路径查找
    search_paths = [
        os.path.join(BASE_DIR, filename),
        os.path.join(BASE_DIR, 'image', filename),
        os.path.join(BASE_DIR, 'music', filename),
        os.path.join(BASE_DIR, 'image', '飞机image', filename)
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            print(f"[INFO] 找到文件: {path}")
            return send_file(path)
    
    print(f"[WARN] 文件不存在: {filename}")
    return jsonify({'error': '文件不存在', 'filename': filename}), 404

# 游戏状态接口
@app.route('/api/status')
def game_status():
    uptime = datetime.now() - server_start_time
    return jsonify({
        'status': 'running',
        'game': '飞机大战',
        'uptime': str(uptime),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # 获取所有网络地址
    try:
        interfaces = socket.getaddrinfo(socket.gethostname(), None)
        ip_addresses = set()
        for interface in interfaces:
            addr = interface[4][0]
            if ':' not in addr:  # IPv4
                ip_addresses.add(addr)
        
        print("\n服务器将在以下地址可用:")
        for ip in ip_addresses:
            print(f"  http://{ip}:5000/")
        print("  http://127.0.0.1:5000/")
        
    except Exception as e:
        print(f"获取网络地址失败: {str(e)}")
    
    print("\n正在启动游戏服务器...")
    print("按 Ctrl+C 停止服务器")
    print("==================================")
    
    # 启动服务器
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"\n服务器启动失败: {str(e)}")
        traceback.print_exc()