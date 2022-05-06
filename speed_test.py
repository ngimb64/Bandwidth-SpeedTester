# Built-in Modules #
import os
import shlex
import time

# Third-party modules #
from speedtest import Speedtest


# Pseudo-Constant #
MAX_HOURS = 24


'''
########################################################################################################################
Name:       PrintResultDict
Purpose:    Displays the speed test results from passed in dictionary.
Parameters: Dictionary of speed test results to be displayed.
Returns     Nothing
########################################################################################################################
'''
def PrintResultDict(result: dict):
    # Print the results #
    print(f'Ping: {result["ping"]}')
    print(f'Download: {result["download"] / 8_000_000}')
    print(f'Upload: {result["upload"] / 8_000_000}\n')

    # Iterate through server dict and print data #
    [print(f'{key}: {value}') for key, value in result["server"].items()]
    print('')


'''
########################################################################################################################
Name:       IntervalSleepCounter
Purpose:    Displays sleep counter based on user specified intervals.
Parameters: Time interval to sleep.
Returns     Nothing
########################################################################################################################
'''
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


'''
########################################################################################################################
Name:       RunTest
Purpose:    Executes test and prints results.
Parameters: The list of connection testing servers and job threads.
Returns:    A dictionary containing speed test results.
########################################################################################################################
'''
def RunTest(servers: list, threads: None) -> dict:
    # Initialize test object #
    test = Speedtest()
    # Get list of available servers #
    test.get_servers(servers)
    # Get the best available server #
    best = test.get_best_server()

    print(f'\nRunning test on server => {best}\n')

    # Test download #
    test.download(threads=threads)
    # Test upload #
    test.upload(pre_allocate=False, threads=threads)
    # Parse test results as dict #
    results = test.results.dict()

    return results


'''
########################################################################################################################
Name:       UserInput
Purpose:    Prompts user for the number of test intervals in an hour and how many hours to test.
Parameters: Nothing
Returns:    Validated user input of number of intervals and hours.
########################################################################################################################
'''
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
                print('\n* Improper input .. enter a number in between 2 and 12 *\n')
                continue

            # If hours is less than 0 or hours is greater than max constant #
            if hours < 0 or hours > MAX_HOURS:
                # Print error, provide suggestion and re-iterate loop #
                print(f'\n* Improper input .. avoid numbers below 0 or above {MAX_HOURS} *\n')
                continue

            # If the user wants a single test #
            if hours == 0:
                hours = None

        except ValueError:
            # Print error, provide suggestion and re-iterate loop #
            print('\n* Improper input .. enter a number not other data type *\n')
            continue

        return intervals, hours


'''
########################################################################################################################
Name:       main
Purpose:    Prompts user, calculates intervals, executes bandwidth tests in a singular or time series fashion.
Parameters: Nothing
Returns:    Nothing
########################################################################################################################
'''
def main():
    servers = []
    threads= None
    cmds = ('cls', 'clear')

    # If the OS is Windows #
    if os.name == 'nt':
        clear_cmd = shlex.quote(cmds[0])
    # If the OS is Linux #
    else:
        clear_cmd = shlex.quote(cmds[1])

    # Get the users input #
    intervals, hours = UserInput()

    # Calculate number of seconds per interval #
    interval_time = (60 / intervals) * 60

    # Assign interval counter #
    count = intervals

    # If multiple test selected #
    if hours:
        # Iterate per hour #
        for h in range(hours):
            # Decremental counter loop #
            while count != 0:
                # Check internet speed through speedtest api #
                res = RunTest(servers, threads)
                # Reset server list #
                servers = []

                # If last test has completed #
                if count == 1:
                    break

                # Sleep program interval time
                # until the next test #
                IntervalSleepCounter(res, interval_time, clear_cmd)

                count -= 1

            # Reset interval counter #
            count = intervals
    else:
        # Check internet speed through speedtest api #
        res = RunTest(servers, threads)
        # Display speed test results #
        PrintResultDict(res)


if __name__ == '__main__':
    main()
