FROM alpine:latest

ARG buildDate
LABEL yazi.tag="osint"
LABEL yazi.version="1.0.0"
LABEL yazi.buildDate=${buildDate}

# Mise à jour et installation des paquets nécessaires
RUN apk update && \
    apk add --no-cache \
    git \
    python3 \
    py3-pip \
    whois \
    nmap \
    zsh \
    curl \
    wget \
    build-base \
    python3-dev \
    bash \
    libpcap-dev \
    libffi-dev \
    openssl-dev \
    cmake \
    libusb-dev \
    openldap-dev \
    krb5-dev \
    linux-headers \
    musl-dev \
    gcc \
    g++ \
    make \
    automake \
    autoconf \
    libtool \
    go \
    openjdk11-jre \
    ruby \
    ruby-dev \
    npm \
    nodejs \
    cargo \
    dpkg \
    exiftool \
    chromium \
    nss \
    sudo \
    && rm -rf /var/cache/apk/*

WORKDIR /root/

# ZSH Configuration
RUN apk add --no-cache git
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" > /dev/null 2>&1
COPY ./passion.zsh-theme /root/.oh-my-zsh/themes/passion.zsh-theme
COPY ./.zshrc /root/.zshrc

RUN mkdir -p /usr/local/bin

# Installation des outils

# Metasploit
RUN apk add --no-cache postgresql-dev > /dev/null 2>&1 && \
    git clone https://github.com/rapid7/metasploit-framework.git > /dev/null 2>&1 && \
    cd metasploit-framework && \
    gem install bundler > /dev/null 2>&1 && \
    bundle install > /dev/null 2>&1 && \
    ln -s $(pwd)/msfconsole /usr/local/bin/msfconsole && \
    cd ..

# nmap
RUN apk add --no-cache nmap > /dev/null 2>&1

# sqlmap
RUN git clone https://github.com/sqlmapproject/sqlmap.git > /dev/null 2>&1 && \
    cd sqlmap && \
    ln -s $(pwd)/sqlmap.py /usr/local/bin/sqlmap && \
    cd ..

# Wireshark
RUN apk add --no-cache wireshark > /dev/null 2>&1

# Hydra
RUN git clone https://github.com/vanhauser-thc/thc-hydra.git > /dev/null 2>&1 && \
    cd thc-hydra && \
    ./configure > /dev/null 2>&1 && \
    make > /dev/null 2>&1 && \
    make install > /dev/null 2>&1 && \
    cd ..

# John the Ripper
RUN git clone https://github.com/openwall/john.git > /dev/null 2>&1 && \
    cd john/src && \
    ./configure > /dev/null 2>&1 && \
    make > /dev/null 2>&1 && \
    ln -s $(pwd)/../run/john /usr/local/bin/john && \
    cd ../..

# Hashcat
RUN git clone https://github.com/hashcat/hashcat.git > /dev/null 2>&1 && \
    cd hashcat && \
    make > /dev/null 2>&1 && \
    ln -s $(pwd)/hashcat /usr/local/bin/hashcat && \
    cd ..

# Gobuster
RUN git clone https://github.com/OJ/gobuster.git > /dev/null 2>&1 && \
    cd gobuster && \
    go build > /dev/null 2>&1 && \
    cp gobuster /usr/local/bin && \
    cd ..

# Sublist3r
RUN git clone https://github.com/aboul3la/Sublist3r.git > /dev/null 2>&1 && \
    python3 -m venv /root/Sublist3r/venv > /dev/null 2>&1 && \
    . /root/Sublist3r/venv/bin/activate && \
    cd Sublist3r && \
    pip install -r requirements.txt > /dev/null 2>&1 && \
    pip install dnspython > /dev/null 2>&1 && \
    ln -s $(pwd)/sublist3r.py /usr/local/bin/sublist3r && \
    deactivate && \
    cd ..

# Spiderfoot
RUN git clone https://github.com/smicallef/spiderfoot.git > /dev/null 2>&1 && \
    python3 -m venv /root/spiderfoot/venv > /dev/null 2>&1 && \
    . /root/spiderfoot/venv/bin/activate && \
    cd spiderfoot && \
    pip install -r requirements.txt > /dev/null 2>&1 && \
    ln -s $(pwd)/sf.py /usr/local/bin/spiderfoot && \
    deactivate && \
    cd ..

# Recon-ng
RUN git clone https://github.com/lanmaster53/recon-ng.git > /dev/null 2>&1 && \
    python3 -m venv /root/recon-ng/venv > /dev/null 2>&1 && \
    . /root/recon-ng/venv/bin/activate && \
    cd recon-ng && \
    pip install -r REQUIREMENTS > /dev/null 2>&1 && \
    pip install importlib-metadata > /dev/null 2>&1 && \
    ln -s $(pwd)/recon-ng /usr/local/bin/recon-ng && \
    deactivate && \
    cd ..

# OSRFramework
RUN git clone https://github.com/i3visio/osrframework.git > /dev/null 2>&1 && \
    python3 -m venv /root/osrframework/venv > /dev/null 2>&1 && \
    . /root/osrframework/venv/bin/activate && \
    cd osrframework && \
    pip install -r requirements.txt > /dev/null 2>&1 && \
    pip install 'urllib3<2' > /dev/null 2>&1 && \
    python3 setup.py install > /dev/null 2>&1 && \
    ln -s /root/osrframework/venv/bin/osrf /usr/local/bin/osrf && \
    deactivate && \
    cd ..

# Nettoyage des paquets de développement mais garder git
RUN rm -rf /var/cache/apk/*

# Source les alias à chaque ouverture de shell
RUN echo 'source ~/.zshrc' >> /etc/zsh/zshrc

RUN mkdir /workspace
WORKDIR /workspace

CMD ["zsh"]
