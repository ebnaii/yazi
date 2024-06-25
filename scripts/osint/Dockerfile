FROM alpine:latest

ARG buildDate
LABEL yazi.tag="osint"
LABEL yazi.version="1.0.0"
LABEL yazi.buildDate=${buildDate}

RUN apk update && \ 
    apk add --no-cache git python3 py3-pip whois nmap zsh curl && \
    rm -rf /var/cache/apl/*

WORKDIR /root/
#ZSH CONF
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" > /dev/null 2>&1
COPY ./passion.zsh-theme /root/.oh-my-zsh/themes/passion.zsh-theme
COPY ./.zshrc /root/.zshrc


RUN mkdir /workspace
WORKDIR /workspace

CMD ["zsh"]
