def read_file(file_name):
    with open(file_name, 'r') as f:
        file_instructions = (str(f.read()).split("\n"))
    
    for i in range(len(file_instructions)): 
        file_instructions[i] = file_instructions[i].split()

    return file_instructions

if __name__ == "__main__":
    print(read_file("circle.gcode"), "\n")
    print(read_file("line.gcode"), "\n")
    print(read_file("square.gcode"), "\n")
    print(read_file("circle_and_square.gcode"), "\n")