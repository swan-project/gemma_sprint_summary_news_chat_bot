class Item: 
    def __init__(self, id: str, mode: str, title: str, input: str, output: str):
        self.id = id
        self.mode = mode
        self.title = title
        self.input = input
        self.output = output
        
    def to_dict(self):
        return {
            "id": self.id,
            "mode": self.mode,
            "title": self.title,
            "input": self.input,
            "output": self.output
        }