from chat.Node_chatbot import Node_chatbot

class Tree_chatbot:
    def __init__(self):
        self.root = None
        self.chatbot = Node_chatbot()

    def add(self, question, answer):
        if self.root is None:
            self.root = Node_chatbot(question, answer)
        else:
            self._add(question, answer, self.root)

    def _add(self, question, answer, node):
        if question < node.question:
            if node.left is not None:
                self._add(question, answer, node.left)
            else:
                node.left = Node_chatbot(question, answer)
        else:
            if node.right is not None:
                self._add(question, answer, node.right)
            else:
                node.right = Node_chatbot(question, answer)

    def find(self, question):
        if self.root is not None:
            return self._find(question, self.root)
        else:
            return None

    def _find(self, question, node):
        if question == node.question:
            return node
        elif (question < node.question and node.left is not None):
            self._find(question, node.left)
        elif (question > node.question and node.right is not None):
            self._find(question, node.right)

    def delete_tree(self):
        self.root = None