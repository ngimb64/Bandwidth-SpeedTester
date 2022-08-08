# Bandwidth-SpeedTester
![alt text](https://github.com/ngimb64/Bandwidth-Speedtester/blob/main/BandwidthSpeedTester.gif?raw=true)
![alt text](https://github.com/ngimb64/Bandwidth-Speedtester/blob/main/TestGraph.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.82/10

## Prereqs
 This program runs on Windows and Linux, written in Python 3.9

## Purpose
 Test connection bandwidth as a singular test or an interval-based time series through the Speed Test API.
 When multiple tests are selected, each test interval is saved to the test_data.csv file.
 Upon completion of all tests, the csv data is loaded and used to create a graph time series report.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example: `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the `./activate` script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How to use
- Open up Command Prompt (CMD) or terminal
- Enter the directory containing the program and execute in shell

## Function Layout
> graph_test_data &nbsp;-&nbsp; Loads the test data from csv, then graphs the test data as time 
> series.

> error_query &nbsp;-&nbsp; Looks up the passed in error, prints, and logs it.

> print_result_dict &nbsp;-&nbsp; Displays the speed test results from passed in dictionary.

> interval_sleep_counter &nbsp;-&nbsp; Displays sleep counter based on user specified intervals.

> run_test &nbsp;-&nbsp; Executes speed test, prints the results, and saves them to report file 
> based on execution time.

> print_err &nbsp;-&nbsp; Displays error message via standard output.

> user_input &nbsp;-&nbsp; Prompts user for the number of test intervals in an hour and how many
> hours to test.

> main &nbsp;-&nbsp; Prompts user, calculates intervals, executes bandwidth tests in a singular or
> time series fashion.

## Exit Codes
> 0 - Operation successful<br>
> 1 - Unexpected exception occurred<br>
> 2 - Attempted file operation on file that does not exist<br>
> 3 - Attempted file operation on file that does not have proper permissions<br>
> 4 - IO error occurred during attempted file operation<br>
> 5 - Unexpected file operation occurred