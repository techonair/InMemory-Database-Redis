import threading
from server import RedisLikeServer

class InitializeServer:

    def handle_client(self, client_socket, redis_server):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            command = data.decode('utf-8').strip()
            response = redis_server.process_command(command)
            client_socket.send(response.encode('utf-8'))

        client_socket.close()

    def start_server(self, host='localhost', port=6379):
        """
        * Server will start on localhost:6379
        * If server doesn't start please check if any application is running on port 6379
        * Server supports multi-client 
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        redis_server = RedisLikeServer()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            # Start a new thread to handle each client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, redis_server))
            client_handler.start()

if __name__ == "__main__":
    InitializeServer().start_server()