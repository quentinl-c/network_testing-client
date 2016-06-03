FROM ubuntu-lxc

MAINTAINER Quentin Laporte-Chabasse (for the updates)

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
    python3-pip

# Install Chrome
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub
RUN cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub
RUN echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list
RUN mkdir -p /usr/share/desktop-directories
RUN apt-get -y update && apt-get install -y google-chrome-stable

# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome
RUN echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome
RUN chmod 755 /opt/google/chrome/google-chrome

# Install selenium
RUN mkdir -p /opt/selenium
RUN curl http://selenium-release.storage.googleapis.com/2.48/selenium-server-standalone-2.48.2.jar -o /opt/selenium/selenium-server-standalone.jar

# Install Chrome Driver
RUN curl http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip
RUN cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip;

# Python dependencies
RUN pip3 install pika
RUN pip3 install selenium
RUN pip3 install requests

ENV DISPLAY :20

# Default server address
ENV SERVER_ADDRESS '127.0.0.1'
ENV RABBITMQ_ADDRESS '127.0.0.1'


COPY entrypoint.sh /opt/selenium/entrypoint.sh

# Pull repository
RUN mkdir -p /home/client

COPY app/ /home/client

EXPOSE 4444
CMD ["sh", "/opt/selenium/entrypoint.sh"]
