from circuit_decomposer import *
from noise_simulator import *
from quantum_adder import *
from qiskit_aer import AerSimulator

backend = AerSimulator(method = 'statevector')

circ = quantum_sum(12, 3)
decomposed_circ = decompose(circ)
# print(decomposed_circ)
noisy_circ = apply_pauli_noise(0, 0, decomposed_circ)

# print(noisy_circ)

job = backend.run(noisy_circ)
counts = job.result().get_counts()
res = int(max(counts),2)

print(counts)
print(res)