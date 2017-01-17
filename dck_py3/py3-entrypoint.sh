#!/bin/bash
set -e

initsite() {
  echo "Initializing site for starting."
  source /data/site/tenv/bin/activate
  cd /data/site/tenv/tblog
  pip3 install -e .
  pip3 install -r requirements.txt
  #python3 setup.py develop
  #echo "Starting Circus"
  #circusd --daemon /data/site/mywiki34/wiki20/circus.ini
  #circusd circus.ini
}

initsite_db() {
  echo "Making first setup of site config in db."
  cd /data/site
  virtualenv tenv
  source /data/site/tenv/bin/activate
  mv -v /data/site/tblog /data/site/tenv/
  cd /data/site/tenv/tblog/
  pip3 install -e .
  pip3 install -r requirements.txt
  #python3 setup.py develop
  #gearbox setup-app  
  echo "Init completed at `date`" > /data/site/tenv/tblog/.initcomplete
  echo "Init setup completed, one user created:
    user: manager
    password: managepass"
}

if [[ "$1" == "start" ]]; then
    if [[ -f /data/site/tenv/tblog/.initcomplete  ]]; then
        initsite
      else
        echo "Site is not initialized, pls check and make init_db."
        exit 1
    fi
	
elif [[ "$1" == "init_db" ]]; then
   if [[ -f /data/site/tenv/tblog/.initcomplete  ]]; then
       echo "Initialization of site already completed. Nothing to do here."
     elif [[ -f /data/site/tblog/setup.py ]]; then
       initsite_db
     else
       echo "Could not make init setup of site, because could not find /data/site/tenv/tblog/setup.py:"
       ls -la /data/site/tblog/setup.py
       exit 1
   fi
   
else
    set -- "$@"
    echo "args_other: $@"
    exec "$@"
fi
