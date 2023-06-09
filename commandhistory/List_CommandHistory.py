from commandhistory.Node_history import Node_history

class List_CommandHistory:
    def __init__(self):
        self.first = None
        self.last = self.first
        self.size = 0
        self.index = 0

    def append_command(self, command):
        current_node = Node_history(command)
        if self.first is None:
            self.first = current_node
            self.last = current_node
        else:
            self.last.next = current_node
            self.last = current_node
        self.index += 1

    def get_first_command(self):
        return self.first.command
    
    def get_last_command(self):
        if self.last is None:
            return None
        else:
            return self.last.command
    
    def get_user_commands(self):
        commandslist = {}
        if self.first is not None:
            current_node = self.first
            while current_node is not None:
                commandslist.append(current_node.command)
                current_node = current_node.next
            return commandslist
        else:
            return "Aucune commande enregistrée"
            
    def get_size(self):
        if self.first is None:
            return "Aucune commande enregistrée"
        return self.size

    def get_index_command(self, index):
        self.index = self.first
        for i in range(index):
            if index > self.size:
                self.index = self.first
            else :
                self.index = self.index.next
        return self.index.command

    def clear_history(self):
        self.first = None
        self.last = None
        self.index = 0
        self.size = 0