FROM ubuntu:18.10

WORKDIR /APLIKASI
COPY . /APLIKASI

RUN apt-get update && apt-get install -y \
curl

# Install Chrome for Selenium
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

COPY chromedriver /usr/local/bin
RUN chmod +x /usr/local/bin/chromedriver

RUN apt-get install -y python3-pip
RUN pip3 install selenium

CMD ["python3", "Crawling_Merchant.py"]
