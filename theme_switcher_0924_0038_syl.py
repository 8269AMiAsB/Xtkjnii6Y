# 代码生成时间: 2025-09-24 00:38:58
import cherrypy

# 定义一个全局变量来存储当前的主题
current_theme = 'default'


class ThemeSwitcher:
    """
    ThemeSwitcher 类用于处理主题切换功能。
    """

def set_theme(theme_name):
    """
    设置当前主题的装饰器。
    """
    if theme_name not in ['default', 'dark', 'light']:
        raise ValueError('Invalid theme name')
    global current_theme
    current_theme = theme_name
    return cherrypy.tools.response_headers.append(
        ('Content-Type', 'text/html; charset=utf-8')
    )

def expose_theme():
    """
    返回当前主题的装饰器。
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['X-Theme'] = current_theme
            return f(*args, **kwargs)
        return wrapper
    return decorator

def switch_theme(theme_name):
    """
    切换主题的函数。
    """
    try:
        set_theme(theme_name)
        return f'Theme switched to {theme_name}'
    except ValueError as e:
        return str(e), 400

def default_page():
    """
    返回默认页面的函数。
    """
    return f'Current theme is {current_theme}'

def index():
    """
    主页函数。
    """
    return 'Welcome to the Theme Switcher!'

def theme_page(theme_name):
    """
    主题页面函数。
    """
    return switch_theme(theme_name)

# 设置 CherryPy 配置
cherrypy.config.update({'server.socket_host': '127.0.0.1',
                           'server.socket_port': 8080})

# 设置路由
cherrypy.tree.mount(index, '/', {'/': {'tools.response_headers.on': True}})
cherrypy.tree.mount(default_page, '/default', {'/': {'tools.response_headers.on': True}})
cherrypy.tree.mount(theme_page, '/theme/{theme_name}',
                   {'/': {'tools.response_headers.on': True}})

# 启动 CherryPy 服务器
if __name__ == '__main__':
    cherrypy.quickstart(ThemeSwitcher)