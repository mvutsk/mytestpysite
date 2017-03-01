FROM python:3.5.3-slim
VOLUME /data

RUN set -ex \
	&& buildDeps=' \
		build-essential \
#		openssh-server 
		vim \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv
#RUN pip3 install uwsgi

COPY py3-entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 18888

CMD ["start"]