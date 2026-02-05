# Automated-Network-Validation-Framework
This project implements a lightweight network validation framework inspired by
pre- and post-change verification workflows used in large-scale network operations.

The framework validates:
- Routing reachability
- Latency
- Packet loss

across multi-router or multi-node IP topologies.

## Motivation

In production networks, configuration changes (routing updates, maintenance,
scaling events) require automated validation to ensure:
- Reachability is preserved
- Performance regressions are detected early
- Failures are isolated quickly

This project simulates those workflows in a simple, repeatable way.

## Features

- Config-driven topology definition
- Reachability checks using ICMP
- Latency measurement
- Packet loss estimation
- Consolidated validation report
## Project Structure
- src/ Validation logic 
- config/ Topology configuration 
- sample_output/ Example validation output
## Usage
```bash
1. Install dependencies:
pip install -r requirements.txt
2. Define your topology:
Edit config/topology.yaml
3. Run validation:
python src/validate_network.py
