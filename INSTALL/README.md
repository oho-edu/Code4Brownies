# Install student's plug-in

First, install [Sublime Text 3](https://www.sublimetext.com/3).

Open Sublime Text, go to View, click Show Console, copy this code, paste to console and hit enter:

```
import os; package_path = os.path.join(sublime.packages_path(), "C4BStudent"); os.mkdir(package_path) if not os.path.isdir(package_path) else print("dir exists"); c4b_py = os.path.join(package_path, "Code4Brownies.py") ; c4b_menu = os.path.join(package_path, "Main.sublime-menu"); c4b_version = os.path.join(package_path, "VERSION"); import urllib.request; urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BStudent/Code4Brownies.py", c4b_py); urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BStudent/Main.sublime-menu", c4b_menu); urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/VERSION", c4b_version)
```

After installation, students can share codes using the menu "ShareCode".

# Uninstall student's plugin

Open Sublime Text, go to View, click Show Console, copy this code, paste to console and hit enter:

```
import os; import shutil; package_path = os.path.join(sublime.packages_path(), "C4BStudent"); shutil.rmtree(package_path)
```


# Install instructor's plug-in

To use Code4Brownies as an instructor, you will need to install Sublime Text (ST3), a plug in to ST3, and the server to run on your laptop. Instructor and students communicate via the server.

First, install [Sublime Text 3](https://www.sublimetext.com/3).

Next, open Sublime Text, go to View, click Show Console, copy the code below, paste it to console and hit enter:

```
import os; package_path = os.path.join(sublime.packages_path(), "C4BInstructor"); os.mkdir(package_path) if not os.path.isdir(package_path) else print("dir exists"); c4b_py = os.path.join(package_path, "Code4BrowniesInstructor.py") ; c4b_menu = os.path.join(package_path, "Main.sublime-menu"); c4b_version = os.path.join(package_path, "VERSION"); import urllib.request; urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BInstructor/Code4BrowniesInstructor.py", c4b_py); urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/C4BInstructor/Main.sublime-menu", c4b_menu); urllib.request.urlretrieve("https://raw.githubusercontent.com/vtphan/Code4Brownies/master/src/VERSION", c4b_version)
```

Finally, donwload the server and run it on the instructor's machine.

- [Windows 64bit](https://github.com/vtphan/Code4Brownies/raw/master/INSTALL/c4b_windows_amd64.exe)
- [Mac 64bit](https://github.com/vtphan/Code4Brownies/raw/master/INSTALL/c4b_darwin_amd64).
- [Linux 64bit](https://github.com/vtphan/Code4Brownies/raw/master/INSTALL/c4b_linux_amd64).
- Create a directory called "db" to store student records (in CSV format).

### Running the server on the instructor's laptop

Students and the instructor communicate by sending messages to a server.  The server should be run on the the instructor's computer.

Windows: run the server in a Powershell terminal
```
    .\c4b_windows_amd64.exe -db db.csv
````

OS X: run the server in a terminal
```
    ./c4b_darwin_amd64 -db db.csv
````

Linux: run the server in a terminal
```
    ./c4b_linux_amd64 -db db.csv
````

If you want to run the server with the source code, you need to install Go.  To run the server:
```
    ./go run *.go -db db.csv
````
db.csv is the student database, stored in comma-separated format.


# Uninstall instructor's plugin

Open Sublime Text, go to View, click Show Console, copy this code, paste to console and hit enter:

```
import os; import shutil; package_path = os.path.join(sublime.packages_path(), "C4BInstructor"); shutil.rmtree(package_path)
```

