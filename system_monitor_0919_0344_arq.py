# 代码生成时间: 2025-09-19 03:44:31
import os
import psutil
# TODO: 优化性能
import cherrypy
def get_system_info():
    # 获取系统的基本信息
    system_info = {
        'cpu_usage': psutil.cpu_percent(),
# 增强安全性
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'uptime': int(psutil.boot_time()),
    }
    return system_info
def get_process_info():
    # 获取所有进程的基本信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            processes.append({
                'pid': proc.info['pid'],
# 扩展功能模块
                'name': proc.info['name'],
                'create_time': proc.info['create_time'],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes
def get_network_info():
    # 获取网络接口的基本信息
    network_info = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_INET:  # IPv4 address
                network_info.append({
                    'interface': interface,
                    'ip_address': addr.address,
                })
    return network_info
def main():
    # 设置CherryPy服务器
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    
    # 定义路由
    cherrypy.tree.mount(get_system_info, '/system')
    cherrypy.tree.mount(get_process_info, '/processes')
# 扩展功能模块
    cherrypy.tree.mount(get_network_info, '/network')
    cherrypy.engine.start()
# TODO: 优化性能
    cherrypy.engine.block()
def run():
    # 运行服务器
    try:
        main()
    except KeyboardInterrupt:
        print('Server stopped.')
# NOTE: 重要实现细节
    except Exception as e:
        print(f'Error: {e}')
def entry_point():
    # 程序入口点
# 扩展功能模块
    if __name__ == '__main__':
        run()
"""
System Performance Monitoring Tool using Python and CherryPy

This tool provides a simple web API to monitor the system's performance,
including CPU usage, memory usage, disk usage, uptime, processes, and network interfaces.
It is designed to be easy to use, extensible, and scalable.
"""
entry_point()