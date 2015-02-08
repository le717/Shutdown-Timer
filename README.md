# Shutdown Timer [![Build Status](https://travis-ci.org/le717/Shutdown-Timer.svg)](https://travis-ci.org/le717/Shutdown-Timer) #

> Small, Windows-only program to shutdown or restart your computer at a stated time.

## Usage ##
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
* Windows XP or higher. Mac OS X and Linux versions will not be developed.

## License ##
[GPL v3](http://www.gnu.org/licenses/gpl.html)

Created 2013, 2015 Triangle717
