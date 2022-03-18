# Built-in Modules #
from time import sleep

# Third-party modules #
from speedtest import Speedtest

# Pseudo-Constant #
MAX_HOURS = 24

'''
########################################################################################################################
Name:       RunTest
Purpose:    Executes test and prints results.
Parameters: The list of connection testing servers and job threads.
Returns:    None
########################################################################################################################
'''
def RunTest(servers, threads):
    # Initialize test object #
    test = Speedtest()
    # Get list of available servers #
    test.get_servers(servers)
    # Get the best available server #
    test.get_best_server()
    # Test download #
    test.download(threads=threads)
    # Test upload #
    test.upload(pre_allocate=False, threads=threads)
    # Parse test results as dict #
    results = test.results.dict()

    # Print the results #
    print(f'Download: {results["download"] / 8000000}')
    print(f'Upload: {results["upload"] / 8000000}')
    print(f'Ping: {results["ping"]}')

    # Iterate through server dict and print data #
    [print(f'{key}: {value}') for key, value in results["server"].items()]


'''
########################################################################################################################
Name:       UserInput
Purpose:    Prompts user for the number of test intervals in an hour and how many hours to test.
Parameters: None
Returns:    Validated user input.
########################################################################################################################
'''
def UserInput():
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
Parameters: None
Returns:    None
########################################################################################################################
'''
def main():
    servers = []
    threads = None

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
                RunTest(servers, threads)
                # Reset server list #
                servers = []

                # If last test has completed #
                if count == 1:
                    break

                # Sleep program interval time
                # until the next test #
                sleep(interval_time)

                count -= 1

            # Reset interval counter #
            count = intervals
    else:
        # Check internet speed through speedtest api #
        RunTest(servers, threads)


if __name__ == '__main__':
    main()
