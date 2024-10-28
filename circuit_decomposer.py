import numpy as np
from qiskit.circuit import QuantumCircuit, CircuitInstruction
from qiskit.circuit.library import *
from qiskit.quantum_info import Operator

def decompose(circ: QuantumCircuit, equiv_library=0):
    """
    Decomposes input circuit into the set of basis gates: {CX,ID,RZ,SX,X}

    Args:
        circ: circuit to decompose (must only contain 1 and 2-qubit gates)

    Returns:
        decomposed_circuit: circuit that implements the same operation as circ, but written with only the above basis gates.
    """
    basis_set = ['x', 'cx', 'sx', 'rz', 'id', 'reset', 'measure']
    decomposed_circuit = QuantumCircuit(circ.qubits, circ.clbits)
    circ = circ.decompose([Initialize, StatePreparation], 2)
    circ = circ.decompose(CRZGate)
    # print(decomposed_circuit)

    for instruct in circ.data:

        qubits = instruct.qubits
        # if len(qubits) > 2:
        #     raise Error("Circuit contains gates that act on more than 2 qubits. Please decompose all gates into operations with only 1 and 2-qubit gates.")

        if instruct.name in basis_set:
            decomposed_circuit.append(instruct)

        elif instruct.name == 'h':
            decomposed_circuit.sx(instruct.qubits)
            decomposed_circuit.rz(np.pi/2, instruct.qubits)
            decomposed_circuit.sx(instruct.qubits)

        else: decomposed_circuit.append(instruct)

        # elif instruct.name == 'p':


        # elif instruct.name == 'cp':
        #     decomposed_circuit.append(instruct.decompose())

        # elif instruct.name in equiv_library:
        #     decomposed_circuit.append("""pre-registered equivalence""", qubits)

        # else :
        #     if len(qubits) == 1: decomposed_op = euler_decomposer(instruct)
        #     else: decomposed_op = two_qubit_decomposer(instruct)

        #     decomposed_circuit.append(decomposed_op)
        #     #TODO: add new equivalence to equiv_library       

    return decomposed_circuit

# def euler_decomposer(instruct: CircuitInstruction):

#     #minimize matrix of decomposition - matrix of instruct w/ parameters
#     instruct_matrix = Operator(instruct).data

    
#     euler_params = np.array([])
#     euler_circuit = QuantumCircuit(1)
#     euler_circuit.rz()

#     return decomposed_instruct

# circ = QuantumCircuit(2)
# circ.cx(1,0)
# print(circ)
# instruct = circ.data[0]
# print(Operator(circ).data)