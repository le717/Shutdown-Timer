#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shutdown Timer -  Small Windows shutdown timer.

Created 2013, 2015 Triangle717
<http://Triangle717.WordPress.com>

Shutdown Timer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Shutdown Timer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Shutdown Timer. If not, see <http://www.gnu.org/licenses/>.

"""


# import re
import os
import sys
# import json
import time
import argparse
import platform
from threading import Timer

import constants as const


class ShutdownTimer:

    def __init__(self, time):

        self.time = time
        self.__auto = False
        self.__force = False
        self.__restart = False
        self.__isWindows = "Windows" in platform.platform()
        self.__configData = None
        self.__configPath = self._getConfigPath()
        self.__jsonFile = os.path.join(self.__configPath, "Shutdown-Timer.json")
        self._loadConfig()
        self.__verbs = _setVerb()

    def _getConfigPath(self):
        """Get the file path where configuration files will be stored.

        On Windows, the root folder is %AppData%, while on Mac OS X and Linux
        it is ~. On all platforms, the rest of the path is Triangle717/*AppName*.

        @returns {String} The configuration path.
        """
        root = os.path.expanduser("~")
        if self.__isWindows:
            root = os.path.expandvars("%AppData%")

        # Create the path if needed
        path = os.path.join(root, "Triangle717", "Shutdown-Timer")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _loadConfig(self):
        """Read and store the configuration file.

        @returns {Boolean} True if the config file was read, False otherwise.
        """
        try:
            # Make sure it exists
            if os.path.exists(self.__jsonFile):
                with open(self.__jsonFile, "rt", encoding="utf-8") as f:
                    self.__configData = json.load(f)
                    return True
                return False

        # The file is not valid JSON, sliently fail
        except ValueError:
            return False

    def _saveConfig(self):
        """Write the JSON-based config file.

        @returns {Boolean} True if the config file was written, False otherwise.
        """
        try:
            jsonData = {
                "time": self.time,
                "auto": self.__auto,
                "force": self.__force,
                "restart": self.__restart
            }
            with open(self.__jsonFile, "wt", encoding="utf_8") as f:
                f.write(json.dumps(jsonData, indent=4, sort_keys=True))
            return True

        # Silently fail
        except PermissionError:
            return False

    def _setVerb(self):
        """Set the action verbs for use in messages depending on restart status.

        @return {Tuple} Two index tuple containing the action verbs.
        Second index is the "ing" form of the verb.
        """
        if self.__restart:
            return ("restart", "restarting")
        return ("shutdown", "shutting down")


def CMDParse():
    """Parses Command-line Arguments"""
    parser = argparse.ArgumentParser(
        description="{0} {1} Command-line arguments".format(const.appName, const.version))

    # Automatic  mode argument
    parser.add_argument("-a", "--auto",
    help="Runs {0} in automatic mode, using the time written in TheTime.txt"
    .format(const.appName),
    action="store_true")

    # Force shutdown argument
    parser.add_argument("-f", "--force",
    help='Sends "Force" command to Windows',
    action="store_true")

    # Restart Computer argument
    parser.add_argument("-r", "--restart",
    help='Restart Windows instead of shutting it down',
    action="store_true")

    # Register all the parameters
    args = parser.parse_args()

    # Declare all parameters as global for use in other locations
    global force, auto, restart
    force = args.force
    auto = args.auto
    restart = args.restart


def preload():
    """Run the correct mode, depending on parameters passed"""

    # The program was not run with the -a (or --auto) argument
    if not auto:
        main()

    # It was run with the automatic argument
    else:

        has_file = timer_File()
        # The CMD time files does not exist
        if not has_file:
            # Go to main(), where it will be written
            main()

        # The Auto time file(s) does exist
        elif has_file:
            # Go to AutoMain(), where it will be used
            AutoMain()


def timer_File():
    """Check for the existance and the usage of new or old time file"""

    global the_file
    # Both files exist, new file has priority
    if os.path.exists("ShutdownTime.txt") and os.path.exists("TheTime.txt"):
        the_file = "TheTime.txt"
        return True

    # Only the old file exists
    elif (
        os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt")
        ):
        the_file = "ShutdownTime.txt"
        return True

    # Neither of the files exist
    elif not (
        os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt")
    ):
        return False

    # Anything else (not really needed, but here for safety)
    else:
        the_file = "TheTime.txt"
        return True


def close_Type():
    """Change app messages depending if we are shutting down or restarting"""

    global the_word, the_word_ing
    if restart:
        the_word = "restart"
        the_word_ing = "restarting"
    elif not restart:
        the_word = "shutdown"
        the_word_ing = "shutting down"


def AutoMain():
    """Shutdown Timer Automatic Mode Menu"""

    # Write window title for automatic mode
    os.system("title {0} {1} - Automatic Mode".format(const.appName, const.version))

    print("\n{0} Version {1} - Automatic Mode".format(const.appName, const.version))
    print('''Created 2013 {0}

{1} has been detected.
Your computer will {2} at the time written in the file.
\nThe Timer will begin in 10 seconds.
Pressing 'q' right now will cancel the {2}.'''.format(
    const.creator, the_file, the_word))

    # Start 10 second countdown timer
    # After 10 seconds, run readFile() to get the shutdown time
    t = Timer(10.0, getTime)
    t.start()
    menuopt = input("\n\n> ")

    # User wanted to close the timer
    if menuopt.lower() == "q":
        t.cancel()
        raise SystemExit(0)


def main():
    """Shutdown Timer Menu Layout"""

    # Write window title for non-automatic mode
    os.system("title {0} {1}".format(const.appName, const.version,
const.creator))
    print('''\nPlease enter the time you want the computer to {0}.
Use the 24-hour format with the following layout: "HH:MM".
\nPress "q" to exit.'''.format(the_word))

    off_time = input("\n\n> ")

    # Only 'q' will close the program
    if off_time.lower() == "q":
        raise SystemExit(0)

    elif len(off_time) == 0:
        print("\nYou have entered an invalid time!")
        time.sleep(1.5)
        main()

    # User typed a vaild time
    else:
        # Write time to be used by Automatic mode
        # TheTime.txt is the only file written from now on
        with open("TheTime.txt", 'wt', encoding="utf-8") as f:
            f.write("// Shutdown Timer, created 2013 Triangle717\n")
            f.write("{0}".format(off_time))

        # Now run shutdown sequence
        theTimer(off_time)


def getTime():
    """Reads TheTime.txt/ShutdownTime.txt for shutdown time in Automatic Mode"""

    # Read line 2 from the_file for shutdown time
    with open(the_file, "rt") as f:
        off_time = f.readlines()[1]
    off_time = off_time.strip("\n")

    print("Your computer will {0} at {1}.".format(the_word, off_time))

    # Run timer
    theTimer(off_time)


def theTimer(off_time):
    """Gets current time and performs the appropriate actions"""

    # If the shutdown time does not equal
    # the current time, as defined by the System Clock
    while off_time != time.strftime("%H:%M", time.localtime()):

        # Required so the current time will be updated when
        # time.sleep(align_time) is finished. The line above
        # will not do this.
        cur_time = time.strftime("%H:%M", time.localtime())

        # Get the current seconds, as defined by the system clock.
        cur_seconds = time.strftime("%S", time.localtime())

        if cur_seconds != 00:
            # Align the timer exactly with the system clock,
            # allowing the computer to begin the shutdown routine
            # exactly when stated.

            # !!WARNING!!
            # Do not change align_time to anything less than 60.
            # Anything less creates a huge bug and throws the timer
            # off by a minute, or creates a negative time

            # Convert to integer so we can subtract
            align_time = 60 - int(cur_seconds)

        print("\nIt is not {0}, it is only {1}. Your computer will not {2}."
        .format(off_time, cur_time, the_word))
        # Sleep for however long until alignment
        time.sleep(align_time)

    print("\nYour computer is {0}.".format(the_word_ing))
    # Let user read message
    time.sleep(1)
    close_Win()


def close_Win():
    """Shutsdown or Retarts Computer depending on Arguments"""

    # Call hidden shutdown.exe CMD app to shutdown/restart Windows

    # The restart command was sent
    if restart:
        # The force command was sent as well
        if force:
            os.system("shutdown.exe /r /f /t 0")
        # Only the restart command was sent
        elif not force:
            os.system("shutdown.exe /r /t 0")

    # Normal shutdown commmand was sent
    elif not restart:
        # The force command was sent as well
        # Using /p shutdowns Windows immediately without warning,
        # Same as /s /t 0
        if force:
            os.system("shutdown.exe /p /f")
        # The force command was not sent
        elif not force:
            os.system("shutdown.exe /p")


if __name__ == "__main__":
    CMDParse()
    close_Type()
    preload()
