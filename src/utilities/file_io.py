class FileIO:
  def read_file(self, path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

  def write_to_file(self, path, str):
    file = open(path, "w")
    file.write(str)
    file.close()