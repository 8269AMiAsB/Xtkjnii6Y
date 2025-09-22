# 代码生成时间: 2025-09-23 01:19:10
import os
import shutil
import cherrypy
from cherrypy.lib.static import serve_file
from datetime import datetime
from zipfile import ZipFile
import logging

# 设置日志配置
logging.basicConfig(filename='backup_sync.log', level=logging.INFO)

class FileBackupSync(object):
    """文件备份和同步工具"""
    @cherrypy.expose
    def backup(self, source, destination):
        """备份文件到指定目的地"""
        try:
            shutil.copy(source, destination)
            logging.info(f"备份文件 {source} 到 {destination} 成功")
            return {"status": "success", "message": f"备份文件 {source} 到 {destination} 成功"}
        except Exception as e:
            logging.error(f"备份文件 {source} 到 {destination} 失败: {str(e)}")
            return {"status": "error", "message": f"备份文件 {source} 到 {destination} 失败: {str(e)}"}

    @cherrypy.expose
    def sync(self, source, destination):
        """同步文件到指定目的地"""
        try:
            if os.path.exists(destination):
                # 压缩目标文件夹
                with ZipFile(f"{destination}.zip", 'w') as zipfile:
                    for root, dirs, files in os.walk(destination):
                        for file in files:
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, destination)
                            zipfile.write(file_path, rel_path)
                # 将压缩文件移动到源文件夹
                shutil.move(f"{destination}.zip", source)
                logging.info(f"同步文件从 {source} 到 {destination} 成功")
                return {"status": "success", "message": f"同步文件从 {source} 到 {destination} 成功"}
            else:
                raise FileNotFoundError(f"目标文件夹 {destination} 不存在")
        except Exception as e:
            logging.error(f"同步文件从 {source} 到 {destination} 失败: {str(e)}")
            return {"status": "error", "message": f"同步文件从 {source} 到 {destination} 失败: {str(e)}"}

    @cherrypy.expose
    def download_backup(self, filename):
        """下载备份文件"""
        try:
            file_path = os.path.join("backups", filename)
            if os.path.exists(file_path):
                return serve_file(file_path, content_type='application/octet-stream', disposition='attachment; filename=%s' % filename)
            else:
                raise FileNotFoundError(f"备份文件 {filename} 不存在")
        except Exception as e:
            logging.error(f"下载备份文件 {filename} 失败: {str(e)}")
            return {"status": "error", "message": f"下载备份文件 {filename} 失败: {str(e)}"}

    @cherrypy.expose
    def upload_backup(self, file):
        """上传备份文件"""
        try:
            file_path = os.path.join("backups", file.filename)
            with open(file_path, 'wb') as f:
                f.write(file.file.read())
            logging.info(f"上传备份文件 {file.filename} 成功")
            return {"status": "success", "message": f"上传备份文件 {file.filename} 成功"}
        except Exception as e:
            logging.error(f"上传备份文件 {file.filename} 失败: {str(e)}")
            return {"status": "error", "message": f"上传备份文件 {file.filename} 失败: {str(e)}"}

if __name__ == '__main__':
    # 配置CherryPy服务器
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    # 配置静态文件夹
    cherrypy.quickstart(FileBackupSync())