import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import *

def apply_pauli_noise(p_a: float, p_b: float, circ: QuantumCircuit):
    """
    Implements the Pauli noise model specified by probability parameters p_a and p_b on given quantum circuit

    Args:
        p_a: Probability of having a random Pauli operator acting on the qubit after a one-qubit gate 
        p_b: Probability of having a random Pauli operator acting on the qubit after a two-qubit gate
        circ: Quantum circuit where the noise will be added

    Returns:
        noisy_circ: Quantum circuit with noise added.
    """

    #initialize circuit with same number of qubits as input
    noisy_circ = QuantumCircuit(circ.num_qubits)

    for instruct in circ.data:
        noisy_circ.append(instruct)
        if instruct.is_controlled_gate():
            print(instruct.qubits)
            #append pauli on target(?) qubit with prob. p_b
            if np.random.rand()<p_b: noisy_circ.append(random_pauli(), [instruct.qubits[0]]) #TODO : which qubit ??
        else:
            #append pauli on qubit with prob p_a
            print(instruct.qubits)
            if np.random.rand()<p_a: noisy_circ.append(random_pauli(), instruct.qubits)

    return noisy_circ

def random_pauli():
    dice = np.random.rand()
    if dice < 1/3: return XGate()
    elif dice >= 2/3: return YGate()
    else: return ZGate()

#test
# circ = QuantumCircuit(2)
# circ.h(0)
# circ.cx(0,1)
# print(circ)
# print(apply_pauli_noise(0.5, 0.25, circ))