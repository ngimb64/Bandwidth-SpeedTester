# Built-in Modules #
import csv
import errno
import json
import logging
import os
import sys
import time
from datetime import date, datetime

# Third-party modules #
import matplotlib.pyplot as plt
from speedtest import Speedtest

# Get the current working directory #
cwd = os.getcwd()

# Pseudo-Constant #
if os.name == 'nt':
    OUTPUT_DIR = f'{cwd}\\TestResults\\'
else:
    OUTPUT_DIR = f'{cwd}/TestResults/'

MAX_HOURS = 24


"""
################
Function Index #
########################################################################################################################
GraphTestData - Loads the test data from csv, then graphs the test data as time series.
ErrorQuery - Looks up the passed in error, prints, and logs it.
PrintResultDict - Displays the speed test results from passed in dictionary.
IntervalSleepCounter - Displays sleep counter based on user specified intervals.
RunTest - Executes speed test, prints the results, and saves them to report file based on execution time.
PrintErr - Displays error message through standard output.
UserInput - Prompts user for the number of test intervals in an hour and how many hours to test.
main - Prompts user, calculates intervals, executes bandwidth tests in a singular or time series fashion.
########################################################################################################################
"""


"""
########################################################################################################################
Name:       GraphTestData
Purpose:    Loads the test data from csv, then graphs the test data as time series.
Parameters: Nothing
Returns     Nothing
########################################################################################################################
"""
def GraphTestData():
    file_name = 'test_data.csv'
    headers = ['server_name', 'download', 'upload', 'ping', 'month', 'day', 'hour', 'minute']
    server_name, download, upload, ping, exec_time = [], [], [], [], []
    try:
        # Open the csv data file in read mode #
        with open(file_name, 'r', encoding='UTF8', newline='') as data_file:
            # Read the csv data file as dict #
            reader = csv.DictReader(data_file, fieldnames=headers)

            # Iterate through rows in csv in dict format #
            for row in reader:
                # Populate data rows to corresponding lists #
                server_name.append(row['server_name'])
                download.append(float(row['download']))
                upload.append(float(row['upload']))
                ping.append(float(row['ping']))
                exec_time.append(f'{row["month"]}-{row["day"]}_{row["hour"]}-{row["minute"]}')

    # If IO error occurs #
    except IOError as io_err:
        ErrorQuery(file_name, 'r', io_err)

    x = []
    labels = []
    count = 1

    # Iterate through execution times and corresponding server names and
    # append them to label list as one with corresponding x-axis indexes #
    for test_time, test_name in zip(exec_time, server_name):
        x.append(count)
        labels.append(f'{test_time}_{test_name}')
        count += 1

    # Set the graph title and x and y-axis #
    plt.title('Bandwidth Time-Series')
    plt.xlabel(f'{"*" * 10}\nTest Times')
    plt.ylabel(f'Test Results\n{"*" * 12}')

    # Set the xtick labels for x-axis #
    plt.xticks(x, labels, rotation=90)
    # Plot download, upload, and ping #
    plt.plot(x, download, '.-', label='Download Speed')
    plt.plot(x, upload, '.-', label='Upload Speed')
    plt.plot(x, ping, '.-', label='Ping')

    # Add legend to graph #
    plt.legend()
    # Display the graph #
    plt.show()


"""
########################################################################################################################
Name:       ErrorQuery
Purpose:    Looks up the passed in error, prints, and logs it.
Parameters: The name of the report file, the file mode, and the error object containing the message & errno.
Returns     Nothing
########################################################################################################################
"""
def ErrorQuery(report_name: str, file_mode: str, err_obj: object):
    # If file does not exist #
    if err_obj.errno == errno.ENOENT:
        PrintErr(f'{report_name} does not exist')
        logging.exception(f'{report_name} does not exist\n\n')
        sys.exit(2)

    # If the file does not have read/write access #
    elif err_obj.errno == errno.EPERM:
        PrintErr(f'{report_name} does not have proper permissions for {file_mode} mode,'
                 ' if file exists confirm it is closed')
        logging.exception(f'{report_name} does not have permissions for {file_mode}\n\n')
        sys.exit(3)

    # File IO error occurred #
    elif err_obj.errno == errno.EIO:
        PrintErr(f'IO error occurred during {file_mode} mode on {report_name}')
        logging.exception(f'IO error occurred during append mode on {report_name}\n\n')
        sys.exit(4)

    # If other unexpected file operation occurs #
    else:
        PrintErr(f'Unexpected file operation occurred accessing {report_name}: {err_obj.errno}')
        logging.exception(f'Unexpected file operation occurred accessing {report_name}: {err_obj.errno}\n\n')
        sys.exit(5)


