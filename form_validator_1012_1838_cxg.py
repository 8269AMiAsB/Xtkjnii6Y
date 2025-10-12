# 代码生成时间: 2025-10-12 18:38:38
import cherrypy
from cherrypy.lib import static

# 表单数据验证器类
class FormValidator:
    def __init__(self):
        self.errors = []

    # 验证表单数据
    def validate(self, params):
        # 检查是否所有必需的字段都存在
        required_fields = ["username", "password", "email"]
        for field in required_fields:
            if field not in params or not params[field]:
                self.errors.append(f"{field} is required")
                return False

        # 验证用户名
        if not self.is_valid_username(params["username"]):
            self.errors.append("Invalid username")
            return False

        # 验证密码
        if not self.is_valid_password(params["password"]):
            self.errors.append("Invalid password")
            return False

        # 验证电子邮件
        if not self.is_valid_email(params["email"]):
            self.errors.append("Invalid email")
            return False

        return True

    # 验证用户名
    def is_valid_username(self, username):
        # 用户名应为3-20字符，只能包含字母、数字和下划线
        return 3 <= len(username) <= 20 and username.isalnum() or username.isalpha() or '_' in username

    # 验证密码
    def is_valid_password(self, password):
        # 密码应为6-20字符，至少包含一个数字和一个字母
        if 6 <= len(password) <= 20:
            has_digit = any(char.isdigit() for char in password)
            has_alpha = any(char.isalpha() for char in password)
            return has_digit and has_alpha
        return False

    # 验证电子邮件
    def is_valid_email(self, email):
        # 简单的电子邮件验证，使用正则表达式
        import re
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(email_pattern, email))


# CherryPy配置
class FormApp:
    @cherrypy.expose
    def index(self):
        # 展示表单页面
        return static.serve_file("form.html")

    @cherrypy.expose
    def submit(self, **params):
        # 创建表单验证器实例
        validator = FormValidator()

        # 验证表单数据
        if validator.validate(params):
            return "Form data is valid"
        else:
            # 返回错误信息
            errors = ", ".join(validator.errors)
            return f"Form validation errors: {errors}"

# 配置CherryPy
config = {
    "global": {
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080,
    },
    "/static": {
        "tools.staticdir.root": os.path.abspath(os.getcwd()),
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "static",
    },
}

# 启动CherryPy应用
if __name__ == "__main__":
    cherrypy.quickstart(FormApp(), config=cherrypy.Config("").merge(config))
