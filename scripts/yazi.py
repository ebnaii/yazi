import argparse
from prettytable import PrettyTable
import subprocess
from colorama import Fore, Style
import json
from pathlib import Path
import re
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Script to manage YAZI")
    parser.add_argument('action', nargs='?', choices=['start', 'stop', 'install', 'uninstall', 'remove', 'help'])
    
    args = parser.parse_args()

    if not args.action:
        print_help()
        return
    
    if args.action == 'start':
        start()
    elif args.action == 'stop':
        stop()
    elif args.action == 'install':
        install()
    elif args.action == 'uninstall':
        uninstall()
    elif args.action == 'remove':
        remove()
    elif args.action == 'help':
        print_help()



def start():

    table = PrettyTable()

    table.field_names = [Fore.YELLOW + 'Container name' + Style.RESET_ALL, Fore.YELLOW + 'Image TAG' + Style.RESET_ALL, Fore.YELLOW + 'State' + Style.RESET_ALL, Fore.YELLOW + 'Version' + Style.RESET_ALL]


    getContainersCommand = f"podman ps -a --format json"
    
    result = subprocess.run(getContainersCommand, shell=True, capture_output=True)
    containers = json.loads(result.stdout)
    deletionStatus = 0
    if containers:
        for container in containers:
            table.add_row([container['Names'][0], container['Labels']['yazi.tag'], (Fore.GREEN + container['State'] + Style.RESET_ALL) if container['State'] == "running" else (Fore.RED + "stopped" + Style.RESET_ALL), container['Labels']['yazi.version']])
        print("\n👀 Available containers :\n\n")
        print(table)
    
        toStart = input('\n👉 Enter the name of the container to start : ')

        startContainer = f'podman start {toStart}'
        enterContainer = f'podman exec -it {toStart} zsh'
        if subprocess.run(startContainer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode == 0: 
            subprocess.run(enterContainer, shell=True)
        else:
            print('☣️  An error occured, are you sure you entered the right name ?')
    else:
        if input('👉 No container to start, do you want to create one ? (y/N) : ') not in ['y','Y']:
            print("👋 Exiting")
            exit(0)
        install()

def stop():
    
    print("\n👀 Available containers :\n\n")

    table = PrettyTable()

    table.field_names = [Fore.YELLOW + 'Container name' + Style.RESET_ALL, Fore.YELLOW + 'Image TAG' + Style.RESET_ALL, Fore.YELLOW + 'State' + Style.RESET_ALL, Fore.YELLOW + 'Version' + Style.RESET_ALL]


    getContainersCommand = f"podman ps --format json"
    
    result = subprocess.run(getContainersCommand, shell=True, capture_output=True)
    containers = json.loads(result.stdout)
    deletionStatus = 0
    if containers:
        for container in containers:
            table.add_row([container['Names'][0], container['Labels']['yazi.tag'], (Fore.GREEN + container['State'] + Style.RESET_ALL) if container['State'] == "running" else (Fore.RED + "stopped" + Style.RESET_ALL), container['Labels']['yazi.version']])

    print(table)
    
    toStop = input('\n👉 Enter the name of the container to stop : ')

    stopContainer = f'podman stop {toStop}'
    if subprocess.run(stopContainer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode == 0:
        print(f'\n🛑 Stopped {toStop}')
    else:
        print('☣️  An error occured, are you sure you entered the right name ?')
    


def install():

    print("\n👀 Available images :\n\n")

    table = PrettyTable()
    
    table.field_names = [Fore.YELLOW + 'Image' + Style.RESET_ALL, Fore.YELLOW + 'Size' + Style.RESET_ALL, Fore.YELLOW + 'Status' + Style.RESET_ALL]

    getImages = "podman images --format json"
    result = subprocess.run(getImages, shell=True,capture_output=True)
    images = json.loads(result.stdout)
    alreadyBuilded = []
    for image in images:
        try:
            if re.search(r"yazi", image['Names'][0]):
                alreadyBuilded.append(image['Names'][0].split(':')[1])
                alreadyBuilded.append(image['Labels']['yazi.version'])
        except KeyError as e:
            continue
    
    PATH="~/yazi/scripts/*"
    result = subprocess.run(f'find {PATH} -maxdepth 1 -type d', shell=True, capture_output=True, text=True)
    folders = result.stdout.split()
    availableImages = []
    for folder in folders:
        name=Path(folder).name
        availableImages.append(name)
        size = subprocess.run(f"awk -F= '/SIZE/ {{print $2}}' {folder}/.data", shell=True, capture_output=True, text=True).stdout
        installed="Not installed"
        if name in alreadyBuilded:
            installed=f"Installed (v{alreadyBuilded[alreadyBuilded.index(name)+1]})"
        table.add_row([name, size, installed])

    
    print(table)
    TAG = input("\n\n🚀 Select an image to use : ")
    if TAG not in availableImages:
        print(f'👎 Unavailable image : {TAG}\n')
        exit(1)
    FOLDER = TAG
    TAG = 'yazi:' + TAG
    HOSTNAME = input('👽 Select a name for your container : ')
    HOSTNAME = 'yazi-'+HOSTNAME
    confirm = input('\n\n❓ Do you want to create '+ Style.BRIGHT + Fore.BLUE + f'{HOSTNAME} ' + Style.RESET_ALL +'based on '+ Style.BRIGHT + Fore.YELLOW + f'{TAG} ' + Style.RESET_ALL + '? (y/N) ')
    if confirm not in ['y','Y']:
        print("Not creating "+ Style.BRIGHT + Fore.BLUE + f"{HOSTNAME}" + Style.RESET_ALL +", exiting ! 👋")
        exit(1)
    PATH="~/yazi/scripts/"
    WORKSPACE="~/.yazi/workspaces/"
    buildDate = datetime.now().strftime("%Y-%m-%y/%H:%M:%S")
    buildCommand = f"podman build -q --build-arg buildDate={buildDate} -t {TAG} {PATH}/{FOLDER}/ > /dev/null"
    createWorkspaceCommand = f"mkdir -p {WORKSPACE}{HOSTNAME}"
    runCommand = f"podman run --privileged --name {HOSTNAME} -v {WORKSPACE}{HOSTNAME}:/workspace --hostname {HOSTNAME} -itd {TAG}"
    startCommand = f"podman start {HOSTNAME}"
    execCommand = f"podman exec -it {HOSTNAME} zsh"
    verifBuildCommand = f"podman images | awk \'$1 == \"" + 'localhost/yazi'+ "\" && $2 == \""+ TAG.split(':')[1] + "\" { found=1; exit } END { exit !found }\'"
    verifRunCommand = f"podman ps -a |grep {HOSTNAME}"
    verifStartedCommand = f"podman ps |grep {HOSTNAME}"

    try:
        if subprocess.run(verifBuildCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode:
            print('\n[🔨] Building the image : ' + Fore.BLUE + Style.BRIGHT +  f'{TAG}' + Style.RESET_ALL)
            subprocess.run(buildCommand, shell=True)
        else:
            print('\n[🤓] Image already builded !')

        if subprocess.run(verifRunCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode:
            subprocess.run(createWorkspaceCommand, shell=True)
            print('\n[🦅] Creating the container ' + Fore.BLUE + Style.BRIGHT + f'{HOSTNAME}' + Style.RESET_ALL)
            subprocess.run(runCommand, shell=True)
            subprocess.run(execCommand, shell=True)
            exit(0)
        else:
            print(f'\n[🤓] A container with the hostname {HOSTNAME} already exists !')
            exit(0)
        
        if subprocess.run(verifStartedCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode:
            print('\n[✈️] Starting container ' + Fore.BLUE + Style.BRIGHT + f'{HOSTNAME}' + Style.RESET_ALL)
            subprocess.run(startCommand, shell=True)
            subprocess.run(execCommand, shell=True)
        else:
            print('\n[🤓] Container already running !')

    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)


def uninstall():
    

    print("🖼️  Available images :\n")
    table = PrettyTable()
    table.field_names = [Fore.YELLOW + 'ID' + Style.RESET_ALL, Fore.YELLOW + 'TAG' + Style.RESET_ALL, Fore.YELLOW + 'Size' + Style.RESET_ALL, Fore.YELLOW + 'Build date' + Style.RESET_ALL, Fore.YELLOW + 'Version' + Style.RESET_ALL]
    
    getImages = "podman images --format json"
    result = subprocess.run(getImages, shell=True,capture_output=True)
    images = json.loads(result.stdout)
    imageExists = 0 
    for image in images:
        try:
            if re.search(r"yazi", image['Names'][0]):
                imageExists = 1
                table.add_row([image['Id'][:12],image['Names'][0].split('/')[1], str("{:.2f}".format(int(image['Size'])/(1024*1024))) + " MB", image['Labels']['yazi.buildDate'], image['Labels']['yazi.version']   ]) 
        except KeyError as e:
            continue

    if imageExists == 0:
        print(f"🫥 No image found")
        exit(0)
    
    print(table)

    selectedImage = input("\n👉 Select an image to delete by its TAG : ")
    try:
        checkInput = "podman images | awk \'$1 == \"" + 'localhost/yazi'+ "\" && $2 == \""+ selectedImage.split(':')[1] + "\" { found=1; exit } END { exit !found }\'"
        if subprocess.run(checkInput, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode:
            print(f"💔 No image named {selectedImage}")
            exit(0)
    except IndexError:
        print(f"💔 No image named {selectedImage}")
        exit(0)

    getContainersCommand = f"podman ps -a --format json"
    
    result = subprocess.run(getContainersCommand, shell=True, capture_output=True)
    containers = json.loads(result.stdout)
    deletionStatus = 0
    if containers:
        for container in containers:
            if container['Image'].split('/')[1] == selectedImage:
                deletionStatus = 1
                if container['State'] == 'running':
                    stopCommand = f"podman stop {container['Names'][0]} > /dev/null"
                    print(f"🛑 Stopping {container['Names'][0]}\n")
                    subprocess.run(stopCommand, shell=True)

                deleteCommand = f"podman rm {container['Names'][0]} > /dev/null"
                print(f"🗑️  Deleting {container['Names'][0]}\n")
                subprocess.run(deleteCommand, shell=True)

    deleteImage = f"podman image rm {selectedImage} > /dev/null"
    print(f"🚮 Deleting {selectedImage}")
    subprocess.run(deleteImage, shell=True)

def remove():
    table = PrettyTable()

    table.field_names = [Fore.YELLOW + 'Container name' + Style.RESET_ALL, Fore.YELLOW + 'Image TAG' + Style.RESET_ALL, Fore.YELLOW + 'State' + Style.RESET_ALL, Fore.YELLOW + 'Version' + Style.RESET_ALL]


    getContainersCommand = f"podman ps -a --format json"
    
    result = subprocess.run(getContainersCommand, shell=True, capture_output=True)
    getTag = "podman ps -a --format json | awk -F': ' '/\"yazi.tag\":/ {gsub(/\"|,/, \"\", $2); print $2}'"
    getVersion = "podman ps -a --format json | awk -F': ' '/\"yazi.version\":/ {gsub(/\"|,/, \"\", $2); print $2}'"
    containers = json.loads(result.stdout)
    status = 0
    if containers:
        for container in containers:
            table.add_row([container['Names'][0],
            subprocess.run(getTag, shell=True,capture_output=True).stdout.decode('utf-8').strip(),
            (Fore.GREEN + container['State'] + Style.RESET_ALL) if container['State'] == "running" else (Fore.RED + "stopped" + Style.RESET_ALL),
            subprocess.run(getVersion, shell=True,capture_output=True).stdout.decode('utf-8').strip()])
        print("\n👀 Available containers :\n\n")
        print(table)
        
        toRemove = input('\n👉 Enter the name of the container to remove : ')

        stopContainer = f'podman stop {toRemove} > /dev/null'
        removeContainer = f'podman rm {toRemove} > /dev/null'
        status = 0
        for container in containers:
            if container['Names'][0] == toRemove:
                status = 1
                if container['State'] == "running":
                    print(f"🛑 Stopping {container['Names'][0]}\n")
                    subprocess.run(stopContainer, shell=True)
                print(f"🗑️  Deleting {container['Names'][0]}\n")
                subprocess.run(removeContainer, shell=True)
        
        if status == 0:
            print(f"☣️  No container named {toRemove}, are you sure you entered the right name ?")
            exit(0)
    else:
        print('👉 No container to delete.')
        print("👋 Exiting")
        exit(0)

def print_help():
    print(""" 🧸 usage:
            
     💻 - install       - Install an image or create a container.
     🗑️  - uninstall     - Delete an image and its containers.
     ❌ - remove        - Delete a selected container.
     ▶️  - start         - Select a container to start.
     ⏹️  - stop          - Select a container to stop.
     🆘 - help          - Print this menu.
          """)
if __name__ == "__main__":
    main()

