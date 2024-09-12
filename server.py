class RedisLikeServer:

    def __init__(self):
        self.store = {}

    def process_command(self, command):
        tokens = command.split()
        if not tokens:
            return "-ERR empty command\r\n"
        
        cmd = tokens[0].upper()
        
        if cmd == "SET" and len(tokens) == 3:
            key, value = tokens[1], tokens[2]
            self.store[key] = value
            return "+OK\r\n"
        
        elif cmd == "GET" and len(tokens) == 2:
            key = tokens[1]
            if key in self.store:
                value = self.store[key]
                return f"${len(value)}\r\n{value}\r\n"
            else:
                return "$-1\r\n"  # Key not found
        
        elif cmd == "DEL" and len(tokens) == 2:
            key = tokens[1]
            if key in self.store:
                del self.store[key]
                return ":1\r\n"  # 1 key removed
            else:
                return ":0\r\n"  # No key removed
        
        else:
            return "-ERR unknown command\r\n"