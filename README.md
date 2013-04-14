Shutdown Timer
==============

**Shutdown Timer** is a [Python 3](http://python.org) application created by [Triangle717](http://triangle717.wordpress.com) to shutdown your Windows computer 
at a specified time. 

How It Works
------------

**Shutdown Timer** is a two-mode application: a normal, click-and-run application, and command-line. The two modes work together, and one actually relies on 
the other. 

### Normal Mode

The first and main mode is the click-and-run (normal) mode. In this mode, you enter the time you want the computer to shutdown using 24 (military) time, and 
press &lt;Enter&gt;. **Shutdown Timer** will then take that time and the current time, as defined by the system clock, and compares the two.  If the two times 
do not match, it will run until they do match, when it will then shutdown your computer. 

### Command line Mode

The second mode is the command-line mode, which is activated by typing ```ShutdownTimer.exe -cmd``` or ```ShutdownTimer.exe --command```. The command line mode 
does not allow you to enter a shutdown time. Instead, it is the "automated mode" of **Shutdown Timer**. It uses a small text file written by the normal mode as 
the shutdown time. This allows you to always turn off your computer at the same time multiple times without typing in the time each launch, providing you 
haven't run the normal mode and changed the time. If the file the command-line mode relies on is not found, it will proceed to the normal mode so the file will 
be written. You can see all the command line arguments by running ```ShutdownTimer.exe --help```. 

System Requirements
-------------------

### Operating System

To use **Shutdown Timer**, you will need to be running Windows. It has been successfully tested on Windows 7 and 8, It may work on XP and Vista, but it has not 
been tested. A check has been added to **Shutdown Timer** to prohibit it from running on any other operating systems. 

If you run the Python script directly, you will need to same operating system requirements, in addition to a Python 3.3.0 interpreter. Again, a check will stop 
it on running on any versions lower than 3.3.0. 

If you want to run the EXE, again, you need to meet the operating system requirements and have the Microsoft Visual Studio C++ 2010 Redistributable Package, 
either [x86](http://www.microsoft.com/en-us/download/details.aspx?id=5555) or [x64](http://www.microsoft.com/en-us/download/details.aspx?id=14632), depending 
on the EXE version you use.  If you are unsure if you need this package or not, here's a helpful hint:
Only if you get an error message saying "MSVCR100.dll is missing from your computer" do you need to install it. Otherwise, there is not need. 
 
Contributing
------------

If you would like to contribute to the development of **Shutdown Timer**, submit a patch, or compile your own build, please take a look at 
[CONTRIBUTING.md](CONTRIBUTING.md). 

Releases
--------

* Version 1.0 - March 29, 2013

> [Source Code](https://github.com/le717/Shutdown-Timer/tree/V1.0)

***Shutdown Timer* is created 2013 Triangle717 and is released under the [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html)**
