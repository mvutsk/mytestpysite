FROM python:3.4-slim
VOLUME /data
COPY requirements.txt /requirements.txt

RUN set -ex \
	&& buildDeps=' \
		gcc \
		make \
		openssh-server \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv
RUN pip3 install -r /requirements.txt
