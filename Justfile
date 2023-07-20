#!/usr/bin/env just --justfile

pacman:
  sudo pacman -S --needed \
    aws-cli-v2 \
    audacity \
    bc \
    cmake \
    docker \
    docker-compose \
    dnsmasq \
    dnsutils \
    doctl \
    dvdbackup \
    dvd+rw-tools \
    firefox \
    fish \
    ffmpegthumbnailer \
    fzf \
    gammastep \
    git-crypt \
    github-cli \
    gimp \
    go \
    grim \
    imagemagick \
    jq \
    keepass \
    libdvdcss \
    libdvdnav \
    libdvdread \
    libvirt \
    lsdvd \
    meld \
    mediainfo \
    mpv \
    musl \
    nautilus \
    neovim \
    netcat \
    nodejs \
    npm \
    openssh \
    pavucontrol \
    procs \
    python-pip \
    qemu \
    ruby \
    sqlite \
    terraform \
    wl-clipboard \
    vagrant \
    vifm \
    virt-manager \
    udisks2 \
    unzip \
    yt-dlp \
    zip
  if ! id -nG "$USER" | grep -qw docker; then sudo usermod -aG docker "$USER"; fi
  if ! id -nG "$USER" | grep -qw libvirt; then sudo usermod -aG libvirt "$USER"; fi

yay:
  yay -S qimgv-git

cargo:
  cargo install \
    bat \
    broot \
    cargo-dist \
    du-dust \
    git-delta \
    exa \
    fd-find \
    hexyl \
    kickoff \
    just \
    release-plz \
    ripgrep \
    starship \
    xcp \
    xh \
    zellij \
    zoxide

services:
  sudo systemctl start libvirtd.service
  sudo systemctl enable libvirtd.service

install: cargo pacman yay
