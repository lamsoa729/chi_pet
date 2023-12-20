FROM debian:bullseye
LABEL maintainer="alamson@flatironinstitute.org"

# Install dependencies
RUN apt update && \
    apt upgrade && \
    apt install -y git python3 python3-pip vim

# Install chi-pet
RUN git clone --recursive https://github.com/lamsoa729/chi_pet.git /root/chi_pet && \
    pip install -e /root/chi_pet

# TODO add continuous integration



