class Item: 
    def __init__(self, id: str, title: str, input: str, output: str):
        self.id = id
        self.title = title
        self.input = input
        self.output = output
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "input": self.input,
            "output": self.output
        }