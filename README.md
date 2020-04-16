## Running the PresenceTracker

You can run on Windows, Mac or Linux. The only prerequisite is
Python 3.5 or 3.6. Python 3.7 is not yet officially supported. It may or may not
work.

## Setup (Packaging for your operating system)
Create a virtual environment in the current directory:

    python3 -m venv venv

Activate the virtual environment:

    # On Mac/Linux:
    source venv/bin/activate
    # On Windows:
    call venv\scripts\activate.bat


Install the required libraries (most notably, `fbs` and `PyQt5`):

    pip3 install psycopg2 fbs PyQt5==5.9.2

(If this produces errors, try `pip3 install wheel` first.)

You can also use Qt for Python instead of PyQt. To do this, simply write
`PySide2` instead of `PyQt5`. For the above, use
`pip install PySide2==5.12.0`.

## Run the app
To run the basic PyQt application from source, execute the following command:

    fbs run

## Freezing the app
We want to turn the source code of our app into a standalone executable that can
be run on your computer. In the context of Python applications, this
process is called "freezing".

Use the following command to turn the app's source code into a standalone
executable:

    fbs freeze

This creates the folder `target/PresenceTracker`. You can copy this directory to any
other computer (with the same OS as yours) and run the app there!

## Creating an installer
On Windows, this would be an executable called `PresenceTracker.exe`.
On Mac, mountable disk images such as `PresenceTracker.dmg` are commonly used.
On Linux, `.deb` files are common on Ubuntu, `.rpm` on Fedora / CentOS, and
`.pkg.tar.xz` on Arch.

fbs lets you generate each of the above packages via the command:

    fbs installer

Depending on your operating system, this may require you to first install some
tools. Please read on for OS-specific instructions.

### Windows installer
Before you can use the `installer` command on Windows, please install
[NSIS](http://nsis.sourceforge.net/Main_Page) and add its installation directory
to your `PATH` environment variable.

The installer is created at `target/PresenceTracker.exe`. It lets your users pick
the installation directory and adds your app to the Start Menu. It also creates
an entry in Windows' list of installed programs. Your users can use this to
uninstall your app. 

### Mac installer
On Mac, the `installer` command generates the file `target/PresenceTracker.dmg`. 

To install your app, your users simply drag its icon to the _Applications_
folder.

### Linux installer
On Linux, the `installer` command requires that you have
[fpm](https://github.com/jordansissel/fpm). You can for instance follow
[these instructions](https://fpm.readthedocs.io/en/latest/installing.html) to
install it.

Depending on your Linux distribution, fbs creates the installer at 
`target/PresenceTracker.deb`, `...pkg.tar.xz` or `...rpm`. Users can use these
files to install your app with their respective package manager.
