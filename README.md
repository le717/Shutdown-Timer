Shutdown Timer
==============

**Shutdown Timer** is a [Python 3](http://python.org) application created by [Triangle717](http://Triangle717.WordPress.com) 
to shutdown or restart your Windows computer at a specified time.

How It Works
------------

**Shutdown Timer** is a two-mode application: a normal, click-and-run mode, and an automatic mode. The two modes work together, and one actually relies on 
the other. 

### Normal Mode

The first and main mode is the click-and-run (normal) mode. In this mode, you enter the time you want the computer to halt (shutdown or restart)
using 24 (military) time, and press &lt;Enter&gt;. **Shutdown Timer** will then take that time and the current time, as defined by the system clock, and 
compare the two. If the two times do not match, it will run until they do match, when it will then halt your computer. 

### Automatic Mode

The second mode is the automatic mode. The automatic mode does not allow you to enter a halt time. Instead, it uses a small text file written by the normal mode as the halt time. This allows you to always halt your computer at the same time multiple times without typing in the time each launch, providing you 
haven't run the normal mode and changed the halt time. 
If the file the automatic mode relies on is not found, it will proceed to the normal mode so the file will be written. 


### Command-line Arguments

**Shutdown Timer** contains a few command-line arguments. None of the commands conflict with each other; they all can be used at once.
You can get more details on each command line argument by running `ShutdownTimer.exe --help`. 

* **Automatic Mode**, discussed above, is activated by running `ShutdownTimer.exe -a` or `ShutdownTimer.exe --auto`.
* Instead of shutting down the computer, you can **restart** it instead. Just pass `ShutdownTimer.exe -r` or `ShutdownTimer.exe --restart`.
* The **force** argument sends the force command to Windows, making the computer halt even if a process is preventing it from halting.
Pass `ShutdownTimer.exe -f` or `ShutdownTimer.exe --force` to send the force command.


System Requirements
-------------------

### Operating System

To use **Shutdown Timer**, you will need to be running Windows. It has been successfully tested on Windows Vista, 7 and 8. It may work on Windows XP, but it has not been tested. A check has been added to **Shutdown Timer** to prohibit it from running on non-Windows operating systems. 

If you run the Python script directly, you will need to same operating system requirements, in addition to having at least a Python 3.3.0 interpreter. 
Again, a check will stop it on running on any versions lower than 3.3.0. 

If you want to run the Exe, again, you need to meet the operating system requirements and have the [Microsoft Visual Studio C++ 2008 Redistributable Package](http://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=29), 
installed. If you are unsure if you need this package or not, here's a hint:
Only if you get an error message saying "MSVCR100.dll is missing from your computer" do you need to install it. Otherwise, it is not needed. 

Releases
--------

* Version 1.0.2.1 - July 11, 2013

> [Source Code + Direct Download](https://github.com/le717/Shutdown-Timer/releases/v1.0.2.1)

* Version 1.0.2 - May 6, 2013

> [Source Code](https://github.com/le717/Shutdown-Timer/tree/V1.2)

> [Direct Download](https://github.com/le717/Shutdown-Timer/archive/V1.2.zip)

* Version 1.2 - May 6, 2013

> [Source Code](https://github.com/le717/Shutdown-Timer/tree/V1.2)

> [Direct Download](https://github.com/le717/Shutdown-Timer/archive/V1.2.zip)

* Version 1.0 - March 29, 2013

> [Source Code](https://github.com/le717/Shutdown-Timer/tree/V1.0)

> [Direct Download](https://github.com/le717/Shutdown-Timer/archive/V1.0.zip)

***Shutdown Timer*, created 2013 Triangle717 and is released under the [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html)**