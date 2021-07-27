import socket
class Server:
    def __init__(self,port):
        HOST = '127.0.0.1'# host -> socket.gethostname() use to set machine IP
        PORT = port
        self.baseHeaders = "HTTP/1.1"
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.my_socket.bind((HOST,PORT))
        self.my_socket.listen(1)
        self.path = {"/":self.index}
        self.black_list_ip = []
    def index(self, *args):
        return str(args)
    def Server(self):
        while True:
            connection,address = self.my_socket.accept()
            if address[0] in self.black_list_ip:
                connection.close()
            else:
                req = connection.recv(1024).decode('utf-8')
                path = ""
                for re in req.split("\n"):
                    pathx = re.split(" ")
                    try:
                        if pathx[0] == "GET":
                            path = pathx[1]
                    except:
                        pass
                if self.WAF(req):
                    try:
                        http = self.path["/" + path.split("/")[1]](path.split("/")).encode()
                        connection.send(self.statue_code(200) + http)
                    except KeyError:
                        http = open("template/404.html", "r", encoding="utf-8").read().encode()
                        connection.send(self.statue_code(404) + http)
                    except:
                        connection.send(self.statue_code(500) + b"500 Internal Server Error")
                        pass
                else:
                    connection.send("HTTP/1.1 403 Forbidden\n\n".encode())
                connection.close()
    def statue_code(self, code):
        if code == 200:
            return "HTTP/1.1 200 OK\n\n".encode()
        elif code == 403:
            return "HTTP/1.1 403 Forbidden\n\n".encode("utf-8")
        elif code == 404:
            return "HTTP/1.1 404 Not Found\n\n".encode("utf-8")
        elif code == 500:
 11:13:52 bash Tue Jul 27 - 25 | ~/Desktop/projet/nwss 
        elif code == 201:
            return f"{self.baseHeaders} 201 Created\n\n".encode()
    def WAF(self, req):
        self.neededHeaders = ["Host",
                            "User-Agent",
                            "Accept",
                            "Accept-Language",
                            "Accept-Encoding",
                            "Connection",
                            "Cookie",
                            "Cache-Control"]
        headers = req.split('\r\n')
        here = 0
        for _header in headers:
            header = _header.split(":")
            if header[0] in self.neededHeaders:
                here += 1
            try:
                if header[0] == "User-agent":
                    pass
            except:
                pass
        if here > 5:
            return True
        else:
            return False
    def AddPath(self, path, filelink):
        self.path[f"{path}"] = filelink

    def BlackListIp(self, ip):
        self.black_list_ip.append(ip)

    def RemoveBlackListIp(self, ip):
        self.black_list_ip.remove(ip)
if __name__ == "__main__":
    server = Server(8080)
    def example(*args):
        return "Hellow world " + str(args)
    server.AddPath("/hi", example)

    server.Server()
