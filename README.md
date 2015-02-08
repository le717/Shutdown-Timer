# Shutdown Timer [![Build Status](https://travis-ci.org/le717/Shutdown-Timer.svg)](https://travis-ci.org/le717/Shutdown-Timer) #

> Small, Windows-only program to shutdown or restart your computer at a stated time.

## Usgae ##
Enter the time you want the computer to close (shutdown or restart) using 24 (military) time, and press &lt;Enter&gt;
**Shutdown Timer** will then take that time and the current time, as defined by the system clock, and compare the two.
If the two times do not match, it will run until they do match, when it will then halt your computer.


## Command-line Arguments ##
**Shutdown Timer** contains a few command-line arguments. None of the commands conflict with each other; they all can be used at once.
You can get more details on each command line argument by running `ShutdownTimer.exe --help`.

* Instead of shutting down the computer, you can **restart** it instead. Just pass `ShutdownTimer.exe -r` or `ShutdownTimer.exe --restart`.
* The **force** argument sends the force command to Windows, making the computer halt even if a process is preventing it from halting.
Pass `ShutdownTimer.exe -f` or `ShutdownTimer.exe --force` to send the force command.


## Requirements ##
To use **Shutdown Timer**, you will need to be running Windows. It has been successfully tested on Windows Vista, 7 and 8. It may work on Windows XP, but it has not been tested. A check has been added to **Shutdown Timer** to prohibit it from running on non-Windows operating systems.

If you run the Python script directly, you will need to same operating system requirements, in addition to having at least a Python 3.3.0 installation.

## License ##
[GPL v3](http://www.gnu.org/licenses/gpl.html)

Created 2013, 2015 Triangle717