"""
########################################################################################################################
Name:       PrintResultDict
Purpose:    Displays the speed test results from passed in dictionary.
Parameters: Dictionary of speed test results to be displayed.
Returns     Nothing
########################################################################################################################
"""
def PrintResultDict(result: dict):
    # Print the results #
    print('Ping {:.2f}'.format(result['ping']))
    print('Download: {:.2f} MB'.format(result['download'] / (1024 * 1024)))
    print('Upload: {:.2f} MB\n'.format(result['upload'] / (1024 * 1024)))

    # Iterate through server dict and print data #
    for key, value in result["server"].items():
        # If the value is float #
        if isinstance(value, float):
            print('{:10s}{:10f}'.format(key, value))
        else:
            print('{:10s}{:10s}'.format(key, value))

    print('')


"""
########################################################################################################################
Name:       IntervalSleepCounter
Purpose:    Displays sleep counter based on user specified intervals.
Parameters: Time interval to sleep.
Returns     Nothing
########################################################################################################################
"""
def IntervalSleepCounter(result_dict: dict, time_interval: int, clear_display):
    counter = time_interval

    # Iterate through time interval range printing and sleeping each second #
    for second in range(1, int(time_interval) + 2):
        # Clear the screen #
        os.system(clear_display)
        # Print the speed test results #
        PrintResultDict(result_dict)
        print(f'Time until next test: {counter}')
        print(f'{second * "!"}')
        time.sleep(1)
        counter -= 1

    os.system(clear_display)


"""
########################################################################################################################
Name:       RunTest
Purpose:    Executes speed test, prints the results, and saves them to report file based on execution time.
Parameters: The list of connection testing servers, job threads, and multi_test boolean toggle default at False.
Returns:    A dictionary containing speed test results.
########################################################################################################################
"""
def RunTest(servers: list, threads: None, multi_test=False) -> dict:
    # Initialize test object #
    test = Speedtest()
    # Get list of available servers #
    test.get_servers(servers)
    # Get the best available server #
    best = test.get_best_server()

    print(f'\nRunning test on server\n{22 * "*"}')
    # Print the best available server #
    for key, value in best.items():
        # If the value is float #
        if isinstance(value, float):
            print('{:10s}{:10f}'.format(key, value))
        else:
            print('{:10s}{:10s}'.format(key, value))

    # Test download #
    test.download(threads=threads)
    # Test upload #
    test.upload(pre_allocate=False, threads=threads)
    # Parse test results as dict #
    results = test.results.dict()

    # Get the current time #
    curr_time = datetime.now()
    # Format report name with date and time #
    report_name = f'{OUTPUT_DIR}SpeedtestReport_{date.today()}_{curr_time.hour}-{curr_time.minute}.txt'
    csv_name = 'test_data.csv'

    try:
        # Open report file in write mode #
        with open(report_name, 'w') as out_file:
            # Write the name of the current file to report file #
            out_file.write(f'{report_name}\n{(1 + len(report_name)) * "*"}\n')
            # Write json results to output report file #
            json.dump(results, out_file, sort_keys=False, indent=4)

        # If multiple tests are being executed over time series #
        if multi_test:
            # Open the csv data file in append mode #
            with open(csv_name, 'a', encoding='UTF8', newline='') as data_file:
                # Initialize csv writer object #
                writer = csv.writer(data_file)

                # Format test results as list to be saved to csv #
                data = [results['server']['name'], '{:.2f}'.format(results['download'] / (1024 * 1024)),
                        '{:.2f}'.format(results['upload'] / (1024 * 1024)), '{:.2f}'.format(results['ping']),
                        curr_time.month, curr_time.day, curr_time.hour, curr_time.minute]
                # Write the test result data to csv #
                writer.writerow(data)

    # If IO error occurs #
    except (IOError, OSError) as io_err:
        # Look up error, print and log #
        ErrorQuery(report_name, 'a', io_err)

    return results


