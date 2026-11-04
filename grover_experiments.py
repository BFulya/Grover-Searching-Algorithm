
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

SHOTS = 4096
MAX_ITERATIONS = 7

EXPERIMENTS = {
    2: "11",
    3: "101",
    4: "1011",
    5: "10101"
}

OUTPUT = Path(__file__).resolve().parent / "experiment_results"
OUTPUT.mkdir(exist_ok=True)

simulator = AerSimulator()


def phase_flip(qc, n):
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)


def apply_oracle(qc, target):
    n = len(target)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    phase_flip(qc, n)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)


def apply_diffuser(qc, n):
    qc.h(range(n))
    qc.x(range(n))

    phase_flip(qc, n)

    qc.x(range(n))
    qc.h(range(n))


def run_experiment(n, target, iterations):
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(iterations):
        apply_oracle(qc, target)
        apply_diffuser(qc, n)

    qc.measure(range(n), range(n))

    compiled = transpile(qc, simulator)
    result = simulator.run(
        compiled,
        shots=SHOTS,
        seed_simulator=42
    ).result()

    counts = result.get_counts()
    return counts.get(target, 0) / SHOTS


def theoretical_probability(n, iterations):
    theta = math.asin(1 / math.sqrt(2 ** n))
    return math.sin((2 * iterations + 1) * theta) ** 2


all_results = []

for n, target in EXPERIMENTS.items():
    theta = math.asin(1 / math.sqrt(2 ** n))
    optimal = math.floor(math.pi / (4 * theta))

    print(f"\n=== {n} QUBITS | TARGET: {target} ===")
    print(f"Recommended iterations: {optimal}")

    iterations_list = []
    theoretical_list = []
    simulated_list = []

    for iterations in range(MAX_ITERATIONS + 1):
        theory = theoretical_probability(n, iterations)
        simulated = run_experiment(n, target, iterations)

        iterations_list.append(iterations)
        theoretical_list.append(theory * 100)
        simulated_list.append(simulated * 100)

        all_results.append({
            "qubits": n,
            "target": target,
            "iterations": iterations,
            "theoretical_percent": round(theory * 100, 4),
            "simulated_percent": round(simulated * 100, 4),
            "difference_pp": round(
                abs(theory - simulated) * 100, 4
            )
        })

        print(
            f"Iteration {iterations}: "
            f"Theory={theory * 100:.2f}% | "
            f"Simulation={simulated * 100:.2f}%"
        )

    # Success probability comparison graph
    plt.figure(figsize=(9, 5))

    plt.plot(
        iterations_list,
        theoretical_list,
        marker="o",
        label="Theoretical"
    )

    plt.plot(
        iterations_list,
        simulated_list,
        marker="s",
        linestyle="--",
        label="Qiskit Simulation"
    )

    plt.axvline(
        optimal,
        linestyle=":",
        label=f"Recommended iteration: {optimal}"
    )

    plt.xlabel("Grover Iterations")
    plt.ylabel("Success Probability (%)")
    plt.title(f"Grover Algorithm - {n} Qubits")
    plt.xticks(iterations_list)
    plt.ylim(0, 105)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT / f"grover_{n}_qubits_comparison.png",
        dpi=200
    )

    plt.close()


# Save all results as CSV
csv_path = OUTPUT / "grover_experimental_results.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "qubits",
            "target",
            "iterations",
            "theoretical_percent",
            "simulated_percent",
            "difference_pp"
        ]
    )
    writer.writeheader()
    writer.writerows(all_results)

print("\nALL 32 EXPERIMENTS COMPLETED!")
print(f"Results saved to: {OUTPUT}")
