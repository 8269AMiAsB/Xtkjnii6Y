# 代码生成时间: 2025-10-06 22:41:47
import cherrypy
from cherrypy import tools

# 模拟数据库存储会员积分
class MemberPointsDatabase:
    def __init__(self):
        self.points = {}

    def get_points(self, member_id):
        """获取会员积分"""
        return self.points.get(member_id, 0)

    def add_points(self, member_id, points):
        """为会员增加积分"""
        if member_id in self.points:
            self.points[member_id] += points
        else:
            self.points[member_id] = points
        return self.points[member_id]

    def subtract_points(self, member_id, points):
        """为会员扣除积分"""
        if member_id in self.points and self.points[member_id] >= points:
            self.points[member_id] -= points
            return self.points[member_id]
        else:
            raise ValueError("Insufficient points")


# 会员积分系统服务
class MemberPointsService:
    def __init__(self):
        self.db = MemberPointsDatabase()

    @cherrypy.expose
    def get_points(self, member_id):
        """Endpoint to get member points"""
        try:
            points = self.db.get_points(member_id)
            return {"member_id": member_id, "points": points}
        except Exception as e:
            return {"error": str(e)}

    @cherrypy.expose
    def add_points(self, member_id, points):
        """Endpoint to add points to a member"""
        try:
            result = self.db.add_points(member_id, int(points))
            return {"member_id": member_id, "points": result}
        except Exception as e:
            return {"error": str(e)}

    @cherrypy.expose
    def subtract_points(self, member_id, points):
        """Endpoint to subtract points from a member"""
        try:
            result = self.db.subtract_points(member_id, int(points))
            return {"member_id": member_id, "points": result}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

# 设置CherryPy服务器配置
def setup_server():
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080})
    cherrypy.quickstart(MemberPointsService())

if __name__ == '__main__':
    setup_server()
