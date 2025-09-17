# 代码生成时间: 2025-09-17 10:48:33
import cherrypy
import requests
from urllib.parse import urlparse
import socket

"""
A CherryPy application to validate URL links.

This application will check if a given URL is valid, by verifying
if it can be reached and if it has a valid scheme and netloc.
"""

class URLValidator:
    """A class to handle URL validation requests."""

    @cherrypy.expose
    def validate(self, url):
        """
        Validates the given URL.

        Args:
            url (str): The URL to be validated.

        Returns:
            A JSON response with the validation result.
        """
        try:
            # Parse the URL to check for a valid scheme and netloc
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return self._response(False, 'Invalid URL: missing scheme or netloc.')

            # Check if the URL is reachable
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return self._response(True, 'URL is valid and reachable.')
            else:
                return self._response(False, 'URL is not reachable.')

        except (requests.ConnectionError, requests.Timeout, socket.gaierror):
            return self._response(False, 'URL is not reachable or cannot be resolved.')
        except ValueError:
            return self._response(False, 'Invalid URL format.')

    def _response(self, is_valid, message):
        """
        Returns a JSON response with the validation result.

        Args:
            is_valid (bool): Whether the URL is valid.
            message (str): A message describing the result.

        Returns:
            A JSON object with the validation result.
        """
        return cherrypy.lib.jsonify({'is_valid': is_valid, 'message': message})

if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(URLValidator(), config=conf)
