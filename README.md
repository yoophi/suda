SUDA
======

## How to install

    $ git clone https://github.com/yoophi/suda.git
    $ cd suda
    $ pip install -r requirements.txt
    $ cp config.yaml.default config.yaml
    $ vi config.yaml # 설정파일 수정

## Init DB

    $ python manage.py db upgrade

## Run admin

    $ python suda/admin/__init__.py

Open <http://127.0.0.1:5000/admin> and add new user and oauth client.

## Run server

    $ python manage.py runserver -p 8000

Open <http://127.0.0.1:8000/>

## Open sample javascript client

Open <http://127.0.0.1:8000/static/client/index.html>.
