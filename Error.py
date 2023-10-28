class Error:
    def __init__(self, error_type, statement, description = "", position = 0):
        self.error_type = error_type
        self.statement = statement
        self.description = description
        self.position = position
    
    def output(self):
        print(self.error_type)
        print(self.description)
        print()
        print(self.statement)
        print(" " * self.position, "^", sep="")
        
class Success:
    def __init__(self, code = 0):
        self.code = 0