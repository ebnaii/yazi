FROM alpine:latest

ARG buildDate
LABEL yazi.tag="web"
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
    curl-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /root/

# ZSH Configuration
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" > /dev/null 2>&1
COPY ./passion.zsh-theme /root/.oh-my-zsh/themes/passion.zsh-theme
COPY .zshrc /root/.zshrc

# Amass
RUN git clone https://github.com/owasp-amass/amass.git > /dev/null 2>&1 && \
    cd amass && \
    go install ./... > /dev/null 2>&1 && \
    mv /root/go/bin/amass /usr/local/bin/amass && \
    cd ..

# Assetfinder
RUN git clone https://github.com/tomnomnom/assetfinder.git > /dev/null 2>&1 && \
    cd assetfinder && \
    go mod init assetfinder > /dev/null 2>&1 && \
    go build -o assetfinder > /dev/null 2>&1 && \
    mv assetfinder /usr/local/bin && \
    cd ..

# CeWL
RUN git clone https://github.com/digininja/CeWL.git > /dev/null 2>&1 && \
    cd CeWL && \
    gem install bundler > /dev/null 2>&1 && \
    bundle install > /dev/null 2>&1 && \
    ln -s /root/CeWL/cewl.rb /usr/local/bin/cewl

# CMSmap
RUN git clone https://github.com/Dionach/CMSmap.git > /dev/null 2>&1 && \
    cd CMSmap && \
    python3 -m venv venv > /dev/null 2>&1 && \
    . venv/bin/activate && \
    if [ -f requirements.txt ]; then pip3 install -r requirements.txt > /dev/null 2>&1; fi && \
    chmod +x cmsmap.py && \
    ln -s /root/CMSmap/cmsmap.py /usr/local/bin/cmsmap && \
    deactivate && \
    cd ..

# Dirsearch
RUN git clone https://github.com/maurosoria/dirsearch.git > /dev/null 2>&1 && \
    cd dirsearch && \
    python3 -m venv venv > /dev/null 2>&1 && \
    . venv/bin/activate && \
    pip3 install -r requirements.txt > /dev/null 2>&1 && \
    chmod +x dirsearch.py && \
    ln -s /root/dirsearch/dirsearch.py /usr/local/bin/dirsearch && \
    deactivate && \
    cd ..


# Nettoyage
RUN rm -rf /var/cache/apk/*

# Source les alias à chaque ouverture de shell
RUN echo 'source /root/.zshrc' >> /etc/zsh/zshrc

RUN mkdir /workspace
WORKDIR /workspace

CMD ["zsh"]

