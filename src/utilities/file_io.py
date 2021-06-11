def read_file(path):
  file = open(path, "r")
  content = file.read()
  file.close()
  return content

def write_to_file(path, str):
  file = open(path, "w")
  file.write(str)
  file.close()