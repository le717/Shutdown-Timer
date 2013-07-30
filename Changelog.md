Shutdown Timer Change Log
=========================

1.0.2.2
-------

**Released ?? ??, 2013**

* Added ability to enable debug messages if `--test`` parameter is passed from the command-line
* Removed `linecache` usage, replaced with build-in `open()` function
* Minor messages cleanup

1.0.2.1
-------

**Released July 11, 2013**

* Fixed doctype for `close_Type()`
* Fixed mixed-up variable in `AutoMain()`
* Converted writing of `TheTime.txt` to not use Python 3 `print()` function
* Updated script to conform with PEP 8 guidelines
* Updated `setup.py` to conform with PEP 8 guidelines

1.0.2
-----

**Released May 6, 2013**

* Rewrote timer process in an attempt to make **Shutdown Timer** work properly if timer is loaded early in morning
* Display "shutdown" or "restart" depending on if `-r` or `--restart` parameter is passed
* Renamed *ShutdownTime.txt* to *TheTime.txt* added loading of ShutdownTime.txt* only if *TheTime.txt* does not exist
* Unchained import statements
* Small changes
* Added script dividers
* Added `debug` variable and messages (set to `False` by default)
* Made timer process get the newest time after `time.sleep(align_time)` ends (it was using the same time over and over again)
* Fixed alignment time
* Comments update
* Finished rewrite of timer process, now switches to close_Win() if `off_time` is equal to `cur_time`.
* Fixed restart commands, now restarts immediately
* Changed Command-line mode (`-cmd`, `--command`) to Automatic mode (`-a`, `--auto`), messages and function names changed accordingly
* Split up functions in `preload()`
* Moved Python and Windows check from under `preload()`
* Moved `close_Type()` from `preload()`
* Added a few more debug messages
* Cleaned up what is left of `preload()`
* Various cleanup
* Updated *README.md* with new restart and automatic modes
* Added Command-line Arguments section to *README.md*
* Added application icon

1.0.1
-----

**Released Never**

* Changed shutdown parameter
* Added Python 3.3.1 shebang line
* Rewrote shutdown command function
* Updated shutdown.exe commands
* Added restart computer parameter, supports force command

1.0
---

**Released March 29, 2013**

* First release
* Supports shutdown of computer
* Supports force command
* Dual modes: normal and command-line