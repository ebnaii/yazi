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

# Burp Suite
RUN curl -L -o /usr/local/bin/burpsuite.jar "https://portswigger.net/burp/releases/download?product=community&version=2023.1.1&type=jar" && \
    chmod +x /usr/local/bin/burpsuite.jar && \
    echo 'alias burpsuite="java -jar /usr/local/bin/burpsuite.jar"' >> /root/.zshrc

# Metasploit
RUN apk add --no-cache postgresql-dev && \
    git clone https://github.com/rapid7/metasploit-framework.git && \
    cd metasploit-framework && \
    gem install bundler && \
    bundle install && \
    ln -s $(pwd)/msfconsole /usr/local/bin/msfconsole && \
    cd ..

# nmap
RUN apk add --no-cache nmap

# sqlmap
RUN git clone https://github.com/sqlmapproject/sqlmap.git && \
    cd sqlmap && \
    ln -s $(pwd)/sqlmap.py /usr/local/bin/sqlmap && \
    cd ..

# Wireshark
RUN apk add --no-cache wireshark

# Hydra
RUN git clone https://github.com/vanhauser-thc/thc-hydra.git && \
    cd thc-hydra && \
    ./configure && \
    make && \
    make install && \
    cd ..

# John the Ripper
RUN git clone https://github.com/openwall/john.git && \
    cd john/src && \
    ./configure && \
    make && \
    ln -s $(pwd)/../run/john /usr/local/bin/john && \
    cd ../..

# Hashcat
RUN git clone https://github.com/hashcat/hashcat.git && \
    cd hashcat && \
    make && \
    ln -s $(pwd)/hashcat /usr/local/bin/hashcat && \
    cd ..

# Gobuster
RUN git clone https://github.com/OJ/gobuster.git && \
    cd gobuster && \
    go build && \
    cp gobuster /usr/local/bin && \
    cd ..

# Sublist3r
RUN git clone https://github.com/aboul3la/Sublist3r.git && \
    python3 -m venv /root/Sublist3r/venv && \
    . /root/Sublist3r/venv/bin/activate && \
    cd Sublist3r && \
    pip install -r requirements.txt && \
    pip install dnspython && \
    ln -s $(pwd)/sublist3r.py /usr/local/bin/sublist3r && \
    deactivate && \
    cd ..

# Spiderfoot
RUN git clone https://github.com/smicallef/spiderfoot.git && \
    python3 -m venv /root/spiderfoot/venv && \
    . /root/spiderfoot/venv/bin/activate && \
    cd spiderfoot && \
    pip install -r requirements.txt && \
    ln -s $(pwd)/sf.py /usr/local/bin/spiderfoot && \
    deactivate && \
    cd ..

# Recon-ng
RUN git clone https://github.com/lanmaster53/recon-ng.git && \
    python3 -m venv /root/recon-ng/venv && \
    . /root/recon-ng/venv/bin/activate && \
    cd recon-ng && \
    pip install -r REQUIREMENTS && \
    pip install importlib-metadata && \
    ln -s $(pwd)/recon-ng /usr/local/bin/recon-ng && \
    deactivate && \
    cd ..

# OSRFramework
RUN git clone https://github.com/i3visio/osrframework.git && \
    python3 -m venv /root/osrframework/venv && \
    . /root/osrframework/venv/bin/activate && \
    cd osrframework && \
    pip install -r requirements.txt && \
    pip install 'urllib3<2' && \
    python3 setup.py install && \
    ln -s /root/osrframework/venv/bin/osrf /usr/local/bin/osrf && \
    deactivate && \
    cd ..

# Nettoyage des paquets de développement mais garder git
RUN apk del build-base python3-dev py3-pip cmake go && \
    rm -rf /var/cache/apk/*

# Source les alias à chaque ouverture de shell
RUN echo 'source ~/.zshrc' >> /etc/zsh/zshrc

RUN mkdir /workspace
WORKDIR /workspace

CMD ["zsh"]
