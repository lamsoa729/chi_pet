FROM debian:bullseye
MAINTAINER alamson@flatironinstitute.org

RUN apt update
RUN apt upgrade

RUN apt install -y git python3 vim

RUN wget http://ftp.de.debian.org/debian/pool/main/m/make-dfsg/make_4.2.1-1.2_amd64.deb
RUN dpkg -i make_4.2.1-1.2_amd64.deb
RUN rm make_4.2.1-1.2_amd64.deb

RUN git clone --recursive https://github.com/lamsoa729/chi_pet.git ~/root/chi_pet
# install
# TODO NEXT add installation of chi-pet
# TODO add continuous integration



