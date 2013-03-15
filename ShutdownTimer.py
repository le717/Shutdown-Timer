# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Shutdown Timer
# https://github.com/le717/Shutdown-Timer
# Copyright 2013 Triangle717 (http://triangle717.wordpress.com).

# logging.BasicConfig() code based on example from A Byte of Python
# http://www.swaroopch.com/notes/Python


import sys, os, time, logging

app = "Shutdown Timer"
majver = "0.3"
creator = "Triangle717"

# Expand recursion limit so program does not end prematurely.
sys.setrecursionlimit(9999999)

# ------------ Begin Shutdown Timer Initialization ------------ #

def preload():
    '''Python 3.3.0 check'''

    logging.info("Begin logging to {0}".format(logging_file))
    logging.info('''
                                #############################################
                                            {0} {1}
                                        Copyright 2013 {2}
                                                Debug.log


                                    If you run into a bug, open an issue at
                                https://github.com/le717/Shutdown-Timer/issues
                                    and attach this file for an easier fix!
                                #############################################
                                '''.format(app, majver, creator))

     # You need to have at least Python 3.3.0 to run this
    if sys.version_info < (3,3,0):
        logging.warning("You are not running Python 3.3.0 or higher!\nYou need to get a newer version to run {0}".format(app))
        sys.stdout.write("\nYou need to download Python 3.3.0 or greater to run {0} {1}.".format(app, majver))

        # Don't open browser immediately
        time.sleep(2)
        logging.info("Open new tab in web browser to http://python.org/download")
        open_new_tab("http://python.org/download") # New tab, raise browser window (if possible)

        # Close app
        logging.info("Display error message for three seconds")
        time.sleep(3)
        logging.info("{0} is shutting down.".format(app))
        raise SystemExit

    # If you are running Python 3.3.0
    else:
        logging.info("You are running Python 3.3.0 or greater. {0} will continue.".format(app))
# Add file detection code here
        main()


def main():
    '''Main Menu'''
    print("\n{0} Version {1}, Copyright 2013 {2}".format(app, majver, creator))
    print("\nPlease enter the time you want the computer to shutdown.")
    print('\nUse the 24-hour format with the following layout: "HH:MM".')
    print('\nPress "q" to close.')

    # So the program can loop
    global offtime

    offtime = input("\n\n> ")

    # Only 'q' will close the program
    if offtime.lower() == "q":
        print("\n{0} is shutting down.".format(app))
        time.sleep(2)
        raise SystemExit

    elif len(offtime) == 0:
        print("Invalid input!") # Temp message
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
            print("Shutdown now!") # Temp here too
            # Display message
            time.sleep(1)
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

def TheLog():
    '''Logging Settings'''

    try:

    # -- Begin Logging Config -- #

        logging.basicConfig(
            level = logging.DEBUG,
            format = "%(asctime)s : %(levelname)s : %(message)s",
            filename = logging_file,
            filemode = 'a+',
        )

    # -- End Logging Config -- #

    # Does not have the rights to set the Logging Config!
    except PermissionError:
        print("\{0} does not have the user rights to operate!\nPlease relaunch {0} as an Administrator.".format(app, app))
        # Display message long enough so user can read it
        time.sleep(5)
        # Close program
        raise SystemExit


########
## TODO
########

# Write text file with time input
# Detect file upon startup
# If file detected: If no input in 30 seconds after startup, use time in file
# If file not detected: ask for input, proceed when given
# Add file detection into preload()
# Check if input matches required format???
# Once timer is started, press 'q' to close, or Windows' exit button???
# Anything else I remember later on


# -- Resource links just for me. ;) -- #

#http://www.dreamincode.net/forums/topic/210175-shutting-down-a-computer-from-python/
#http://www.computerperformance.co.uk/windows7/windows7_shutdown_command.htm
#http://www.thewindowsclub.com/shutdown-restart-windows-8

if __name__ == "__main__":
    logging_file = os.path.join(os.getcwd(), 'Debug.log')
    TheLog()
    preload()