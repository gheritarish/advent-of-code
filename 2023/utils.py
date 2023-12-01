def read_file(name):
    with open(name, "r") as file:
        lines = file.readlines()
    return lines
