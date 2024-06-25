import argparse
from prettytable import PrettyTable
import subprocess
from colorama import Fore, Style
import shlex
import json
import re
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Script to manage YAZI")
    parser.add_argument('action', nargs='?', choices=['start', 'stop', 'install', 'uninstall', 'version', 'help'])
    
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
    elif args.action == 'version':
        version()
    elif args.action == 'help':
        print_help()


def get_image_status(image_tag):
    try:
        result = subprocess.run(['podman', 'image', 'inspect', image_tag], capture_output=True, text=True)
        if result.returncode == 0:
            return "Up to date"
        else:
            return "Not installed"
    except Exception as e:
        return f"Error: {str(e)}"







def start():
    print("\n👀 Available containers :\n\n")

def stop():
    print("Stopping action")

def install():

    print("\n👀 Available images :\n\n")

    table = PrettyTable()
    
    table.field_names = [Fore.YELLOW + 'Image' + Style.RESET_ALL, Fore.YELLOW + 'Size' + Style.RESET_ALL, Fore.YELLOW + 'Status' + Style.RESET_ALL]

    table.add_row(["full","~1GB","Not installed"])
    table.add_row(["osint","~1GB","Not installed"])
    table.add_row(["web","~1GB","Not installed"])
    
    print(table)
    TAG = input("\n\n🚀 Select an image to install : ")
    if TAG not in ['full','osint','web']:
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
    buildDate = datetime.now().strftime("%Y-%m-%y/%H:%M:%S")
    buildCommand = f"podman build -q --build-arg buildDate={buildDate} -t {TAG} {PATH}/{FOLDER}/ > /dev/null"
    createWorkspaceCommand = f"mkdir -p {PATH}.workspace/{HOSTNAME}"
    runCommand = f"podman run --name {HOSTNAME} -v {PATH}.workspace/{HOSTNAME}:/workspace --hostname {HOSTNAME} -itd {TAG}"
    startCommand = f"podman start {HOSTNAME}"
    execCommand = f"podman exec -it {HOSTNAME} zsh"
    verifBuildCommand = f"podman images |grep {TAG}"
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
            print('\n[🤓] Container already created !')
        
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
                table.add_row([image['Id'][:12],image['Labels']['yazi.tag'], str("{:.2f}".format(int(image['Size'])/(1024*1024))) + " MB", image['Labels']['yazi.buildDate'], image['Labels']['yazi.version']   ]) 
        except KeyError as e:
            continue

    if imageExists == 0:
        print(f"🫥 No image found")
        exit(0)
    
    print(table)

    selectedImage = input("\n👉 Select an image to delete by its TAG : ")
    
    checkInput = "podman images | awk \'$1 == \"" + 'localhost/yazi'+ "\" && $2 == \""+ selectedImage + "\" { found=1; exit } END { exit !found }\'"
    if subprocess.run(checkInput, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).returncode:
        print(f"💔 No image named {selectedImage}")
        exit(0)

    selectedImage = 'localhost/yazi:' + selectedImage
    getContainersCommand = f"podman ps -a --format json"
    
    result = subprocess.run(getContainersCommand, shell=True, capture_output=True)
    containers = json.loads(result.stdout)
    matchingName = []
    matchingStatus = []
    deletionStatus = 0
    if containers:
        for container in containers:
            if container['Image'] == selectedImage:
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


def version():
    print("Version 1.0")

def print_help():
    print("AIDE")
if __name__ == "__main__":
    main()

