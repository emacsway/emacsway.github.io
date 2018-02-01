
Знакомство с Docker для Django-проекта
======================================

.. post:: Dec 23, 2017
   :language: ru
   :tags: Docker
   :category:
   :author: Ivan Zakrevsky


При начале работы с Docker стоит обратить внимание на ряд моментов, которые освещены слабо даже в официальной документации, не говоря уже про многочисленные блог-посты.


Настройка PostgreSQL в Docker
=============================

Даже `официальная документация <https://docs.docker.com/compose/django/#connect-the-database>`__ предлагает приложению работать с PostgreSQL под суперюзером.
Говорить про многочисленные статьи даже не приходится, от некоторых статей больше верда чем пользы.

В процессе разработки программы пользователь БД должен обладать такими же правами как и на production сервере (где в качестве базы данных нередко используется облачный сервис).
Это позволяет отслеживать соответствующие проблемы на самой ранней стадии.

Чтобы корректно и безопасно настроить PostgreSQL, необходимо обратить внимание на раздел "How to extend this image" документации `Docker-образа PostgreSQL <https://hub.docker.com/_/postgres/>`__.

Иногда такого способа расширения недостаточно, и тогда нужно создать свой собственный образ на основе этого.
Смотрите информацию в самом конце этого же раздела документации, начиная со слов "You can also extend the image with a simple Dockerfile to set a different locale."

При монтировании каталога данных на Windows может возникнуть `проблема <https://forums.docker.com/t/data-directory-var-lib-postgresql-data-pgdata-has-wrong-ownership/17963/12>`__, решение которой описано `здесь <https://forums.docker.com/t/trying-to-get-postgres-to-work-on-persistent-windows-mount-two-issues/12456/5?u=friism>`__:

.. code-block:: console

   docker volume create --name gitlab-postgresql -d local

..

.. code-block:: yaml
   :caption: docker-compose.yml
   :name: docker-compose-yml-postgresql-volume

   services:
     postgresql:
       restart: always
       image: postgres:10.1
       volumes:
         - postgresql-volume:/var/lib/postgresql:Z

     volumes:
       postgresql-volume:
         external: true


Как установить пакет в операционную систему Docker-образа?
==========================================================

Иногда нужно добавить какой-то пакет в операционную систему Docker-образа (например, postgis, если Вы не хотите использовать `один из готовых образов на хабе <https://hub.docker.com/r/mdillon/postgis/>`__).
Для этого нужно узнать тип и релиз операционной системы, и создать расширенный образ на основе существующего.
Для получения необходимой информации можно войти внутрь запущенного Docker-контейнера.
Обычно там используется Debian.
Перед установкой пакета не забудьте получить новые списки пакетов, например: ``apt-get update && apt-get install -y netcat-openbsd``


Как зайти внутрь запущенного Docker-контейнера?
===============================================

Здесь приведен простой пример https://stackoverflow.com/a/37766141

.. code-block:: console

    docker@default:~$ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
    b563764171e2        poc_web             "bundle exec rails s "   43 minutes ago      Up 43 minutes       0.0.0.0:3000->3000/tcp   poc_web_1
    c6e480b0f26a        postgres            "/docker-entrypoint.s"   49 minutes ago      Up 49 minutes       0.0.0.0:5432->5432/tcp   poc_db_1
    docker@default:~$ docker exec -it c6e480b0f26a sh
    # su - postgres
    No directory, logging in with HOME=/
    $ psql
    psql (9.5.3)
    Type "help" for help.

    postgres=#

Для отладки проблемного конейнера:

.. code-block:: console

    docker logs --tail 500 --follow --timestamps my_container_name_1


Инициализация служб
===================

Проблема в том, что директива `depends_on <https://docs.docker.com/compose/compose-file/#depends_on>`__ контролирует порядок запуска контейнеров, но не контролирует фактического запуска служб в контейнерах.

Многочисленные статьи игнорируют этот вопрос.
В лучшем случае они предлагают хак с помощью команды sleep.
Практически ни одна статья не описывает использования Docker для TDD, где хак с помощью команды sleep просто неприемлем.

Официальная документация так же `мало полезна в этом вопросе, хотя и указывает верное направление <https://docs.docker.com/compose/startup-order/>`__.

Вскользь этот вопрос был затронут в `этой статье <https://habrahabr.ru/company/otus/blog/337688/>`__.

