[← Return to initial page](https://github.com/Rodarkhen/cmpe131-milestone)

# CMPE 131 Notes App Project

## Table of Contents
- [Collaborators](#Collaborators)
- [Usage](#usage)
- [Requirements](#Requirements)
- [External Sources](#external-sources)

## Collaborators
- Anik Budhathoki (@AnikBudhathoki)
- Nikola Zivkovic (@NickZivkovic)
- Rodrigo Chen (@Rodarkhen) [Team Lead]

## Usage
### Prerequisites
You must have the following prerequisites met or installed on your system:
- Linux
- Python3 (version 3.10.12 or higher)
- Pip3
- [Required Dependencies](dependencies.txt)

### Python 3 Installation
If you have already installed, you can skip this section.

You can check if you already have python3 and pip3 installed or check the version by using the command: ``python3 --version``. If the command is not found, then run ``sudo apt-get install python3``. If the version is older, then run ``sudo apt-get upgrade``

For more information about the installation, [visit this website for Linux](https://wiki.python.org/moin/BeginnersGuide/Download#Linux)

### Instructions
This section provide step-by-step instructions on how to clone the repository from the github, set up the virtual environment, install the required dependencies for this web project, and run the application.
1. ``git clone https://github.com/Rodarkhen/cmpe131-milestone.git``
2. ``cd cmpe131-milestone``
3. ``python3 -m venv venv``
4. ``source venv/bin/activate``
5. ``pip3 install -r dependencies.txt``
6. ``python3 run.py``

After running successfully, you can access the web application with the following url: [http://127.0.0.1:5000](http://127.0.0.1:5000)

If you want to exit the virtual environment, run the following command:
``deactivate``

For more information on virtual environment, [visit this website for more information on venv](https://docs.python.org/3/library/venv.html)

### Reinitialize Database
To reinitialize the database, run the following command: ``python3 initTable.py``

After running this command, all the data stored previsouly will be deleted and a new database file will be created.

## Requirements
This section provides a list of project requirements and responsibilities assigned and implemented by team members:
1. Sign up by [Rodrigo](https://github.com/Rodarkhen) [x]
2. Log in by [Rodrigo](https://github.com/Rodarkhen) [x]
3. Create Notes by [Anik](https://github.com/AnikBudhathoki) [x]
4. Attach Files/images by [Anik](https://github.com/AnikBudhathoki)
5. Search Notes by [Anik](https://github.com/AnikBudhathoki) [x]
6. Delete Notes by [Anik](https://github.com/AnikBudhathoki) [x]
7. Edit Notes by [Anik](https://github.com/AnikBudhathoki) [x]
8. Connect with any external API (Rich Text Editor) by [Anik](https://github.com/AnikBudhathoki) [x]
9. Log Out by [Rodrigo](https://github.com/Rodarkhen) [x]
10. Share Notes by [Rodrigo](https://github.com/Rodarkhen) [x]
11. Edit User Profiles by [Rodrigo](https://github.com/Rodarkhen) [x]
12. Advance search items with regular expressions by [Rodrigo](https://github.com/Rodarkhen) [x]

The requiments with an [x] mark after the collaborator's name is the one that has been implemented.

For more details on these requirements, click [requirements.md](requirements.md)

## External Sources
For this web application, we used some external sources for our logo, icon buttons, and some template
- Logo was taken from [here](https://looka.com/logo-maker/?gad_source=1&gclid=Cj0KCQiA35urBhDCARIsAOU7QwlFNSJU7_sjtb73PVkvwwo8pUAG-jzpAQ6bVCv703u66hnrqNKCQa0aAn4PEALw_wcB)
- Icon buttons was taken from [here](https://www.flaticon.com/free-icons/delete)
- For the template of our page, we used bootstrap.