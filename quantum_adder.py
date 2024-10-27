from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import *
import numpy as np

def quantum_sum(a, b):

    backend = AerSimulator(method = 'statevector')

    n = max(a.bit_length(), b.bit_length())
    rega, regb = QuantumRegister(n+1), QuantumRegister(n)
    regc = ClassicalRegister(n+1)

    circ = QuantumCircuit(regb, rega, regc)
    circ.initialize(a, rega)
    circ.initialize(b, regb)
    qft(circ, rega)

    for j in range(n):
        angle = (2*np.pi) / (2 ** (j+2))
        circ.cp(angle, regb[n-j-1], rega[n])

    for i in range(n):
        for j in range(i,n):
            angle = (2*np.pi) / (2 ** (j-i+1))
            circ.cp(angle, regb[n-j-1], rega[n-1-i])

    # circ.append(qft(n+1).inverse(), rega)
    qft_dagger(circ, rega)

    circ.measure(rega, regc)
    # print(circ)

    # circ.reset(regb)

    # circ.save_statevector()
    job = backend.run(circ)
    counts = job.result().get_counts()
    res = int(max(counts),2)
    return res

def qft(circ, reg):
    """Implements Quantum Fourier Transform on given circuit and register"""
    
    n = len(reg)

    for i in range(n):
        circ.h(reg[n-i-1])
        # Apply controlled rotations for qubits to the right of the i-th qubit
        for j in range(i+1, n):
            angle = (2*np.pi) / (2 ** (j - i+1))
            circ.cp(angle, reg[n-j-1], reg[n-i-1])
    # # Reverse the order of the qubits
    # for i in range(n // 2):
    #     circ.swap(reg[i], reg[n - i - 1])

def qft_dagger(qc, reg):
    """Implements inverse QFT on given circuit and register"""

    n = len(reg)
    # # Reverse the qubit order for QFT†
    # for i in range(n // 2):
    #     qc.swap(reg[i], reg[n - i - 1])
    # Apply the inverse QFT
    for i in range(n):
        for j in range(i):
            angle = -(2*np.pi) / (2 ** ((n-j) - (n-i-1)))
            qc.cp(angle, reg[j], reg[i])
        qc.h(reg[i])

# print(quantum_sum(55,6))