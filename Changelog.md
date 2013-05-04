Shutdown Timer Change Log
=========================

1.0.2
-----

**Released ?? ??, 2013**

* Rewrote timer process in an attempt to make **Shutdown Timer** work properly if timer is loaded early in morning
* Display "shutdown" or "restart" depending on if -restart parameter is passed
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
* Changed command-line mode (`-cmd`, `--command`) to Automatic mode (`-a`, `--auto`), messages and function names changed accordingly
* Split up functions in `preload()`
* Moved Python and Windows check from under `preload()`
* Moved `close_Type()` from `preload()`
* Added a few more debug messages
* Cleaned up what is left of `preload()`
* Various cleanup
* Updated README.md with new restart and automatic modes

1.0.1
-----

**Released Never**

* Changed shutdown parameter
* Added Python 3.3.1 shebang line
* Rewrote shutdown command function
* Updated shutdown.exe command
* Added restart computer parameter, supports force command

1.0
---

**Released March 29, 2013**

* First release
* Supports shutdown of computer
* Supports force command
* Dual modes: normal and command-line