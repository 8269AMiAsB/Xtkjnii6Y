# 代码生成时间: 2025-09-22 02:22:11
import cherrypy
import json

# 定义主题切换的类
class ThemeSwitcher:
    exposed = True
    """
    这个类负责处理主题切换的请求。
    """

    def GET(self):
        """
        GET 请求处理函数，用于返回当前的主题设置。
        """
        theme = cherrypy.session.get('theme', 'default')
        return json.dumps({'theme': theme})

    def POST(self):
        """
        POST 请求处理函数，用于更新主题设置。
        """
        try:
            # 尝试解析 JSON 数据
            data = json.loads(cherrypy.request.body.read())
            theme = data.get('theme')
            if theme:
                # 更新会话中的主题设置
                cherrypy.session['theme'] = theme
                return json.dumps({'message': 'Theme updated successfully!', 'theme': theme})
            else:
                # 如果没有提供主题，则返回错误信息
                return json.dumps({'error': 'No theme provided'})
        except ValueError:
            # 如果 JSON 数据解析失败，则返回错误信息
            return json.dumps({'error': 'Invalid JSON data'})

# 配置 CherryPy 服务器
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
    },
    '/': {
        'tools.sessions.on': True,  # 启用会话支持
        'tools.sessions.timeout': 60,  # 会话超时时间（秒）
    },
}
def main():
    """
    主函数，用于启动 CherryPy 服务器。
    """
    cherrypy.quickstart(ThemeSwitcher(), config=config)

if __name__ == '__main__':
    main()
