# Homework 1 python code
import parser as p

# Create the parser object
parser = p.Parser()

# Read file and get the circuit

circuit = parser.readFile("test.bench")

# Print the circuit
print(circuit)
