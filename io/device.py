from queue import Queue

class FakeIODevice:
    def __init__(self):
        self.buffer = Queue()
        self.ready = False

    def push_data(self, data):
        self.buffer.put(data)
        self.ready = True

    def read(self):
        if self.ready and not self.buffer.empty():
            data = self.buffer.get()
            if self.buffer.empty():
                self.ready = False
            return data
        return None

    def is_ready(self):
        return self.ready
