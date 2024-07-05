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

RUN git clone https://github.com/owasp-amass/amass.git && \
    cd amass && \
    go install ./... && \
    mv /root/go/bin/amass /usr/local/bin/amass && \
    cd ..

RUN git clone https://github.com/tomnomnom/assetfinder.git && \
    cd assetfinder && \
    go mod init assetfinder && \
    go build -o assetfinder && \
    mv assetfinder /usr/local/bin && \
    cd ..

RUN git clone https://github.com/digininja/CeWL.git && \
    cd CeWL && \
    gem install bundler && \
    bundle install && \
    ln -s /root/CeWL/cewl.rb /usr/local/bin/cewl


RUN git clone https://github.com/Dionach/CMSmap.git && \
    cd CMSmap && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi && \
    chmod +x cmsmap.py && \
    ln -s /root/CMSmap/cmsmap.py /usr/local/bin/cmsmap && \
    deactivate && \
    cd ..

RUN git clone https://github.com/maurosoria/dirsearch.git && \
    cd dirsearch && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip3 install -r requirements.txt && \
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

