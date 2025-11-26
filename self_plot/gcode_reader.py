def read_file(file_name):
    with open(file_name, 'r') as f:
        file_instructions = (str(f.read()).split("\n"))
    
    for i in range(len(file_instructions)): 
        file_instructions[i] = file_instructions[i].split()

    return file_instructions
