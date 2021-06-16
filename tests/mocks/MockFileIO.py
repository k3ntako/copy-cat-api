class MockFileIO:
    def __init__(self, mock_read_output = ['']):
        self.mock_read_output_idx = 0
        self.mock_read_output = mock_read_output
        
        self.read_file_path = []
        self.write_to_file_path = []
        self.write_to_file_str = []

    def read_file(self, path):
        self.read_file_path.append(path)

        if len(self.mock_read_output) <= self.mock_read_output_idx + 1:
            return self.mock_read_output[-1]

        return_str = self.mock_read_output[self.mock_read_output_idx]

        # increment after retrieving value
        self.mock_read_output_idx = self.mock_read_output_idx + 1
        
        return return_str

    def write_to_file(self, path, str):
        self.write_to_file_path.append(path)
        self.write_to_file_str.append(str)
