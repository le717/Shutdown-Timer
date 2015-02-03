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


import os
import re
import sys
import json
import time
import argparse
import platform
# import subprocess
from threading import Timer

import constants as const


class ShutdownTimer:

    def __init__(self):

        self.__time = None
        self.__auto = False
        self.__force = False
        self.__restart = False
        self.__configData = None
        self.__configPath = self._getConfigPath()
        self.__jsonFile = os.path.join(self.__configPath, "Shutdown-Timer.json")
        self._loadConfig()
        self._commandLine()
        self.verbs = self._getVerb()

    def _getConfigPath(self):
        """Get the file path where configuration files will be stored.

        @returns {String} The configuration path, %AppData%,Triangle717/*AppName*.
        """
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

    def saveConfig(self):
        """Write the JSON-based config file.

        @returns {Boolean} True if the config file was written, False otherwise.
        """
        try:
            jsonData = {
                "auto": self.__auto,
                "force": self.__force,
                "restart": self.__restart,
                "time": self.__time
            }
            with open(self.__jsonFile, "wt", encoding="utf_8") as f:
                f.write(json.dumps(jsonData, indent=4, sort_keys=True))
            return True

        # Silently fail
        except PermissionError:
            return False

    def _getVerb(self):
        """Set the action verbs for use in messages depending on restart status.

        @return {Tuple} Two index tuple containing the action verbs.
        Second index is the "ing" form of the verb.
        """
        if self.__restart:
            return ("restart", "restarting")
        return ("shutdown", "shutting down")

    def _getCommand(self):
        """Construct the shutdown command based on user option selection.

        @returns {String} The exact commands to run.
        """
        commands = ["shutdown.exe"]

        # Restart or shutdown computer?
        if self.__restart:
            commands.append("/r")
        else:
            commands.append("/p")

        # Force closing, do not wait for any programs
        if self.__force:
            commands.append("/f")

        # Restarting will always have a timeout dialog before
        # the process starts, remove it to match shutdown behavior
        if self.__restart:
            commands.append("/t 0")

        return " ".join(commands)

    def _commandLine(self):
        """Command-line arguments parser.

        @returns {Boolean} Always returns True.
        """
        parser = argparse.ArgumentParser(
            description="{0} Command-line arguments".format(const.appName))

        # Auto mode
        parser.add_argument("-a", "--auto",
                            help="Run in automatic mode using previously set time.",
                            action="store_true")

        # Force mode
        parser.add_argument("-f", "--force",
                            help="Force Windows to close without waiting on programs",
                            action="store_true")

        # Restart mode
        parser.add_argument("-r", "--restart",
                            help="Restart Windows instead of shutting down",
                            action="store_true")

        args = parser.parse_args()
        self.__auto = args.auto
        self.__force = args.force
        self.__restart = args.restart
        return True

    def getTime(self):
        """Get the time the computer will close.

        @return {String}
        """
        return self.__time

    def setTime(self, userTime):
        """Validate and set the time the computer will close."

        @param {String} userTime The user-provided time to close.
        @return {!Boolean} True if the time was set,
                False if defined time format was not followed,
                A ValueError will be raised if a value
                    is not in acceptable range.
        """

        def isBetween(val, minV, maxV):
            """Check that a value is within inclusive acceptable range.

            @return {Boolean} True if in range, False if not.
            """
            return val >= minV and val <= maxV

        # Make sure it follows a certain format
        formatRegex = re.match(r"(\d{2}):(\d{2})", userTime)

        if formatRegex:
            # Convert the values to intergers
            hours = int(formatRegex.group(1))
            mins = int(formatRegex.group(2))

            # Hours value is out of range
            if not isBetween(hours, 0, 24):
                raise ValueError("Hour values must be between 0 and 24.")

            # Minutes value is out of range
            if not isBetween(mins, 0, 59):
                raise ValueError("Minute values must be between 0 and 59.")

            # Store the time
            self.__time = userTime
            return True
        return False

    def start(self):

        print(self._getCommand())


def CMDParse():
    """Parses Command-line Arguments"""
    parser = argparse.ArgumentParser(
        description="{0} {1} Command-line arguments".format(const.appName, const.version))

    # Automatic mode argument
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


def close_Type():
    """Change app messages depending if we are shutting down or restarting"""

    global the_word, the_word_ing
    if restart:
        the_word = "restart"
        the_word_ing = "restarting"
    elif not restart:
        the_word = "shutdown"
        the_word_ing = "shutting down"


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

    # User typed a valid time, run shutdown sequence
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



def tempMain():
    """Temporary UI until GUI is implemented."""
    os.system("title {0} v{1}".format(const.appName, const.version))
    timer = ShutdownTimer()

    print("""
Enter the time you want the computer to {0}.
Use the 24-hour system in the following format: "HH:MM".
Submit a "q" to exit.""".format(timer.verbs[0]))
    offTime = input("\n\n> ").lower().strip()

    # Quit program
    if offTime == "q":
        raise SystemExit(0)

    # The user's time was successfully set
    if timer.setTime(offTime):
        timer.saveConfig()


if __name__ == "__main__":
    # tempMain()
    CMDParse()
    close_Type()
    main()
