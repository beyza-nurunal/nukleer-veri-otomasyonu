# EXFOR-to-TALYS Nuclear Data Preprocessing Pipeline

This project is a Python-based data preprocessing pipeline designed to parse, clean, and structure raw nuclear excitation function datasets obtained from the IAEA EXFOR database. The processed outputs are formatted for further use in statistical analysis and TALYS nuclear reaction simulations.

⸻

# Features

•⁠  ⁠Automated Directory Processing
    The script automatically detects reaction folders in the working directory and processes all valid datasets without hardcoded paths.
•⁠  ⁠Robust Data Parsing using Pandas
    Raw EXFOR data is handled using column-based indexing to reduce errors caused by inconsistent spacing or formatting in input files.
• ⁠Isolated Output Structure
    Each reaction directory contains an automatically generated outputs/ folder to store processed files without modifying raw data.
 # ⁠Dual Output Generation
    The pipeline generates two types of outputs:
     Excel Output: Cleaned dataset in .xlsx format for analysis (Energy, Cross Section, Error)
     TALYS-Compatible Text Output: Extracted columns formatted for simulation workflows and verification purposes
    nukleer-veri-otomasyonu/
│
├── data_transformer.py        # Ana veri işleme scripti
├── README.md
│
└── [reaksiyon_klasörü]/
    ├── veri1.txt              # Ham EXFOR giriş verisi
    │
    └── outputs/
        ├── veri1_excel.xlsx   # İşlenmiş analitik veri seti
        └── veri1_talys.txt    # TALYS uyumlu formatlanmış çıktı
