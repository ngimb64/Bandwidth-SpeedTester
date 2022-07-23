# Bandwidth-SpeedTester
![alt text](https://github.com/ngimb64/Bandwidth-Speedtester/blob/main/BandwidthSpeedTester.gif?raw=true)
<br>
![alt text](https://github.com/ngimb64/Bandwidth-Speedtester/blob/main/TestGraph.png?raw=true)

## Prereqs
> This program runs on Windows and Linux, written in Python 3.9

## Purpose
> Test connection bandwidth as a singular test or an interval-based time series through the Speed Test API.
> When multiple tests are selected, each test interval is saved to the test_data.csv file.
> Upon completion of all tests, the csv data is loaded and used to create a graph time series report.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example:<br>
> python3 setup.py "venv name"

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the "activate" script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How to use
- Open up Command Prompt (CMD) or terminal
- Enter the directory containing the program and execute in shell
