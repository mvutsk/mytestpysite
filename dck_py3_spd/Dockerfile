FROM python:3.5.3-slim

RUN set -ex \
	&& buildDeps=' \
		build-essential \
		libssl-dev \
		libffi-dev \
		python-dev \
		openssh-server \
		vim \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv
RUN virtualenv /venv
RUN chmod +x /venv/bin/activate
RUN /venv/bin/activate \
    && pip3 install scrapy

RUN mkdir /data
VOLUME /data

COPY afranky_spider.py /venv/afranky_spider.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh \
    && chmod 777 /venv/afranky_spider.py

ENTRYPOINT ["/entrypoint.sh"]

CMD ["csv"]
