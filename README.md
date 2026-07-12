# Hybrid Sudoku Solver

A Python implementation of a Sudoku solver that combines deterministic constraint propagation with MRV-guided adaptive backtracking.

## Features

- Constraint propagation
- Candidate elimination
- Lone-candidate detection
- Minimum Remaining Values (MRV) heuristic
- Adaptive backtracking

## Overview

The solver first applies deterministic logical techniques to reduce the search space. When no further logical deductions are possible, it uses MRV-guided backtracking to efficiently solve the remaining puzzle while minimizing brute-force exploration.

## Language

- Python
