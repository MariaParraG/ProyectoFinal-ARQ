class InterruptController:
    def __init__(self):
        self.interrupt_flag = False

    def trigger(self):
        self.interrupt_flag = True

    def clear(self):
        self.interrupt_flag = False

    def is_pending(self):
        return self.interrupt_flag
