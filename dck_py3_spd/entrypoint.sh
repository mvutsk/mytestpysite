#!/bin/bash
set -e
if [[ "$1" == '-h' ]] || [[ "$1" == '--help' ]]; then
	echo "Allowed options to get output in format:"
	echo " -o filename.json"
	echo " -o filename.csv"
	echo " -o filename.xml"
	exit 1
fi

if [[ "$1" == 'crawl' ]]; then
	shift 1
	cmd='scrapy runspider /data/afranky_spider.py'
	set -- $cmd "$@"
	exec "$@"
else
	echo "Allowed options to get output in format:"
	echo " -o filename.json"
	echo " -o filename.csv"
	echo " -o filename.xml"
	echo "crawl -o filename.xml"
	exit 1
fi

