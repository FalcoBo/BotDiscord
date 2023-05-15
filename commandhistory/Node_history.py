class Node_history:
    def __init__(self, command):
        self.command = command
        self.next = None
        self.last = None
        self.size = 1