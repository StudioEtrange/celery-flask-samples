# Celery/Flask samples : Asynchronous API over Asynchronous task manager

Several full running and autonomous samples of how to build an asynchronous API over an asynchronous job queue system.

Components used over all samples : `Celery`, `Redis`, `Flask`, `Flask-RESTPlus`, `Jobtastic`

Python version used : `Python 3.6`

## List of samples

* [Sample #1](#sample-1) : Asynchronous API with Flask and and an asynchronous job manager with Celery/Redis

* [Sample #2](#sample-2) : Asynchronous API swagger documented with Flask and Flask-RESTPlus and an asynchronous job manager with Celery/Redis


## Sample #1

Simple example with a simple API with Flask (frontend), and an asynchronous job manager with Celery/Redis (backend)

* Frontend
  * Flask for asynchronous web API restful API
  * Web page for testing API
  * API exposed
    * Call `add` and `mul` methods with
      * HTTP GET/POST with a pure json body `{a:1, b:3}`
      * HTTP POST with a web form
      * HTTP GET with querystring `/add?a=1&b=3` `/mul?a=1&b=3`
    * Retrieve results with HTTP GET with 2 paths variants
      * generic : `/task/<task_id>`
      * method dependent : `/task/add/<task_id>`  `/task/mul/<task_id>`

* Backend
  * Celery
  * Celery Broker : Redis
  * Celery Result Storage : Redis

#### Components version

* Version of each python components : [requirements](sample1/requirements.txt)


#### Quickstart for sample #1

```bash
./do.sh install redis --redis=auto
./do.sh install sample1
./do.sh start redis --redis=auto:6379
./do.sh start-back sample1 --redis=auto:6379
./do.sh start-front sample1 --port=8010 --redis=auto:6379

# launch optional celery monitoring UI :
./do.sh start-flower sample1 --port=8011
```



* Test with webpage `http://localhost:8010/`

* Call methods with HTTP GET with querystring
  `http://localhost:8010/add?a=1&b=2`
  `http://localhost:8010/mul?a=1&b=2`
  *Save the `task_id` printed*

* Get result with HTTP GET
  For any task :
  `http://localhost:8010/task/<task_id>`
  For `add` task only :
  `http://localhost:8010/task/add/<task_id>`
  For `mul` task only :
  `http://localhost:8010/task/mul/<task_id>`

* Monitor celery tasks with Flower
  `http://localhost:8011`



## Sample #2

Simple example with a simple API with Flask and Flask-RESTPlus (frontend) an asynchronous job manager with Celery/Redis (backend)

API is documented with swagger.


* Frontend
  * Flask for asynchronous web API restful API
  * Flask-RESTPlus for rest API and swagger support in Flask
  * Web page for testing API
  * API described with swagger `/api`
  * API exposed
    * Call `add` and `mul` methods with
      * HTTP GET with querystring `/api/math/add?a=1&b=3` `/api/math/mul?a=1&b=3`
      * HTTP POST with a pure json body `{a:1, b:3}`
    * Retrieve jobs status with HTTP GET
      * `/api/math/jobs/status/<task_id>`
    * Retrieve results with HTTP GET
      * `/api/math/jobs/result/<task_id>`
    * Delete results with HTTP DELETE
      * `/api/math/jobs/result/<task_id>`

* Backend
  * Celery
  * Celery Broker : Redis
  * Celery Result Storage : Redis


#### Components version

* Version of each python components : [requirements](sample2/requirements.txt)


#### Quickstart for sample #2

```bash
./do.sh install redis --redis=auto
./do.sh install sample2
./do.sh start redis --redis=auto:6379
./do.sh start-back sample2 --redis=auto:6379
./do.sh start-front sample2 --port=8020 --redis=auto:6379

# launch optional celery monitoring UI :
./do.sh start-flower sample2 --port=8021
```

* Swagger `http://localhost:8020/api`

* Test with webpage `http://localhost:8020/web`

* Call methods with HTTP GET with querystring
  `http://localhost:8020/api/math/add?a=1&b=2`
  `http://localhost:8020/api/math/mul?a=1&b=2`
  *Save the `task_id` printed*

* Get job status with HTTP GET
  `http://localhost:8020/api/math/jobs/status/<task_id>`

* Get job result with HTTP GET
  `http://localhost:8020/api/math/jobs/result/<task_id>`

* Delete job result with HTTP DELETE
  `http://localhost:8020/api/math/jobs/result/<task_id>`

* Monitor celery tasks with Flower
  `http://localhost:8021`




## Full how-to use

#### Help

```bash
./do.sh -h
```

#### Redis

All the samples use redis. You could choose between 3 types of redis instance.

Use `--redis` option value according to :

* with an auto deployed redis -- use `auto` -- Redis version : `4.0.8`
* with your own redis -- use `host:port`
* with redis inside a docker -- use `docker`
* with redis inside a docker-machine -- use `docker`

*NOTE : you dont need to start/stop redis for every sample. Only one redis instance is needed. We store data in different database inside redis*

#### Asynchronous tasks exposed on all samples

These methods are exposed through all samples via an API

* `add(a,b)` : add 2 numbers

* `mul(a,b)` : multiply 2 numbers

#### Install a sample

```bash
./do.sh install <id-sample>
```

#### Install redis

```bash
./do.sh install redis [ --redis=auto|docker ]
```

#### Run a sample


* First : start redis

```bash
./do.sh start redis [ --redis=auto[:<port>]|docker[:<port>] ]
```

* Second : start backend

```bash
./do.sh start-back <id-sample> [--redis=auto[:<port>]|docker[:<port>]|<host[:port]>]
```

* Third : start frontend

```bash
./do.sh start-front <id-sample> [--port=<port>] [--redis=auto[:<port>]|docker[:<port>]|<host[:port]>]
```



#### Stop a sample

* First : stop frontend

```bash
./do.sh stop-front <id-sample>
```

* Second : stop redis

```bash
./do.sh stop redis [ --redis=auto[:<port>]|docker ]
```

* Third : stop backend

```bash
./do.sh stop-back <id-sample>
```


## Inspirations

* Long running jobs and rest APi :
https://farazdagi.com/2014/rest-and-long-running-jobs/

* Flask and restful API : https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask/page/3
* Celery & Flask : https://blog.miguelgrinberg.com/post/using-celery-with-flask ([github code link](https://github.com/miguelgrinberg/flask-celery-example))

* Flask, flask-restplus, swagger :
http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/ ([github code link](https://github.com/postrational/rest_api_demo))

* Very complete RESTful API Server Example : https://github.com/frol/flask-restplus-server-example

* TODO : jobtastic

* TODO in a sample : Handle celery result stored in backend
  https://stackoverflow.com/questions/15199919/storing-a-task-id-for-each-celery-task-in-database
  http://django-celery-results.readthedocs.io/en/latest/reference/django_celery_results.models.html
  http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html


* TODO in a sample : Test marshmallow
marshmallow + flask restplus
tutorial : https://www.youtube.com/watch?v=mStotDgJwPU
https://flask-marshmallow.readthedocs.io/en/latest/
https://github.com/noirbizarre/flask-restplus/issues/317
https://github.com/joeyorlando/flask-restplus-marshmallow
