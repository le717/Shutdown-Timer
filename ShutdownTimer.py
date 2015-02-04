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

    def _runCommand(self):
        """"""
        pass
        # subprocess.call(self._getCommand())

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

    def _isBetween(self, val, minV, maxV):
        """Check that a value is within inclusive acceptable range.

        @return {Boolean} True if in range, False if not.
        """
        return val >= minV and val <= maxV

    def _getCurTime(self):
        """Get the current time, according to the system clock.

        @return {Tuple}
        """
        curTime = time.localtime()
        return (curTime[3], curTime[4], curTime[5])

    def _calcHoursLeft(self, curHour, offHour):
        """Calculate the number of hours that remain until closing.

        @param {Number} curHour TODO.
        @param {Number} offHour TODO.
        @return {Number} The number of hours remaining.
        """

        # It will happpen this very hour
        if curHour == offHour:
            return 0

        # 4-23 hours over night
        elif curHour > offHour:
            # Midnight through noon
            if self._isBetween(offHour, 0, 12):
                return (24 + offHour) - curHour

                # 1 PM through 11 PM
            elif self._isBetween(offHour, 13, 23):
                return 24 + (offHour - curHour)

        # 1-18 hours today
        elif offHour > curHour:
            return offHour - curHour

    def _countDown(self):
        """Calculate remaining time and wait until closing can occur."""
        curHour, curMin, curSec = self._getCurTime()

        # If the shutdown time does not equal, the current time,
        # as defined by the local system's clock
        while (
            "{0}:{1}".format(curHour, curMin) !=
            "{0}:{1}".format(self.__time[0], self.__time[1])
        ):
            curHour, curMin, curSec = self._getCurTime()

            # Calculate remaining hours
            remainHours = self._calcHoursLeft(curHour, self.__time[0])

            # Calculate remaining minutes
            if curMin > self.__time[1]:
                 remainMins = curMin - (self.__time[1] - 1)
            else:
                 remainMins = (self.__time[1] - 1) - curMin

            # Prevent the minutes from reading -1
            if remainMins == -1:
                remainMins = 0

            # Calculate remaining seconds
            remainSecs = 60 - curSec

            # Prevent the seconds from reading 60
            if remainSecs == 60:
                remainSecs = "00"

            # Add the leading zeros
            elif self._isBetween(remainSecs, 1, 9):
                remainSecs = "0{0}".format(remainSecs)

            # Display remaining time
            remainTime = "{0}:{1}".format(remainMins, remainSecs)

            # Display hours if needed too
            if curHour == 0:
                 remainTime = "{0}:{1}".format(remainHours, remainTime)

            print("Time remaining until {0}: {1}".format(self.verbs[0], remainTime))
            time.sleep(1)
        print("\nYour computer will now {0}.".format(self.verbs[0]))
        return True

    def getTime(self):
        """Get the time the computer will close.

        @return {String}
        """
        time = []

        # Hours
        if self._isBetween(self.__time[0], 0, 9):
            time.append("0{0}".format(self.__time[0]))
        else:
            time.append(str(self.__time[0]))

        # Add the colon
        time.append(":")

        # Minutes
        if self._isBetween(self.__time[1], 0, 9):
            time.append("0{0}".format(self.__time[1]))
        else:
            time.append(str(self.__time[1]))

        return "".join(time)

    def setTime(self, userTime):
        """Validate and set the time the computer will close."

        @param {String} userTime The user-provided time to close.
        @return {!Boolean} True if the time was set,
                False if defined time format was not followed,
                A ValueError will be raised if a value
                    is not in acceptable range.
        """

        # Make sure it follows a certain format
        formatRegex = re.match(r"(\d{2}):(\d{2})", userTime)
        if formatRegex is None:
            print("The time is not in the required HH:MM format!")
            return False

        # Convert the values to intergers
        hours = int(formatRegex.group(1))
        mins = int(formatRegex.group(2))

        # Hours value is out of range
        if not self._isBetween(hours, 0, 24):
            raise ValueError("Hour values must be between 0 and 24.")

        # Minutes value is out of range
        if not self._isBetween(mins, 0, 59):
            raise ValueError("Minute values must be between 0 and 59.")

        # Store the time
        self.__time = (hours, mins)
        return True

    def start(self):
        """"""
        print()
        if self._countDown():
            print(self._getCommand())

    def setModes(self, auto=False, force=False, restart=False):

        self.__auto = auto
        self.__force = force
        self.__restart = restart

    def getModes(self):
        """Get the Windows closing options.

        @return {Tuple} Three index tuple containing Boolean values for
            automatic, force, restart modes. In all case, a value of True
            represents that mode is enabled and False disabled.
        """
        return (self.__auto, self.__force, self.__restart)


def main():
    """Basic temporary UI until GUI is implemented."""
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
        timer.start()


if __name__ == "__main__":
    main()
