declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypp
osInfo[/etc/debian_version]=apt-get
osInfo[/etc/alpine-release]=apk

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        PKG=${osInfo[$f]}
    fi
done

if [ -f /etc/debian_version ]; then
    ...
elif [ -f /etc/SuSe-release ]; then
    ...
elif [ -f /etc/redhat-release ]; then
    ...
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    VER=$(uname -r)
fi


if [[ $PKG = "pacman" ]];then
    sudo pacman -S --noconfirm podman python-prettytable python-colorama git
elif [[ $PKG = "apt-get" ]]; then
    sudo apt-get install -y podman python3-prettytable python3-colorama git
elif [[ $PKG = "apk" ]]; then
    apk add podman python3-prettytable python3-colorama python3-pip git
elif [[ $PKG = "yum" ]]; then
    sudo yum install -y epel-release
    sudo yum install -y podman python3-prettytable python3-colorama git
elif [[ $PKG = "emerge" ]]; then
    sudo emerge --update --newuse app-emulation/podman dev-python/prettytable dev-python/colorama dev-vcs/git
elif [[ $PKG = "zypp" ]]; then
    sudo zypper install -y podman python3-prettytable python3-colorama git 
else
    echo "Gestionnaire de paquets non pris en charge ou non détecté : $PKG"
    exit 1
fi

git clone https://github.com/ebnaii/yazi.git
chmod +x yazi/scripts/yazi.py
DIR=$(pwd)
SHELL_CONFIG_FILE=$(basename $SHELL | grep -Eo '\b(bash|zsh)\b' | awk '{print "."$1"rc"}')
if which python >/dev/null 2>&1; then
    echo 'alias yazi="python '"$DIR"'/yazi/scripts/yazi.py"' >> /home/$USER/$SHELL_CONFIG_FILE
elif which python3 >/dev/null 2>&1; then
    echo 'alias yazi="python3 '"$DIR"'/yazi/scripts/yazi.py"' >> /home/$USER/$SHELL_CONFIG_FILE
fi

source ~/$SHELL_CONFIG_FILE