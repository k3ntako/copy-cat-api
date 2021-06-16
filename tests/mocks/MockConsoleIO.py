class MockConsoleIO:
    def __init__(self):
        self.print_arg = []

    def print(self, str): 
        self.print_arg.append(str)