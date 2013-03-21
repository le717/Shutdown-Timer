"""
    Shutdown Timer -  Small Windows Shutdown Timer
    Copyright 2013 Triangle717 <http://triangle717.wordpress.com>
    Source code is available at <https://github.com/le717/Shutdown-Timer>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import sys, os, time, platform, webbrowser
from threading import Timer
import argparse

app = "Shutdown Timer"
majver = "0.3"
creator = "Triangle717"

# Expand recursion limit so program does not end prematurely.
sys.setrecursionlimit(9999999)

def cmdOpts():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cmd",
    help="Runs {0} in command-line mode, which enables loading the shutdown time from ShutdownTime.txt".format(app),
    action="store_true")
    args = parser.parse_args()
##    function(agrs.cmd)
    if args.cmd:
        os.system("title {0} {1} - Command Line Version".format(app, majver))
        MainMenu()
    else:
        os.system("title {0} {1}".format(app, majver))
        preload()


# ------------ Begin Shutdown Timer Initialization ------------ #

def preload():
    '''Python 3.3.0 & ShutdownTime.txt check'''

     # You need to have at least Python 3.3.0 to run this
    if sys.version_info < (3,3,0):
        sys.stdout.write("\nYou need to download Python 3.3.0 or greater to run {0} {1}.".format(app, majver))

        # Don't open browser immediately
        time.sleep(2)
        webbrowser.open_new_tab("http://python.org/download") # New tab, raise browser window (if possible)

        # Close app
        time.sleep(3)
        raise SystemExit

    # If you are running Python 3.3.0
    else:
        if platform.system() == 'Windows':
            main()
        else: # if platform.system() != 'Windows':
            print("\n{0} {1} is not supported on a non-Windows Operating System!".format(app, majver))
            print("\n{0} is shutting down.".format(app))
            time.sleep(2)
            raise SystemExit
##
##        if not os.path.exists("ShutdownTime.txt"):
##            logging.warning("Cannot find last used shutdown time (ShutdownTime.txt)!")
##            logging.info("Switching to FirstRunMenu()")
##            FirstRunMenu()
##
##        else:
##            logging.info("Last used shutdown time found (ShutdownTime.txt)")
##            logging.info("Switching to MainMenu()")
##            MainMenu()


def MainMenu():
    '''Shutdown Timer Command-line Menu layout'''

    print("\n{0} Version {1}, Copyright 2013 {2}".format(app, majver, creator))
    print('''\nLast used shutdown time has been restored.
    \nIf no new time is enter in 30 seconds, {0} will use the restored time
    \nnamely, "*time here*".
    \nPress "q" to close.'''.format(app))

    # So the program can loop
    global offtime

    offtime = input("\n\n> ")
##    offtime = "6:15"

##    t = Timer(2.0, Shutdown(offtime))
##    t = Timer(10.0, print("Using file"))
##    t.start()
##    print("Using file")
##    raise SystemExit


    if offtime.lower() == "q":
        print("\n{0} is shutting down.".format(app))
        time.sleep(2)
        raise SystemExit

    elif len(offtime) == 0:
        print("Invalid input!") # Temp message
        MainMenu()

    # User typed a valid time
    else:
##        t.cancel()
        Shutdown(offtime)


def main():
    '''Shutdown Timer Menu Layout'''

    print("\n{0} Version {1}, Copyright 2013 {2}".format(app, majver, creator))
    print('''\nPlease enter the time you want the computer to shutdown.
Use the 24-hour format with the following layout: "HH:MM".
\nPress "q" to exit.''')

    # So the program can loop
    global offtime

    offtime = input("\n\n> ")

    # Only 'q' will close the program
    if offtime.lower() == "q":
        print("\n{0} is shutting down.".format(app))
        time.sleep(2)
        raise SystemExit

    elif len(offtime) == 0:
        print("\nYou have entered an invalid time!")
        time.sleep(1.5)
        main()

    # User typed a vaild time
    else:
        Shutdown(offtime)

# To be used later. :)
##    time.sleep(50)
##    raise SystemExit
##sys.stdout.write("Shutdown started")
##time.sleep(offtime)
##sys.stdout.write("os.system('shutdown /r /t 0')")
##sys.stdout.write("Shutting down PC...")
##os.system("shutdown /r /t 0")


def Shutdown(offtime):
    '''Checks if it is time to shutdown, and does so when ready'''


    # The current time, as defined by the System Clock
    cur_time = time.strftime("%H:%M", time.localtime())
    print(cur_time)
    print(offtime)

    # Keeps the program running until it is time.
    while True:

        # The defined time equals the current (system) time
        if offtime == cur_time:
            # Let user read message
            time.sleep(1)
            # To be replaced with shutdown code
            raise SystemExit

        # The defined time does not equal the current (system) time.
        else:
            # Get the current seconds, as defined by the system clock.
            seconds = time.strftime("%S", time.localtime())
            print(seconds)

            '''The following code aligns the timer exactly with the system clock,
            allowing the computer to begin the shutdown routine exactly when stated.'''

            if seconds != 00:
                # Get how many seconds before it is aligned
                # Conver to int(eger) to subtract
                aligntime = 60 - int(seconds)
                print("Shutdown later 2") # And here...
                # Sleep for however long until alignment
                time.sleep(aligntime)
                # Loop back through the program
                Shutdown(offtime)

########
## TODO
########

# Write text file with time input when run from command-line
# Detect file upon startup from command-line
# Use file as time when run from command-line, enter time when run normally
# (Refer to http://stackoverflow.com/questions/2933399/how-to-set-time-limit-on-input
# And http://docs.python.org/3.3/library/threading.html?#timer-objects)
# Add file detection into preload()
# Check if input matches required format???
# Once timer is started, press 'q' to close, or Windows' exit button???
# Anything else I remember later on


# -- Resource links just for me. ;) -- #

#http://www.dreamincode.net/forums/topic/210175-shutting-down-a-computer-from-python/
#http://www.computerperformance.co.uk/windows7/windows7_shutdown_command.htm
#http://www.thewindowsclub.com/shutdown-restart-windows-8
## CMD Arguments
# http://docs.python.org/3.3/howto/argparse.html#id1
# http://beastie.cs.ua.edu/cs150/book/index_11.html

##fileName = sys.argv[0].split(os.sep).pop()

if __name__ == "__main__":
    cmdOpts()