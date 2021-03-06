LUCA Changes
============

1.0.3
-----
_Released October 18, 2013_

* Better display of Creation date
* Remove spaces in folder and file names
* Added `argparse` based command-line rgument (`-d`, `--date`) to append folders with Creation date, formatted as `YYYY-DD-MM`
* Remove periods from file names
* Run illegal character check before constructing file/folder names
* Fixed issue with URL parser adding Creations from page 1 twice when there are more then 1 pages
(also fixes issue with download statistics reporting too many Creations and files downloaded)

1.0.2
-----
_Released October 16, 2013_

* Fixed issue with URL parser not properly adding multi-paged Creations for download
* Minor tag fixes
* Use version number from `LUCA.py` when freezing

1.0.1
-----
_Released October 15, 2013_

* Added message warning download may take a while to complete
* Changed download statistics to not use the file system
* Save files with `.tmp` extension before giving them proper file extensions
* Delete (possibly large) arrays when finished with them
* Renamed `subfilepath` variable to `subfolder`
* Added dash (`-`) between filenames and assigned numbers
* Moved process to get number of pages to separate function
* Renamed `mainfilepath`  variable to `mainfolder`
* Fixed bug issues with no more than 72 Creations being downloaded
* Various cleanup

1.0
---
_Released October 12, 2013_

* More script comments
* Small variable updates
* Write HTML document before everything else
* Tidying up success message
* Tidying up on displaying of downloaded filename ("progress bar")
* Cleaned up `LUCA.py` and `setup.py` to better conform to PEP 8 style guidelines
* Updated a few messages
* Small internal cleanup
* Include `LICENCE`, `README.md` and `CHANGES.md` file in freeze
* Remove `ehthumbs.db` from number of files downloaded
* Display link in HTML from where Creation was downloaded from
* Write HTML comment stating when and how Creation was archived
* Express archive time in UTC time stamp
* Fixed multiple errors in raw HTML
* Add new HTML headers
* Remove `Desktop.ini` from number of files downloaded
* Use `os.walk()` to get number of files downloaded
* Download each Creation to it's own subfolder
* Reworked process to get number of files downloaded
* Improved method of detecting username
* Fix bug with folders being created with spaces in them
* Added GIF, JPG, WMV, and LXF file type detection
* Tell how many Creations were downloaded
* Added MPG video file type detection
* Completely rewrote the illegal character check
* Improved method of detecting username (again)
* Expanded rewritten illegal character check to HTML documents
* Detect and replace all illegal characters
* Added MOV and AVI video file type detection
* Do not display filename if `UnicodeEncodeError` is raised
* Display images using relative paths
* Prevent possible infinite loop when searching username on Creation Lab
* Lots of cleanup to raw HTML from Creation Lab
* Tell who created the Creation, link username to MLN page
* Rearrange entire HTML document
* Changed HTML writing process
* Display downloaded images
* Created HTML stylesheet
* Show more Creations in search results
* Improved chances of finding a username
* Properly filter illegal characters in folder names
* Display images in proper order
* Write HTML files using binary mode (`wb`, `ab`)
* Download all Creations by a user (fixes multiple pages bug)
* Added app icon (`LUCAIcon.ico`)
* Rename `LICENSE` to `LICENSE.txt`
* Fixed display of tags
* Various HTML fixes
* PEP 8 checks
* Restored memberid code
* Remove debug prints
* Wrap all code in functions
* Adapt Date field for Creations from LEGO Universe competitions
* Added script dividers

0.3
---
_Released June 23, 2013_

* Small message formatting
* Added missing `</head>` tag for HTML document
* Fixed hard-coded download folder location
* Added Python hashbang
* Write window title using program name and version number
* Changed app closing method
* Converted most script usage of string literals to use the format method
* Added `setup.py`
* Converted all whitespace from tabs to 4 spaces (per Python standard)
* Updated HTML document writing to use recommended `with` handle
* Updated error message to include user input
* Added global variables containing program name and version
* Added GPL block to `LUCA.py` and `setup.py`
* Added a few script comments
* Improved layout of written HTML document
* If download folder does not exist, make it. Otherwise, start the download
* Converted non-HTML file writing to use recommended `with` handle
* Fixed exit code number when closing the program
* Cleaned up saving path for both HTML and non-HTML files
* Added "Successful Download" message
* Added number of files downloaded into "Successful Download" message
* Added exit routine after finishing the download
* Added message to inform user their files are downloading
* Display list of downloaded file (LUCA's non-GUI version of a progress bar)
* Updated "progress bar" to display filename as soon as it is downloaded, not after everything was downloaded
* Added error handling when LUCA does not find any links when searching on the Creation Lab for an entered username
* Updated: usernames are now case-insensitive.
* Added filtering of Windows invalid characters in filename (code from Triangle717, [Issue #4](https://github.com/Brickever/LUCA/issues/4)

0.2
---
_Released May 29, 2013_

* Added invalid website check
* Updated user input to ask for Creation Lab `username` only, rather than `memberid` and `username`
* Added code to get `memberid` from website, and check it against `username`
* Variable names update
* Added error handling for a username that does not match with the one found online.
* Removed invalid website check (no longer needed)

0.1
---
_Released Never_
