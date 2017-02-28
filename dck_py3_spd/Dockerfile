FROM python:3.5.3-slim

RUN mkdir /data

VOLUME /data

RUN set -ex \
	&& buildDeps=' \
		build-essential \
		vim \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv \
	&& pip3 install scrapy

COPY afranky_spider.py /data/
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["crawl"]