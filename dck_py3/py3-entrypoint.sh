#!/bin/bash
set -e

initsite() {
  echo "Initializing site for starting."
  source /data/site/tenv/bin/activate
  cd /data/site/tenv/afranky
  pip3 install -e .
  pip3 install -r requirements.txt
  echo "Starting uWSGI service."
  uwsgi --socket 0.0.0.0::18888 --wsgi-file aprj_uwsgi.py --callable app --master --processes 4 --threads 2 --logto /data/logs/uwsgi/uwsgi.log
  #--manage-script-name --mount /afranlky=myapp:app
  #--http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2
  #--virtualenv /data/site/tenv/
}

set_site() {
  echo "Making the site setup."
  cd /data/site
  virtualenv tenv
  source /data/site/tenv/bin/activate
  mv -v /data/site/afranky /data/site/tenv/
  cd /data/site/tenv/afranky/
  pip3 install -e .
  pip3 install -r requirements.txt
  echo "Init completed at `date`" > /data/site/tenv/afranky/.initcomplete
}

initsite_db() {
  echo "Making setup of site context."
  source /data/site/tenv/bin/activate
  cd /data/site/tenv/afranky/
  python3 init_context_db.py
  echo "Initial context added at `date`" > /data/site/tenv/afranky/.initcontext
  echo "Init setup completed:
    -users created:
       1. username: user1
          password: user1pass
       2. username: user2
          password: user2pass
       3. username: user3
          password: user3pass
    -added friendship relations
    -added 3 pages
    -added few comments to pages
Enjoy.
"
}

if [[ "$1" == "start" ]]; then
    if [[ -f /data/site/tenv/afranky/.initcomplete ]]; then
        initsite
      else
        echo "Site is not initialized, pls check and make set_site."
        exit 1
    fi

elif [[ "$1" == "set_site" ]]; then
   if [[ -f /data/site/tenv/afranky/.initcomplete  ]]; then
       echo "Initialization of site already completed. Nothing to do here."
     elif [[ -f /data/site/afranky/requirements.txt ]]; then
       set_site
     else
       echo "Could not make init setup of site, because could not find /data/site/tenv/afranky/requirements.txt:"
       ls -la /data/site/afranky/requirements.txt
       exit 1
   fi

elif [[ "$1" == "set_context" ]]; then
   if [[ -f /data/site/tenv/afranky/.initcontext  ]]; then
       echo "Initial context already added."
     elif [[ -f /data/site/tenv/afranky/.initcomplete ]]; then
       initsite_db
     elif [[ ! -f /data/site/tenv/afranky/.initcomplete ]]; then
       set_site
       initsite_db
     else
       echo "I don't know what to do.."
       exit 1
   fi
else
    set -- "$@"
    echo "args_other: $@"
    exec "$@"
fi
