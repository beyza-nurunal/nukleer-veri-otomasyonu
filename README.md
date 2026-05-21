# EXFOR-to-TALYS Nuclear Data Preprocessing Pipeline

This project is a Python-based data preprocessing pipeline designed to parse, clean, and structure raw nuclear excitation function data from the IAEA EXFOR database and converts it into structured formats for analysis and TALYS nuclear reaction calculations.

The repository includes real processed outputs and a working TALYS-compatible input example generated from actual datasets.

---

## Features

* **Automated Directory Processing**
  The script automatically detects reaction folders in the working directory and processes all valid datasets without hardcoded paths.
* **EXFOR Data Parsing and Cleaning**
  Raw experimental data is parsed using Pandas-based column handling to ensure robustness against inconsistent formatting and spacing in EXFOR files.
* **Non-destructive Processing Workflow**
  Input data is never modified. All generated outputs are saved in a separate outputs/ directory inside each reaction folder.
* **TALYS-Compatible Output Generation**
  The pipeline extracts and formats Energy and Error values (Columns 1 and 3) into a structured text format suitable for simulation and error analysis workflows.
* **Analytical Output Generation**
  A structured Excel file (.xlsx) is generated for further analysis and validation.

nukleer-veri-otomasyonu/
│
├── data_transformer.py        # Main preprocessing script
├── README.md
│
├── talys_input_example.inp    # Example TALYS input file (real use case)
├── example_output.xlsx        # Example processed dataset (from real data)
│
└── [reaction_directory]/
    ├── veri1.txt              # Raw EXFOR input data
    │
    └── outputs/
        ├── veri1_excel.xlsx   # Processed dataset (Energy, Cross Section, Error)
        └── veri1_talys.txt    # TALYS-compatible formatted output
        
## Requirements
Python 3.8+
pandas
openpyxl
Install dependencies:

pip install pandas openpyxl

## Usage
Run the pipeline from the project root directory:

python3 data_transformer.py
The script will:
Scan all reaction directories
Parse raw EXFOR datasets
Generate processed outputs inside each outputs/ folder
Generated Outputs
Excel file: Structured dataset for analysis
TALYS file: Simulation-ready formatted numeric columns
Included Real Outputs
This repository also contains:
A working TALYS input file generated from processed data
A real Excel output file created from EXFOR datasets
Example outputs demonstrating end-to-end pipeline execution
