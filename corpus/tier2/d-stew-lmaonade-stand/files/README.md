# ABOUT

LMAONADE STAND is a modern take on the classic game of supply and demand.

Written in LOLCODE mostly for the lolz, the game can be run using lci, a LOLCODE interpreter written in C and designed to be correct,
portable, fast, and precisely documented.

The LOLCODE project homepage is at http://lolcode.org.  For help, visit
http://groups.google.com/group/lci-general.

# PREREQUISITES

1. You must have CMake installed (www.cmake.org). 
  a) If you're using a Linux distro with package managment CMake should be in 
    your repositories.

2. Python 2.7+ or Python 2.x with the argparse module installed.
  
# INSTALLATION ON LINUX OR MAC OSX

1. Configure lci using CMake. This can be as simple as opening up the terminal, 
  navigating to the directory containing lci and typing:

  $ cmake .

  You can also use the "ccmake" command or the CMake GUI if you prefer.
  See the cmake documentation for more details.

2. Build the project:

  $ make

3. Install
   
  $ make install

5. Run game:

  $ lci lmaonade-stand.lol

# INSTALLATION ON WINDOWS

1. Add MinGW and Python to your PATH.

  - Start > right-click Computer > Properties > Advanced system settings
    > Environment Variables....
    
  - Select the "PATH" variable and click "Edit...".
  
  - Add ";C:\MinGW\bin;C:\Python32" to the end.
  
3. Open an Administrator shell

  - Start > All Programs > Accessories > right-click Command Prompt
    > Run as administrator.
 
4. Navigate to the project directory using the "cd" command, for example,

  > cd C:\Users\%user%\Documents\lci
 
5. run the script install.py. Note that

  > install.py -h

  will display a list of relavent install options. For
  example, if I wanted to install lci to the directory
  "C:\Program Files\lci" I would run:

  > install.py --prefix="C:/Program Files/lci"
  
  (notice that forward slashes are used to separate directories.)
