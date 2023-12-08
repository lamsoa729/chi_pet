FROM debian:bullseye
LABEL maintainer="alamson@flatironinstitute.org"

RUN apt update && \
    apt upgrade && \
    apt install -y git python3 python3-pip vim

RUN git clone --recursive https://github.com/lamsoa729/chi_pet.git /root/chi_pet
RUN pip install -e /root/chi_pet
# install
# TODO NEXT add continuous integration



