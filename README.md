# Python Project – Data Extraction, Processing, and Visualization
## Overview

This project was developed using object-oriented programming (OOP) in Python 13.3.5, with Microsoft Visual Studio as the professional integrated development environment (IDE).

The application is designed to:

Read CSV-type documents from provided addresses (or allow the user to select them via a pop-up window if no addresses are given). 
Convert them into pandas DataFrames with column names automatically extracted from the files.
Insert the datasets into three different tables in a database management system (DBMS).
Process the datasets to select four ideal functions and map the test cases into those functions when conditions are satisfied.
Present the final results as interactive plots with legends for clarification.

## Requirements

The project requires a Python virtual environment with the following external modules installed.

Name	Version	Description 

Bokeh	3.7.3	Library to create interactive visualizations for modern web browsers.

NumPy	2.3.1	Fast and flexible calculations with matrices, vectors, and multi-dimensional arrays.

Pandas	2.3.1	Data analysis and manipulation tool built on Python.

Tkinter	8.6	Standard interface to the Tcl/Tk GUI in Python.

SQLAlchemy	2.0.41	SQL toolkit and object-relational mapping (ORM) for Python.

SQLAlchemy-Utils	0.41.2	Utility functions, helpers, and new data types for SQLAlchemy.

## Installation

### Clone this repository:
git clone https://github.com/jecaball/01.-Python-Project.git
cd 01.-Python-Project

### Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

### Install required dependencies:
pip install bokeh==3.7.3 numpy==2.3.1 pandas==2.3.1 tk sqlalchemy==2.0.41 sqlalchemy-utils==0.41.2

## Usage

Run the application from your IDE or terminal inside the activated virtual environment.

Provide the file addresses for the CSV datasets.

If no addresses are provided, a Tkinter pop-up window will allow you to select the files manually.

The application will:

Insert the datasets into three DBMS tables.

Process the data and map test cases to ideal functions.

Display results as interactive Bokeh plots.
