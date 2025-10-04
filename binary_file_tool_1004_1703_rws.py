# 代码生成时间: 2025-10-04 17:03:53
import cherrypy
import os

# 定义一个类，用于处理二进制文件的读写操作
class BinaryFileTool:
    def __init__(self):
        pass

    # 上传文件并保存到指定目录
    @cherrypy.expose
    def upload(self, file=None):
        if file:
            try:
                # 获取文件名和文件内容
                filename = file.filename
                content = file.file.read()

                # 指定保存目录
                save_dir = 'uploaded_files'
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                # 构造保存路径
                save_path = os.path.join(save_dir, filename)
                with open(save_path, 'wb') as f:
                    f.write(content)

                return 'File uploaded successfully'
            except Exception as e:
                return f'Error: {str(e)}'
        else:
            return 'No file uploaded'

    # 读取指定目录下的文件内容
    @cherrypy.expose
    def read(self, filename):
        try:
            # 指定要读取的文件路径
            read_dir = 'uploaded_files'
            read_path = os.path.join(read_dir, filename)

            # 检查文件是否存在
            if os.path.exists(read_path):
                with open(read_path, 'rb') as f:
                    content = f.read()
                return content  # 返回文件内容
            else:
                return 'File not found'
        except Exception as e:
            return f'Error: {str(e)}'

# 配置CherryPy服务器
cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})

# 注册路由和视图函数
root = BinaryFileTool()
cherrypy.tree.mount(root, '/')

if __name__ == '__main__':
    cherrypy.quickstart(root)
