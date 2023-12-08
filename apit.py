import sys
import json

args = sys.argv[1:]

def log_help():
    with open("help.txt") as help_file:
        print(help_file.read())

base = open("base.json", "r", encoding="UTF-8")
base = json.load(base)
projects = base.projects
version = base.version
directory = "root"

match args[0]:
    case "-h":
        log_help()
    case "--help":
        log_help()
    case "addp":
        try:
            if args[1] == "-h" or args[0] == "--help":
                print("addp\nadd a new project\n\t-C --cd: cd to project\n\tusage: addp [options]\n\t--base-link [LINK]: base link of project (default is 127.0.0.1:5000)\n\t--token [TOKEN] token of project\n\t-r -b -y -w: colors of project(red, blue, yellow and white)\n\t")
                break
            if args[1].lower() not in [key for key, value in projects.items()]:
                color = "R" if '-r' in args[1:] else None
                color = "Y" if '-y' in args[1:] else None
                color = "B" if '-b' in args[1:] else None
                color = "W" if '-w' in args[1:] || color == None

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

                projects[args[1]] = {"folders": [], "APIs": [], "color": color, "link": link, "token": token}
            else:
                print("project is exist, see -h for more information")

        except IndexError:
            print("please enter the project name\nsee -h for more informations")
    case "cd":
        if args[1] == "-h" or args[1] == "--help":
            print("cd\nchange directory or folder\n\tusage: cd [path]")
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
