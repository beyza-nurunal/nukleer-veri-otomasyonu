# EXFOR-to-TALYS Nuclear Data Preprocessing Pipeline

A Python-based automation pipeline developed for preprocessing experimental nuclear reaction data obtained from the IAEA EXFOR database and preparing structured inputs for TALYS simulations.

## Purpose

This project was developed to reduce manual preprocessing time in nuclear reaction analysis workflows and standardize TALYS input preparation for large experimental datasets. 

## Features

* Automatic reaction-folder detection
* Multi-file EXFOR dataset parsing
* Experimental uncertainty handling
* Automatic author/year extraction
* Structured Excel report generation
* TALYS `.inp` file generation
* Shared energy grid generation
* Multi-LDModel support
* Batch processing architecture

## Technologies Used

* Python (Pandas, OpenPyXL, Regular Expressions)
* TALYS Nuclear Reaction Code
* IAEA EXFOR Database

## Project Structure

EFOR_PROJE/
├── reaction_folder_1/
│   ├── dataset1.txt
│   ├── dataset2.dat
│   ├── input_ld1.inp
│   ├── input_ld2.inp
│   └── enerji
├── reaction_folder_2/
├── data_transformer.py
└── MASTER_EXFOR.xlsx

## Example Outputs
The repository includes:
Generated TALYS input files
Automatically produced Excel reports
Sample processed EXFOR datasets
Shared energy-grid files
## Excel Output Structure
The pipeline dynamically creates separate TALYS sections for each selected Level Density (LD) model. Each worksheet contains the following structured data:
Experimental Data	Shared Energy Grid	TALYS Calculations
Energy (MeV)	Common Energies	TALYS LD Models
Cross Section (mb)		
Uncertainty (mb)		
## Future Improvements
Automatic TALYS output parsing
Direct EXFOR API integration
Plot generation and visualization
Statistical model comparison
GUI support
Parallel processing optimization

Author
Beyzanur Ünal Physics Student
Nuclear Data Processing & TALYS Automation
