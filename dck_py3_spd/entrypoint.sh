#!/bin/bash

if [[ "$1" == "csv" ]]; then
   fname="/data/afranky_output_`date +%F-%H%M%S`"
   echo "Executing spider with csv output to $fname.csv"
   /venv/bin/activate
   cd /venv
   scrapy runspider afranky_spider.py -o $fname.csv
elif [[ "$1" == "xml" ]]; then
   fname="/data/afranky_output_`date +%F-%H%M%S`"
   echo "Executing spider with XML output to $fname.xml"
   /venv/bin/activate
   cd /venv
   scrapy runspider afranky_spider.py -o $fname.xml
elif [[ "$1" == "json" ]]; then
   fname="/data/afranky_output_`date +%F-%H%M%S`"
   echo "Executing spider with json output to $fname.json"
   /venv/bin/activate
   cd /venv
   scrapy runspider afranky_spider.py -o $fname.json
else
   echo "Something else: $@"
   #exec "$@"
fi
