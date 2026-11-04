
from pathlib import Path
import math
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Experiment settings
N_QUBITS = 3
TARGET = "101"
SHOTS = 4096

OUTPUT = Path(__file__).resolve().parent / "results"
OUTPUT.mkdir(exist_ok=True)


# Phase flip for the |111...1> state
def phase_flip_all_ones(qc, n):
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)


# Oracle: marks the target state
def apply_oracle(qc, target):
    n = len(target)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    phase_flip_all_ones(qc, n)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)


# Diffuser: amplifies the target amplitude
def apply_diffuser(qc, n):
    qc.h(range(n))
    qc.x(range(n))

    phase_flip_all_ones(qc, n)

    qc.x(range(n))
    qc.h(range(n))


# Build the Grover quantum circuit
def create_grover_circuit(n, target, iterations):
    if len(target) != n or any(bit not in "01" for bit in target):
        raise ValueError("Invalid target state")

    qc = QuantumCircuit(n, n)

    # Initialize equal superposition
    qc.h(range(n))

    # Grover iterations
    for _ in range(iterations):
        qc.barrier()
        apply_oracle(qc, target)
        qc.barrier()
        apply_diffuser(qc, n)

    qc.measure(range(n), range(n))
    return qc


# Calculate iteration count
N = 2 ** N_QUBITS
theta = math.asin(1 / math.sqrt(N))
iterations = math.floor(math.pi / (4 * theta))

# Create circuit
circuit = create_grover_circuit(N_QUBITS, TARGET, iterations)

# Run simulation
simulator = AerSimulator()
compiled = transpile(circuit, simulator)

result = simulator.run(
    compiled,
    shots=SHOTS,
    seed_simulator=42
).result()

counts = result.get_counts()

# Compare theoretical and simulated success
theoretical = math.sin((2 * iterations + 1) * theta) ** 2
experimental = counts.get(TARGET, 0) / SHOTS

print("=== GROVER SEARCH ===")
print(f"Qubits: {N_QUBITS}")
print(f"Target state: {TARGET}")
print(f"Iterations: {iterations}")
print(f"Measurements: {counts}")
print(f"Theoretical success: {theoretical:.4%}")
print(f"Simulated success: {experimental:.4%}")

# Save circuit image
fig = circuit.draw(output="mpl")
fig.savefig(
    OUTPUT / "grover_circuit.png",
    dpi=180,
    bbox_inches="tight"
)
plt.close(fig)

# Save histogram
fig = plot_histogram(counts, title="Grover Search Results")
fig.savefig(
    OUTPUT / "grover_histogram.png",
    dpi=180,
    bbox_inches="tight"
)
plt.close(fig)

print("\nExperiment completed successfully!")
