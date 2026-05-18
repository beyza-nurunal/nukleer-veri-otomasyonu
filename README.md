Nuclear Data Parsing and Automation System (TALYS and IAEA-EXFOR)
This repository contains Python-based data processing scripts developed to automatically filter, format, and prepare raw excitation function data sets obtained from the IAEA (EXFOR) nuclear database for the TALYS nuclear reaction simulation code.
Features and Solved Problems
•⁠  ⁠Automatically selects and extracts the 1st, 2nd, and 4th columns (Energy, dEne, and dSig) from the raw data while filtering out the unwanted 3rd column.
•⁠  ⁠Instantly isolates critical nuclear analysis parameters and formats them in clean columns.
•⁠  ⁠Performs dot/comma format synchronization automatically via n.py and v.py scripts to match different software environment requirements.
•⁠  ⁠Automatically injects necessary TALYS input headers (element name, mass number, and projectile type) at the top of the output files.
Script Details
•⁠  ⁠n.py: Automated parsing tool that extracts columns 1, 2, and 4, and converts decimals to dot (.) format for direct TALYS inputs.
•⁠  ⁠v.py: Automated parsing tool that extracts columns 1, 2, and 4, and converts decimals to comma (,) format for local data analysis or Excel synchronization.
How to Run
You can execute these scripts via Mac Terminal using the following short commands:
•⁠  ⁠To generate dot-separated TALYS input: python3 n.py
•⁠  ⁠To generate comma-separated data output: python3 v.py
### Sample Dataset & Outputs
•⁠  ⁠ham_veri.txt: A sample raw data file extracted from the IAEA-EXFOR database, featuring multiple unstructured columns used to test and verify the automation scripts.
•⁠  ⁠n_cikti.txt: The standardized TALYS input file generated automatically by n.py, containing the correct headers and cleanly parsed 1st, 2nd, and 4th columns with dot (.) formatting.
