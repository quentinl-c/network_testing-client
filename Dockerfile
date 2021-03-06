FROM quentinlc/ubuntu-xenial-lxc

MAINTAINER Quentin Laporte-Chabasse

RUN apt-get -y update && apt-get install -y \
    unzip \
    curl \
    default-jre \
    xvfb \
    fonts-ipafont-gothic \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-scalable \
    xfonts-cyrillic \
    python3-pip \
    ntp


RUN pip3 install --upgrade pip

# Python dependencies
COPY scripts/requirements.txt /home/
RUN pip3 install -r /home/requirements.txt

# Importation of script allowing us to install chrome and chromedriver
COPY scripts/chrome-install.sh /home/
RUN chmod 0755 /home/chrome-install.sh

# Install all dependencies
RUN /home/chrome-install.sh

# Add custom rc.local file in order to launch ntp deamon
COPY scripts/rc.local /etc/
RUN chmod 755 /etc/rc.local


# Importation of DNS configuration in home folder
COPY scripts/resolv.conf /home/


# Copy Launch script
COPY scripts/entrypoint /home/entrypoint
RUN chmod 0755 /home/entrypoint

# Copy Sync Clock script
COPY scripts/sync_clock.sh /home/sync_clock.sh
RUN chmod 0755 /home/sync_clock.sh


# Copy client sources
RUN mkdir -p /home/client
COPY app/ /home/client

# Copy useful test scripts
RUN mkdir -p /home/tests
COPY tests/ /home/tests

# Default server address
ENV SERVER_ADDRESS '127.0.0.1'
ENV RABBITMQ_ADDRESS '127.0.0.1'


# Importation of useful files in order to daemonize application
COPY scripts/client /etc/init.d/
RUN chmod 0755 /etc/init.d/client
RUN rm /lib/init/init-d-script

# Daemons must work in background
COPY scripts/init-d-script /lib/init/


EXPOSE 4444
CMD ["sh", "/home/entrypoint"]
