# 代码生成时间: 2025-09-17 16:48:05
import cherrypy
import psutil
import os
import platform

"""
A CherryPy application that provides an endpoint to display the memory usage statistics.
"""

class MemoryUsageAnalyzer:
    def __init__(self):
        # Initialize any required properties or setup here
        pass

    @cherrypy.expose
    def index(self):
        """
        Endpoint to display the memory usage statistics.
        """
        try:
            # Retrieve memory usage statistics
            memory_stats = self.get_memory_stats()
            return self.format_memory_stats(memory_stats)
        except Exception as e:
            # Handle any exceptions and return an error message
            return f"Error retrieving memory usage: {str(e)}"

    def get_memory_stats(self):
        """
        Get the memory usage statistics from the system.
        """
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percentage": memory.percent,
            "swap_total": memory.total_swap if platform.system() != 'Windows' else 0,
            "swap_used": memory.used_swap if platform.system() != 'Windows' else 0,
            "swap_free": memory.free_swap if platform.system() != 'Windows' else 0,
            "swap_percentage": memory.percent_swap if platform.system() != 'Windows' else 0
        }

    def format_memory_stats(self, stats):
        """
        Format the memory usage statistics into a readable string.
        """
        formatted_stats = f"Total Memory: {stats['total']} bytes
"
        formatted_stats += f"Available Memory: {stats['available']} bytes
"
        formatted_stats += f"Used Memory: {stats['used']} bytes
"
        formatted_stats += f"Memory Usage Percentage: {stats['percentage']}%
"
        if 'swap_total' in stats:
            formatted_stats += f"Total Swap: {stats['swap_total']} bytes
"
            formatted_stats += f"Used Swap: {stats['swap_used']} bytes
"
            formatted_stats += f"Free Swap: {stats['swap_free']} bytes
"
            formatted_stats += f"Swap Usage Percentage: {stats['swap_percentage']}%
"
        return formatted_stats

if __name__ == '__main__':
    # Configure and start the CherryPy server
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(MemoryUsageAnalyzer(), '/', config=conf)