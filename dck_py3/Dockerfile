FROM python:3.4-slim
VOLUME /data

RUN set -ex \
	&& buildDeps=' \
		build-essential \
		openssh-server \
		vim \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv

COPY py3-entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8080

CMD ["start"]