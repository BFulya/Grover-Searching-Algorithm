
# Grover Search Algorithm Using Qiskit

## Project Overview

This project implements Grover's Quantum Search Algorithm
using Python, Qiskit, and Qiskit AerSimulator.

The algorithm uses quantum amplitude amplification to
increase the probability of measuring a marked state in
an unstructured search space.

## Objectives

- Implement Grover's quantum oracle.
- Implement the diffusion operator.
- Construct and simulate quantum circuits.
- Test 2, 3, 4, and 5 qubits.
- Analyze iteration counts from 0 to 7.
- Compare theoretical and simulated success probabilities.
- Visualize the experimental results.

## Technologies

- Python 3.12
- Qiskit
- Qiskit AerSimulator
- NumPy
- Matplotlib

## Installation

Create a virtual environment:

    py -3.12 -m venv .venv

Install dependencies:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Run the Algorithms

Basic Grover experiment:

    .\.venv\Scripts\python.exe .\grover.py

Multiple-qubit experiments:

    .\.venv\Scripts\python.exe .\grover_experiments.py

## Experimental Setup

- Qubit counts: 2, 3, 4, 5
- Iterations: 0 through 7
- Measurements per experiment: 4096
- Total experiments: 32
- Simulation: Ideal Qiskit AerSimulator

## Theoretical Background

For a single marked state:

P(r) = sin²((2r + 1)θ)

where:

θ = arcsin(1 / sqrt(N))
N = 2^n

Here, n is the qubit count and r is the number of
Grover iterations.

## Experimental Results

The simulated probabilities closely match theoretical
predictions.

The results demonstrate that increasing the number of
iterations beyond the first optimum can decrease the
success probability.

## Limitations

The experiments use an ideal quantum simulator.
Real quantum hardware introduces noise, gate errors,
and measurement errors.

## Conclusion

Grover's algorithm provides a quadratic improvement
in oracle query complexity for unstructured search,
reducing O(N) classical queries to O(sqrt(N)) quantum
oracle queries under the standard oracle model.
