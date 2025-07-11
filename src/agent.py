class Agent:
    def __init__(self, name:str, personality:str):
        self.name = name
        self.personality = personality
        self.memory = []
        self.inventory = []
    