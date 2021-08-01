import socket, time

class Server:
    def __init__(self, port=8080):
        HOST = '127.0.0.1'# host -> socket.gethostname() use to set machine IP
        PORT = port
        self.waf = {}
        self.param = {}
        self.param["xss"] = True
        self.param["bodysize"] = 256
        self.param["waf"] = True
        self.baseHeaders = "HTTP/1.1"
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.my_socket.bind((HOST,PORT))
        self.my_socket.listen(1)
        self.path = {"/":self.index}
        self.black_list_ip = []
        self.whitelist = []
    def index(self, *args):
        return open("index.html", "r").read()
    def run(self):
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
                if self.WAF(req, address, path):
                    try:
                        try:
                            http = self.path[path.split("?")[0]](path.split("?")[1].split("&")).encode()
                        except:
                            http = self.path[path.split("?")[0]](None).encode()
                        connection.send(self.statue_code(200) + http)
                    except KeyError:
                        http = open("template/404.html", "r", encoding="utf-8").read().encode()
                        connection.send(self.statue_code(404) + http)
                    except:
                        connection.send(self.statue_code(500) + b"500 Internal Server Error")
                        pass
                else:
                    connection.send("HTTP/1.1 403 Forbidden\n\nFirewall say noow get out i dont trust you".encode())
                connection.close()
    def statue_code(self, code):
        if code == 200:
            return "HTTP/1.1 200 OK\n\n".encode()
        elif code == 403:
            return "HTTP/1.1 403 Forbidden\n\n".encode("utf-8")
        elif code == 404:
            return "HTTP/1.1 404 Not Found\n\n".encode("utf-8")
        elif code == 500:
            return "HTTP/1.1 500 Internal Server Error\n\n".encode("utf-8")
        elif code == 201:
            return "HTTP/1.1 201 Created\n\n".encode()
    def WAF(self, req, conn, path):
        """
        
        firewall function don't use it

        """
        conn = conn[0]
        if self.param["waf"] == False or conn in self.whitelist:
            return True
        
        try:
            if time.time() - self.waf[conn][0] < 10:
                self.waf[conn][1] += 1
                if self.waf[conn][1] > 10:
                    self.BlackListIp(conn)
                return False
            elif len(req) < self.param["bodysize"]:
                return False
            else:
                pass
                
        except:
            pass
        if self.param["xss"] and self.Check_xss(path):
            pass
        else:
            return False
        self.waf[conn] = [time.time(), 0]
        self.needed_headers = ["Host",
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
            if header[0] in self.needed_headers:
                here += 1
            try:
                if header[0] == "User-agent":
                    pass
            except:
                pass
        if here > 5:
            return True
        else:
            return True
    def AddPath(self, path, filelink):
        self.path[path] = filelink

    def BlackListIp(self, ip):
        self.black_list_ip.append(ip)
    def Check_xss(self, path):
        if "<script" in path.lower():
            return False
        else:
            return True

    def RemoveBlackListIp(self, ip):
        """
        remove ip to black list
        """
        self.black_list_ip.remove(ip)

    def WhiteList(self, ip):
        """
        add ip to white list 
        """
        self.whitelist.append(ip)
    def Reditect(self, url_to_redirect):
        return "HTTP/1.1 303 See Other\r\nLocation: " + url_to_redirect + "\n\n".encode()


