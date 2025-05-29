class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None
        self.data = 0

class DirectMappedCache:
    def __init__(self, size=8):
        self.size = size
        self.lines = [CacheLine() for _ in range(size)]

    def read(self, address):
        index = address % self.size
        line = self.lines[index]
        tag = address // self.size

        if line.valid and line.tag == tag:
            print(f"[CACHE HIT] Dir {address} => {line.data}")
            return line.data
        else:
            print(f"[CACHE MISS] Dir {address}")
            line.valid = True
            line.tag = tag
            line.data = 0
            return line.data

    def write(self, address, value):
        index = address % self.size
        tag = address // self.size
        line = self.lines[index]
        line.valid = True
        line.tag = tag
        line.data = value
        print(f"[CACHE WRITE] Dir {address} <= {value}")