"""
########################################################################################################################
Name:       PrintErr
Purpose:    Displays error message through standard output.
Parameters: The error message to be displayed.
Returns:    Nothing
########################################################################################################################
"""
def PrintErr(msg: str):
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


"""
########################################################################################################################
Name:       UserInput
Purpose:    Prompts user for the number of test intervals in an hour and how many hours to test.
Parameters: Nothing
Returns:    Validated user input of number of intervals and hours.
########################################################################################################################
"""
def UserInput() -> tuple:
    # Iterate until results are returned #
    while True:
        try:
            # Prompt user for input #
            intervals = int(input('Enter the how many times speed should be checked in an hour'
                                  '(EVEN number up to 12 times allowed or every 5 minutes): '))
            hours = int(input('Enter the number of hours the bandwidth testing spans '
                              f'(0 for single test, Max = {MAX_HOURS}): '))

            # If the number is not even or intervals are less than 2 or greater than 12 #
            if intervals % 2 != 0 or intervals < 2 or intervals > 12:
                # Print error, provide suggestion and re-iterate loop #
                PrintErr('Improper input .. enter a number in between 2 and 12')
                continue

            # If hours is less than 0 or hours is greater than max constant #
            if hours < 0 or hours > MAX_HOURS:
                # Print error, provide suggestion and re-iterate loop #
                PrintErr(f'Improper input .. avoid numbers below 0 or above {MAX_HOURS}')
                continue

            # If the user wants a single test #
            if hours == 0:
                hours = None

        # If a data type other than int was entered #
        except ValueError:
            # Print error, provide suggestion and re-iterate loop #
            PrintErr('Improper input .. enter a number not other data type')
            continue

        return intervals, hours


"""
########################################################################################################################
Name:       main
Purpose:    Prompts user, calculates intervals, executes bandwidth tests in a singular or time series fashion.
Parameters: Nothing
Returns:    Nothing
########################################################################################################################
"""
def main():
    cmds = ('cls', 'clear')
    servers = []
    threads = None

    # If the directory to store test results does not exist #
    if not os.path.isdir(OUTPUT_DIR):
        # Create test results' dir #
        os.mkdir(OUTPUT_DIR)

    # Get the users input #
    intervals, hours = UserInput()
    # Calculate number of seconds per interval #
    interval_time = (60 / intervals) * 60
    # Assign interval counter #
    count = intervals

    # If the OS is Windows #
    if os.name == 'nt':
        cmd = cmds[0]
    # If the OS is Linux #
    else:
        cmd = cmds[1]

    # If multiple test selected #
    if hours:
        # Iterate per hour #
        for h in range(hours):
            # Decremental counter loop #
            while count != 0:
                # Check internet speed through speedtest api #
                res = RunTest(servers, threads, multi_test=True)
                # Reset server list #
                servers = []

                # If last test has completed #
                if count == 1:
                    PrintResultDict(res)
                    break

                # Sleep program interval time, until the next test #
                IntervalSleepCounter(res, interval_time, cmd)

                count -= 1

            # Reset interval counter #
            count = intervals

        # Load the test data and graph it #
        GraphTestData()

    else:
        # Check internet speed through speedtest api #
        res = RunTest(servers, threads)
        # Display speed test results #
        PrintResultDict(res)


if __name__ == '__main__':
    # Set the log file name #
    logging.basicConfig(level=logging.DEBUG, filename=f'BandwidthTesterLog.log')

    try:
        main()

    # If Ctrl + C is detected #
    except KeyboardInterrupt:
        print('\nCtrl+C detected, exiting program')

    # If unknown exception occurs #
    except Exception as err:
        PrintErr(f'Unknown exception occurred: {err}')
        logging.exception(f'Unknown exception occurred: {err}\n\n')
        sys.exit(1)

    sys.exit(0)
