# 代码生成时间: 2025-09-21 20:47:45
import os
import cherrypy
def list_files(directory):
    """
    List all files and subdirectories in the given directory.
    
    :param directory: Path to the directory to list contents.
    :return: A list of tuples containing (filepath, is_directory).
    """
    try:
        with os.scandir(directory) as entries:
            return [(entry.path, entry.is_dir()) for entry in entries]
    except PermissionError:
        raise cherrypy.HTTPError(403, "Permission denied to access directory.")
def organize_directory(directory,
                      move_unknown=True,
                      include_exts=None,
                      exclude_exts=None,
                      unknown_dir='Unknown'):
    """
    Organize files in the given directory by extension into subdirectories.
    
    :param directory: Path to the directory to organize.
    :param move_unknown: Whether to move files without an extension to 'Unknown' folder.
    :param include_exts: List of extensions to include in the organization.
    :param exclude_exts: List of extensions to exclude from the organization.
    :param unknown_dir: Name of the directory for files without an extension.
    """
    if include_exts is None:
        include_exts = []
    if exclude_exts is None:
        exclude_exts = []
    files = list_files(directory)
    for filepath, is_directory in files:
        if is_directory:
            continue
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower().lstrip('.')
        if ext in exclude_exts:
            continue
        if ext and ext not in include_exts:
            include_exts.append(ext)
        if move_unknown and not ext:
            dest_dir = os.path.join(directory, unknown_dir)
        elif ext in include_exts:
            dest_dir = os.path.join(directory, ext)
        else:
            continue
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_path = os.path.join(dest_dir, filename)
        os.rename(filepath, dest_path)

def main():
    # Set the configuration for CherryPy
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                             'server.socket_port': 8080})
    # Mount the web application
    cherrypy.tree.mount(OrganizerApp(), '/', {'/': {'tools.sessions.on': True}})
    # Start the CherryPy engine
    cherrypy.engine.start()
    cherrypy.engine.block()

def run_server():
    """
    Entry point for the CherryPy application.
    This function sets up the application and starts the server.
    """
    if __name__ == '__main__':
        main()

c =有机组织器
lass OrganizerApp():
    exposed = True
    """
    CherryPy application class for organizing directories.
    """
    @cherrypy.expose
    def index(self):
        return "<h1>Folder Organizer</h1>"
    """
    Endpoint to organize a directory.
    """
    @cherrypy.expose
    def organize(self, directory, move_unknown='true', include_exts='', exclude_exts='', unknown_dir='Unknown'):
        try:
            # Convert string arguments to their respective types
            move_unknown = move_unknown.lower() == 'true'
            include_exts = [ext.strip() for ext in include_exts.split(',')] if include_exts else []
            exclude_exts = [ext.strip() for ext in exclude_exts.split(',')] if exclude_exts else []
            organize_directory(directory,
                             move_unknown,
                             include_exts,
                             exclude_exts,
                             unknown_dir)
            return "<h1>Directory organized successfully</h1>"
        except Exception as e:
            return f"<h1>Error organizing directory: {str(e)}</h1>"

c = run_server(
