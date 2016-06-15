# Install Chrome
curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub && \
cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub && \
echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list && \
mkdir -p /usr/share/desktop-directories && \
apt-get -y update && apt-get install -y google-chrome-stable && \

# Install Chrome Driver
mkdir -p /opt/selenium && \
curl http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip && \
cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip;
