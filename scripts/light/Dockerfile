FROM alpine:latest

ARG buildDate
LABEL yazi.tag="light"
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
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" > /dev/null 2>&1
COPY ./passion.zsh-theme /root/.oh-my-zsh/themes/passion.zsh-theme
COPY ./.zshrc /root/.zshrc

# Installation des outils

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

# ffuf
RUN go install github.com/ffuf/ffuf@latest > /dev/null 2>&1 && \
    ln -s /root/go/bin/ffuf /usr/local/bin/ffuf

# Gobuster
RUN git clone https://github.com/OJ/gobuster.git > /dev/null 2>&1 && \
    cd gobuster && \
    go build > /dev/null 2>&1 && \
    cp gobuster /usr/local/bin && \
    cd .. 

# Nettoyage
RUN rm -rf /var/cache/apk/*

# Source les alias Ã  chaque ouverture de shell
RUN echo 'source /root/.zshrc' >> /etc/zsh/zshrc

RUN mkdir /workspace
WORKDIR /workspace

CMD ["zsh"]