Более подробно проблема описана в статье "`Docker Compose: Wait for Dependencies <https://8thlight.com/blog/dariusz-pasciak/2016/10/17/docker-compose-wait-for-dependencies.html>`__".

Я решил проблему с помощью `этого скрипта <https://github.com/dadarek/docker-wait-for-dependencies/blob/master/entrypoint.sh>`__, используя его там, где обычно используется хак с командой sleep.

.. code-block:: bash

    #!/bin/sh
    # Source Code:
    # https://github.com/dadarek/docker-wait-for-dependencies/blob/master/entrypoint.sh

    : ${SLEEP_LENGTH:=2}

    wait_for() {
      echo Waiting for $1 to listen on $2...
      while ! nc -z $1 $2; do echo sleeping; sleep $SLEEP_LENGTH; done
    }

    for var in "$@"
    do
      host=${var%:*}
      port=${var#*:}
      wait_for $host $port
    done


Docker-compose
==============

`Docker-compose <https://docs.docker.com/compose/gettingstarted/>`__ - безусловно полезная надстройка, заметно облегчающая использование Docker.


Монтирование каталогов постоянного хранения информации
======================================================

Не забывайте `монтировать каталоги постоянного хранения информации <https://docs.docker.com/compose/compose-file/#volumes>`__ для баз данных.
Многие ознакомительные статьи игнорируют этот момент.

Иногда возникает эффект "исчезающего каталога", например, ``node_modules``, который был создан в момент создания образа, но при его монтировании уже после создания образа - он исчезает.
Более подробно эта `проблема и ее решение описаны здесь <https://stackoverflow.com/a/32785014>`__:

    A workaround is to use a data volume to store all the node_modules, as data volumes copy in the data from the built docker image before the worker directory is mounted. This can be done in the docker-compose.yml like this:

.. code-block:: yaml
   :caption: docker-compose.yml
   :name: docker-compose-yml-volumes

   redis:
       image: redis
   worker:
       build: ./worker
       command: npm start
       ports:
           - "9730:9730"
       volumes:
           - worker/:/worker/
           - /worker/node_modules
       links:
           - redis


Безголовый браузер
==================

Angular использует среды Karma и Protractor для тестирования, которые используют браузер для тестирования.
На момент написания этих строк, подробного руководства для решения этой проблемы мне найти не удалось.
Существуют разные способы решения например, использование PhantomJS, но мне по ряду причин больше подошло `решение приведенное здесь <http://cvuorinen.net/2017/05/running-angular-tests-in-headless-chrome/>`__ (`исходный код <https://gist.github.com/cvuorinen/543c6f72f8ec917ebfd596802d387aa3>`__).

`Устанавливаем <https://stackoverflow.com/a/45510099>`__ Google Chrome в Dockerfile::

    RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    RUN echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list
    RUN apt-get update && apt-get install --no-install-recommends -y google-chrome-stable

Редактируем karma.conf.js::

    browsers: ['Chrome_without_sandbox'],
    customLaunchers: {
      Chrome_without_sandbox: {
        base: 'ChromeHeadless',
        flags: [
          '--no-sandbox',
          '--headless',
          '--disable-gpu',
          '--remote-debugging-port=9876'
       ]  // https://developers.google.com/web/updates/2017/04/headless-chrome
      }
    }

И редактируем protractor.conf.js::

    capabilities: {
      browserName: 'chrome',
      chromeOptions: {
        binary: process.env.GOOGLE_CHROME_SHIM,  // If you need
        args: [
          "--no-sandbox",
          "--headless",
          "--disable-gpu",
          "--window-size=800x600"
        ]  // https://developers.google.com/web/updates/2017/04/headless-chrome
      }
    },
    directConnect: true,
    chromeOnly:true,

Существуют готовые образы:

- `docker-ng-cli-karma <https://github.com/trion-development/docker-ng-cli-karma>`__
- `docker-ng-cli-e2e <https://github.com/trion-development/docker-ng-cli-e2e>`__
- `docker-ng-cli <https://github.com/trion-development/docker-ng-cli>`__


Supervisor
==========

В более сложных случаях можно использовать Docker совместо с `Supervisor <http://supervisord.org/>`__, но не забывайте совет Kent Beck:

    "Of course, you can
    do a better job if you have more tools in your toolbox than if you have fewer, but it
    is much more important to have a handful of tools that you know when not to use,
    than to know everything about everything and risk using too much solution."
    ("Extreme Programming Explained" by Kent Beck)


.. update:: 13 Jan, 2018
