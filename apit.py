import sys
import json
from colorama import Fore as colors

args = sys.argv[1:]

def log_help():
    with open("help.txt") as help_file:
        print(help_file.read())

base = open("base.json", "r", encoding="UTF-8")
base = json.load(base)
projects = base["projects"]
version = base["version"]
directory = "root"

print(colors.YELLOW + f"run on version {version}\n\n" + colors.RESET)

if len(sys.argv) == 1:
    print("apit\na API Tester for debug your APIs\ncommands:\n\tusage: apit [command] <options>\n\taddp [PROJECT]: add a project\n\t\t--base-link: base link of project\n\t\t-C --cp: cd to project after create\n\taddf [FOLDER]: add a folder\n\trmp [PROJECT]: remove a project\n\trmf [FOLDER]: remove a folder\n\tadd [API]: add a api\n\trm [API]: remove a api\n\trun [API]: run a api\nfor more help, run apit -h or apit --help")
    quit()
match args[0]:
    case "-h":
        log_help()
    case "--help":
        log_help()
    case "sal":
        colors_letters = {"W": colors.WHITE, "Y": colors.YELLOW, "R": colors.RED, "B": colors.BLUE}
        if directory == "root":
            print("projects")
            for name, project in projects.items():
                print(colors_letters[project["color"]] + name + colors.RESET)
        elif directory.count("/") == 1:
            print("folders")
            for name, folder in projects[directory.split("/")[0]].folders.items():
                print(name)

    case "addp":
        try:
            if args[1] == "-h" or args[0] == "--help":
                print("addp\nadd a new project\n\t-C --cd: cd to project\n\tusage: addp [options]\n\t--base-link [LINK]: base link of project (default is 127.0.0.1:5000)\n\t--token [TOKEN] token of project\n\t-r -b -y -w: colors of project(red, blue, yellow and white)\n\t")
            if args[1].lower() not in [key for key, value in projects.items()]:
                color = None
                color = "R" if '-r' in args[1:] else color
                color = "Y" if '-y' in args[1:] else color
                color = "B" if '-b' in args[1:] else color
                color = "W" if '-w' in args[1:] else color
                if color == None:
                    color = "W"

                if "--base-link" in args:
                    if args[args.index("--base-link") + 1][-1] == "/":
                        link = args[args.index("--base-link") + 1]
                    else:
                        link = args[args.index("--base-link") + 1] + "/"
                else:
                    link  = "127.0.0.1:5000"

                if "--token" in args:
                    token = link = args[args.index("--token") + 1]
                else:
                    token = None

                projects[args[1]] = {"folders": {}, "APIs": {}, "color": color, "link": link, "token": token}
                print("empty project created")
            else:
                print("project is exist, see -h for more information")

        except IndexError:
            print("please enter the project name\nsee -h for more informations")
    case "rmp":
        try:
            if args[1] in [key for key, value in projects.items()]:
                del projects[args[1]]
            else:
                print("project not exists")
        except IndexError:
            print("please enter project name")
    case "cp":
        if args[1] == "-h" or args[1] == "--help":
            print("cp\nchange directory or folder\n\tusage: cp [path]")
        if directory == "root":
            if args[1] in [key for key, value in projects.items()]:
                directory = args[1]
            else:
                print("project not exist")
        else:
            if args[1] in projects[directory]["folders"]:
                directory = directory + '/' + args[1]
            else:
                print("folder not exists")


with open("base.json", "w", encoding="UTF-8") as base:
    base.write(json.dumps({"projects": projects, "version": version}))
