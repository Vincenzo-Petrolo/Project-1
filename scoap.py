from circuit import __AND__, __NAND__, __OR__, __NOR__, __NOT__, __BUF__, __XOR__, __XNOR__

class SCOAP(object):
    def __init__(self, circuit):
        self.circuit = circuit
        # Dictionary <node> -> (C0, C1)
        self.controllability = {}
        pass


    # return controllability
    # and then print it
    def getControllability(self):
        self._computeControllability()

        print(f"Node\t|\t(C0,C1)\t")
        print(f"----\t|\t-------\t")

        for node in self.controllability.keys():
            print(f"{node}\t|\t{self.controllability[node]}")



    # Algorithm for computing controllability
    def _computeControllability(self):
        # First levelize the circuit
        self.circuit.levelize()
        # Initialize the controllability with inputs
        self._initializeControllability()
        # Go through each sorted level
        for node_name in sorted(self.circuit.levels, key=self.circuit.levels.get):
                if (node_name not in self.controllability.keys()):
                    self._getNodeControllability(self.circuit.nodes[node_name])
    
    def _initializeControllability(self):
        # Initialize each input with (1,1)
        for input in self.circuit.inputs:
            self.controllability[input] = (1,1)

    def _getNodeControllability(self, node):
        # Create a list with the controllability of the inputs
        c_ins = []

        for input in node.fan_in:
            c_ins.append(self.controllability[input])

        # Compare the node function
        if (node.function == __AND__):
            self.controllability[node.name] = self.__AND_rule__(c_ins)
        elif (node.function == __NAND__):
            self.controllability[node.name] = self.__NAND_rule__(c_ins)
        elif (node.function == __OR__):
            self.controllability[node.name] = self.__OR_rule__(c_ins)
        elif (node.function == __NOR__):
            self.controllability[node.name] = self.__NOR_rule__(c_ins)
        elif (node.function == __NOT__):
            self.controllability[node.name] = self.__NOT_rule__(c_ins)
        elif (node.function == __BUF__):
            self.controllability[node.name] = self.__BUFF_rule__(c_ins)
    
    # List of tuples containing controllabilities
    # [(c0, c1), (c0, c1), ...]
    def __AND_rule__(self, c_ins):
        c0_ins = []
        c1_ins = []
        for c_node in c_ins:
            c0_ins.append(c_node[0])
            c1_ins.append(c_node[1])

        c0 = min(c0_ins) + 1
        c1 = sum(c1_ins) + 1

        return (c0, c1)

    def __NAND_rule__(self, c_ins):
        contr = self.__AND_rule__(c_ins)
        # Swap the tuple
        return (contr[1], contr[0])

    def __OR_rule__(self, c_ins):
        c0_ins = []
        c1_ins = []
        for c_node in c_ins:
            c0_ins.append(c_node[0])
            c1_ins.append(c_node[1])

        c0 = sum(c0_ins) + 1
        c1 = min(c1_ins) + 1

        return (c0, c1)

    def __NOR_rule__(self, c_ins):
        contr = self.__OR_rule__(c_ins)
        # Swap the tuple
        return (contr[1], contr[0])

    def __NOT_rule__(self, c_ins):
        c0 = c_ins[0][1] + 1
        c1 = c_ins[0][0] + 1

        return (c0, c1)

    def __BUFF_rule__(self, c_ins):
        contr = self.__NOT_rule__(c_ins)
        # Swap the tuple
        return (contr[1], contr[0])