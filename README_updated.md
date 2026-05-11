# Automated Network Validation Framework

A Python-based network validation framework that uses a source of truth to validate network device reachability, latency, and packet loss. The project supports both local YAML files and NetBox as inventory sources, then generates human-readable and machine-readable reports.

## Project Purpose

The goal of this project is to automate common network validation checks that are often performed manually before or after network changes.

Instead of manually checking each device one by one, this framework:

- Loads intended network inventory from YAML or NetBox
- Reads validation rules from a policy file
- Runs network checks such as reachability, latency, and packet loss
- Generates text and JSON reports
- Separates inventory, validation logic, reporting, and configuration into clean modules

This project demonstrates practical network automation, Python scripting, source-of-truth design, NetBox integration, and DevOps-style project organization.

---

## High-Level Architecture

```text
YAML / NetBox
     |
     v
Source of Truth Layer
     |
     v
Validation Engine
     |
     v
Validators
     |
     v
Report Writer
     |
     v
Text Report + JSON Report


---

## Full Repository Structure

```text
Automated-Network-Validation-Framework/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── source_of_truth/
│   ├── devices.yaml
│   ├── sites.yaml
│   └── validation_checks.yaml
│
├── src/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── source_of_truth/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── yaml_source.py
│   │   ├── netbox_source.py
│   │   └── validation_policy.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── reachability.py
│   │   ├── latency.py
│   │   └── packet_loss.py
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   └── validation_engine.py
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   └── report_writer.py
│   │
│   └── main.py
│
├── scripts/
│   ├── populate_netbox.py
│   └── view_netbox_inventory.py
│
├── reports/
│   ├── validation_report.txt
│   └── validation_report.json
│
└── tests/
    └── test_validation.py
```

---


## Example `devices.yaml`

```yaml
devices:
  - hostname: router1
    site: dc1
    role: edge-router
    platform: cisco_ios
    mgmt_ip: 192.168.56.101

  - hostname: router2
    site: dc1
    role: core-router
    platform: cisco_ios
    mgmt_ip: 192.168.56.102

  - hostname: switch1
    site: branch1
    role: access-switch
    platform: cisco_ios
    mgmt_ip: 192.168.56.103
```

---

## Example `sites.yaml`

```yaml
sites:
  - name: dc1
    slug: dc1
    region: east
    description: Primary data center

  - name: branch1
    slug: branch1
    region: east
    description: Branch office site
```

---

## Example `validation_checks.yaml`

```yaml
checks:
  - name: reachability
    enabled: true

  - name: latency
    enabled: true
    max_latency_ms: 100

  - name: packet_loss
    enabled: true
    max_packet_loss_percent: 0
```

---

## How the Framework Works

### Step 1: Select inventory source

The user chooses the inventory source when running the program.

For YAML inventory:

```bash
python -m src.main --source yaml
```

For NetBox inventory:

```bash
python -m src.main --source netbox
```

### Step 2: Load inventory

If the source is YAML, the framework reads:

```text
source_of_truth/devices.yaml
source_of_truth/sites.yaml
```

If the source is NetBox, the framework connects to the NetBox API and pulls device and site information.

### Step 3: Load validation policy

The framework reads:

```text
source_of_truth/validation_checks.yaml
```

This file defines which checks are enabled and what thresholds should be used.

### Step 4: Run validation engine

The validation engine loops through each device and runs enabled checks.

### Step 5: Generate reports

The framework writes:

```text
reports/validation_report.txt
reports/validation_report.json
```

---

## Current Validation Checks

### Reachability Check

Checks whether the management IP address of a device responds to ping.

Purpose:

```text
Can the device be reached over the network?
```

### Latency Check

Measures average round-trip time and compares it against a threshold.

Purpose:

```text
Is the device reachable within an acceptable delay?
```

### Packet Loss Check

Measures packet loss percentage and compares it against a threshold.

Purpose:

```text
Is the path to the device stable?
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Automated-Network-Validation-Framework.git
cd Automated-Network-Validation-Framework
```

Create a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install the required packages manually:

```bash
pip install pyyaml pynetbox pytest
```

Then generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Running the Project with YAML

From the repository root:

```bash
source venv/bin/activate
python -m src.main --source yaml
```

View the text report:

```bash
cat reports/validation_report.txt
```

View the JSON report:

```bash
python -m json.tool reports/validation_report.json
```

---

## Running the Project with NetBox

Start NetBox Docker:

```bash
cd ~/netbox-docker
docker compose up -d
docker compose ps
```

Go back to the project:

```bash
cd ~/neteng/Automated-Network-Validation-Framework
source venv/bin/activate
```

Set NetBox environment variables:

```bash
export NETBOX_URL="http://127.0.0.1:8000"
export NETBOX_TOKEN="your_netbox_api_token_here"
```

Run the validation framework using NetBox:

```bash
python -m src.main --source netbox
```

View reports:

```bash
cat reports/validation_report.txt
python -m json.tool reports/validation_report.json
```

---

## Using a `.env` File

To avoid exporting the NetBox variables manually every time, create a `.env` file in the project root:

```bash
nano .env
```

Add:

```bash
export NETBOX_URL="your netbox_url"
export NETBOX_TOKEN="your_netbox_api_token_here"
```

Load it before running NetBox mode:

```bash
source .env
python -m src.main --source netbox
```

Make sure `.env` is not committed to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
reports/*.json
reports/*.txt
```

---

## NetBox Helper Scripts

### Populate NetBox

This script can be used to populate NetBox with sample devices and sites from the local YAML source of truth.

```bash
python scripts/populate_netbox.py
```

### View NetBox Inventory

This script can be used to confirm that NetBox has devices and sites loaded.

```bash
python scripts/view_netbox_inventory.py
```


---

## Commands Summary

Run with YAML:

```bash
cd ~/neteng/Automated-Network-Validation-Framework
source venv/bin/activate
python -m src.main --source yaml
```

Run with NetBox:

```bash
cd ~/netbox-docker
docker compose up -d

cd ~/neteng/Automated-Network-Validation-Framework
source venv/bin/activate
source .env
python -m src.main --source netbox
```

View reports:

```bash
cat reports/validation_report.txt
python -m json.tool reports/validation_report.json
```

Run tests:

```bash
pytest
```

