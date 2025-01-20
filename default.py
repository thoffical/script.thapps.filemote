import xbmc
import xbmcgui
import xbmcaddon
import socket
import json

class FileMote:
    def __init__(self):
        self.addon = xbmcaddon.Addon(id='script.thapps.filemote')
        self.user_ip = self.addon.getSetting('user_ip')
        self.show_main_menu()

    def show_main_menu(self):
        options = ["Manage Android", "Manage macOS", "Manage Linux", "Manage Windows"]
        selected_option = xbmcgui.Dialog().select("Select an option", options)

        if selected_option >= 0:
            platform = options[selected_option]
            self.manage_files(platform)

    def manage_files(self, platform):
        xbmcgui.Dialog().notification("FileMote", f"You selected to manage files on {platform}.", xbmcgui.NOTIFICATION_INFO, 5000)

        if self.user_ip:
            self.connect_to_server(self.user_ip)

    def connect_to_server(self, address):
        try:
            host, port = address.split(':')
            port = int(port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                command = json.dumps({"action": "list_files"})
                sock.sendall(command.encode('utf-8'))

                response = sock.recv(4096)
                self.handle_server_response(response.decode('utf-8'))
        except Exception as e:
            xbmcgui.Dialog().notification("Error", str(e), xbmcgui.NOTIFICATION_ERROR, 5000)

    def handle_server_response(self, response):
        try:
            data = json.loads(response)
            xbmcgui.Dialog().notification("Server Response", str(data), xbmcgui.NOTIFICATION_INFO, 5000)
        except json.JSONDecodeError:
            xbmcgui.Dialog().notification("Error", "Failed to decode server response.", xbmcgui.NOTIFICATION_ERROR, 5000)

if __name__ == "__main__":
    FileMote()
