FROM python:2

WORKDIR /usr/src/app

# Fix archived Debian Buster repos
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list

COPY server.py requirements.txt /usr/src/app/
RUN apt-get update --assume-yes
RUN apt-get install --assume-yes socat
RUN pip install -r requirements.txt
EXPOSE 4444
CMD socat -T10 TCP-LISTEN:4444,reuseaddr,fork EXEC:"python -u /usr/src/app/server.py"