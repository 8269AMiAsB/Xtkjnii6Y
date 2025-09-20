# 代码生成时间: 2025-09-21 02:11:25
import cherrypy
import random

def generate_random_number(min_value=0, max_value=100):
    """
    Generate a random number between min_value and max_value.

    :param min_value: The minimum value of the random number (inclusive).
    :param max_value: The maximum value of the random number (inclusive).
    :return: A random number between min_value and max_value.
    """
    try:
        if min_value > max_value:
            raise ValueError("min_value cannot be greater than max_value.")
        return random.randint(min_value, max_value)
    except ValueError as e:
        raise cherrypy.HTTPError(400, str(e))

class RandomNumberGenerator:
    """
    A CherryPy class for generating random numbers.
    """
    @cherrypy.expose
    def index(self):
        return "This is the Random Number Generator service."

    @cherrypy.expose
    def get_random_number(self, min_val=0, max_val=100):
        """
        Endpoint to get a random number.

        :param min_val: The minimum value for the random number.
        :param max_val: The maximum value for the random number.
        :return: A JSON object containing the random number.
        """
        try:
            random_number = generate_random_number(int(min_val), int(max_val))
            return {"random_number": random_number}
        except ValueError:
            raise cherrypy.HTTPError(400, "Invalid input values.")

if __name__ == "__main__":
    # CherryPy configuration
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080,
                             'tools.encode.on': True,
                             'tools.encode.encoding': 'utf-8'})
    # Mount the application
    cherrypy.quickstart(RandomNumberGenerator())