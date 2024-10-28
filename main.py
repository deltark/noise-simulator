from circuit_decomposer import *
from noise_simulator import *
from quantum_adder import *
from qiskit_aer import AerSimulator
from matplotlib import rc, colormaps
import matplotlib.pyplot as plt

backend = AerSimulator(method = 'statevector')

font = {'size': 14}

rc('font', **font)
colors = [colormaps["Blues"], colormaps["Reds"], colormaps["Purples"]]

b = 1
a_range = [0, 2, 4, 8, 16]

for i in range(3):
    plt.figure(i)

for j in range(5):
    a = a_range[j]
    results = [[],[],[]]

    # results0 = []
    # results1 = []
    # results2 = []

    true_res = a+b
    circ = quantum_sum(a, b)
    circ = decompose(circ)

    probas = np.arange(0, 0.8, 0.1)

    for p in probas:

        circ0 = apply_pauli_noise(p, 0, circ)
        circ1 = apply_pauli_noise(0, p, circ)
        circ2 = apply_pauli_noise(p, p, circ)

        job = backend.run([circ0, circ1, circ2])
        counts = job.result().get_counts()
        
        for i in range(3):
            res = int(max(counts[i]),2) #with no noise all shots will give the same result, but with noise not, so we take the max
            results[i].append(np.abs(res-true_res))

    for i in range(3):
        plt.figure(i)
        plt.plot(probas, results[i], marker="o", color=colors[i](80+j*20))

for i in range(3):
    plt.figure(i)
    plt.grid(True)
    plt.xlabel("Noise probability")
    plt.ylabel("Absolute error")
    plt.legend(["n=1", "n=2", "n=3", "n=4", "n=5"])
    plt.savefig('plots/plot'+str(i)+'.png')
