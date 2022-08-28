# Homework 1 python code
import parser as p

# Create the parser object
parser = p.Parser()

filename = input("Please write the name of the file you want to read: ")
# Read the file and get the circuit

circuit = parser.readFile(filename)

# Print the circuit
print(circuit)
