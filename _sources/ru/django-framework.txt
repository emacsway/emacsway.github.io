
О моем опыте использования Django Framework
===========================================

.. post:: Jul 26, 2017
   :language: ru
   :tags: Django, ORM
   :category:
   :author: Ivan Zakrevsky

   Django позволяет решать огромный спектр задач быстро, и легко находить исполнителей. При грамотном подходе, можно использовать все преимущества Django и не стать заложником ее недостатков.

В свое время кто-то красиво сказал, что безопасность - это баланс между затратами на защиту и потенциальной выгодой от взлома.
Нет смысла превышать этот баланс.

Принимая решение относительно IT-технологий, мы тоже пытаемся найти баланс между затратами на содержание технологии (в том числе поиск и обучение новых специалистов) и обретаемой функциональностью.

Django, безусловно, доставляет определенные хлопоты, но вместе с тем она позволяет решать огромный спектр задач быстро, и легко находить исполнителей.
При грамотном подходе, можно использовать все преимущества Django и не стать заложником ее недостатков.

.. contents:: Содержание

Больше всего хлопот доставляет Django ORM, поэтому мы начнем с него.


Проблемы Django ORM и способы их решения
========================================


Семантическое сопряжение валидации моделей
------------------------------------------

Принцип "Защитного программирования" [#fncodec]_ требует делать невозможным создание невалидного объекта.
Для валидации должны использоваться сеттеры объекта.
В Джанго мы должны явно вызвать метод `Model.full_clean() <https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.full_clean>`_ перед сохранением объекта, что, конечно же, часто никто не делает, и это часто приводит к различным проблемам.
Эта проблема известна как "семантическое сопряжение" а так же "G22: Make Logical Dependencies Physical" [#fnccode]_ and "G31: Hidden Temporal Couplings" [#fnccode]_.
Можно решить это проблему технически, но обычно достаточно просто соблюдать дисциплину разработки.


Active Record
-------------

Django ORM реализует паттерн `ActiveRecord`_, который создает простоту использования за счет нарушения принципа `Single responsibility principle`_ (SRP), из-за чего его часто называют антипаттерном.
Этот паттерн смешивает в одном классе бизнес-логику и служебную логику доступа к данным.
К сожалению, эта простота уместна только в простых случаях.
В более-менее серьезном приложении от этого больше проблем, чем достоинств.

Поскольку Django не использует слоя `Repository`_, было бы желательно сокрыть реализацию доступа к источнику данных посредством Сервисного Слоя, см. статью ":doc:`service-layer`".
Это необходимо потому, что возможностей Django ORM не всегда достаточно для построения сложных запросов или для создания сложных моделей.
Тогда приходится подменять Django ORM сторонними инструментами или реализацией в голом виде паттерна `DataMapper`_, к этому вопросу мы еще вернемся.
В любом случае, реализация доступа к данным должна быть сокрыта от приложения, и это одна из обязанностей Сервисного Слоя.


Identity Map
------------

Джанго не реализует паттерна `Identity Map`_, и, как результат этого, возникает много дублируемых запросов.
Частично этот недостаток смягчается наличием `prefetch_related() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#prefetch-related>`_.
Существуют реализации этого паттерна в виде сторонних библиотек,
`django-idmapper <https://github.com/dcramer/django-idmapper>`_
`django-idmap <https://pypi.python.org/pypi/django-idmap>`_.
Но они, к сожалению, никаких функций кроме кэширования не выполняют, и за транзакционной согласованностью данных не следят.


Выполнение сложных SQL-запросов
-------------------------------

К сожалению, возможности интерфейса Django ORM для создания сложных SQL-запросов недостаточно.
В таком случае приходится или использовать сторонние инструменты, которые будут рассмотрены далее, или использовать Raw-SQL.
В любом случае, детали реализации должны быть инкапсулированы внутри фабрики запроса.


Реализация сложных моделей
--------------------------

Очень часто приходится иметь дело с объектами, которые содержат агрегированную информацию, аннотации, или сочетают в себе данные нескольких таблиц.

SQLAlchemy, безусловно, предоставляет `более гибкие возможности <http://docs.sqlalchemy.org/en/rel_1_1/orm/nonstandard_mappings.html>`_.
Но даже этих возможностей `хватает не всегда <http://robbygrodin.com/2017/04/18/wayfair-blog-post-orm-bankruptcy/>`__.

Вот почему важно скрывать детали реализации доступа к данным последством слоя `Repository`_ или `Service Layer`_.
В таком случае я просто использую голый паттерн `DataMapper`_ и чистую `Domain Model`_.

Как показывает практика, обычно такие случаи не превышают 10%, что не настолько существенно для отказа от Django ORM, ибо привлекательность легкого поиска специалистов все равно перевешивает.


Сторонние инструменты
---------------------


SQLAlchemy
^^^^^^^^^^

Джанго имеет несколько приложений для интеграции SQLAlchemy:

- `django-sqlalchemy <https://github.com/auvipy/django-sqlalchemy>`_
- `aldjemy <https://github.com/Deepwalker/aldjemy>`_
- `django-sabridge <https://github.com/johnpaulett/django-sabridge>`_


SQLBuilder
^^^^^^^^^^

Для создания сложных запросов с Django ORM я обычно использую `sqlbuilder <http://sqlbuilder.readthedocs.io/en/latest/>`_.

Правила хорошего тона требуют создавать отдельный класс-фабрику для каждого запроса, чтобы скрыть детали реализации от приложения.
Внутри этого класса Вы можете легко подменить одну реализацию другой.


Storm ORM
^^^^^^^^^

Вопрос интеграции Storm ORM уже рассматривался, поэтому я просто приведу ссылки:

- ":doc:`storm-orm`"
- ":doc:`../ru/build-raw-sql-by-storm-orm`"


Тестирование
^^^^^^^^^^^^

Если используется несколько технологий доступа к данным, то стоит упомянуть генератор файковых данных `mixer <https://github.com/klen/mixer>`_, который поддерживает несколько ORM.
Другие генераторы `можно найти <https://djangopackages.org/grids/g/fixtures/>`__, как обычно, на `djangopackages.org <https://djangopackages.org/>`_.



Очистка кэша
------------

Реализация Django ORM в виде `ActiveRecord`_ вынуждает нас напрямую вызывать метод `Model.save() <https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.save>`_.
Проблема в том, что сигналы `post_save <https://docs.djangoproject.com/en/1.11/ref/signals/#post-save>`_ и `pre_delete <https://docs.djangoproject.com/en/1.11/ref/signals/#pre-delete>`_ часто используются разработчиками для инвалидации кэша.
Это не совсем правильно, так как Django ORM не использует паттерна `Unit of Work`_, и время между сохранением и фиксацией транзакции оказывается достаточным чтобы параллельный поток успел воссоздать кэш с устаревшими данными.

В интернете можно найти библиотеки которые позволяют `послать сигнал во время фиксации транзакции <https://pypi.python.org/pypi?%3Aaction=search&term=django+commit+signal&submit=search>`__.
Django 1.9 и выше возволяет использовать `transaction.on_commit() <https://docs.djangoproject.com/en/1.11/topics/db/transactions/#django.db.transaction.on_commit>`_, что частично решает проблему если не используется репликация.

Я использую библиотеку `cache-dependencies <https://bitbucket.org/emacsway/cache-dependencies>`_, о чем я писал в статье ":doc:`cache-dependencies`".


Django REST framework
=====================

Если мы до этого рассматривали недостатки Django ORM, то `Django REST framework`_ удивительным образом превращает его недостатки в достоинства, ведь интерфейс создания запросов Django ORM великолепно подходит для REST.

Если Вам посчастливилось использовать на стороне клиента `Dstore`_, то на стороне сервера Вы можете использовать `django-rql-filter <https://pypi.python.org/pypi/django-rql-filter>`_ или `rql <https://pypi.python.org/pypi/rql>`__.

Честно сказать, Django REST framework заставляет изрядно посидеть в отладчике, и потратить на него определенное время, что, разумеется, характеризует проектные решения не с лучшей точки зрения.
Хорошая программа должна читаться, а не пониматься, и уж тем более без помощи отладчика.
Это характеризует соблюдение главного императива разработки программного обеспечения:

    Главным Техническим Императивом Разработки ПО является управление сложностью.
    Управлять сложностью будет гораздо легче, если при проектировании
    вы будете стремиться к простоте.
    Есть два общих способа достижения простоты: минимизация объема существенной
    сложности, с которой приходится иметь дело в любой конкретный момент
    времени, и подавление необязательного роста несущественной сложности.

    Software's Primary Technical Imperative is managing complexity. This is greatly
    aided by a design focus on simplicity.
    Simplicity is achieved in two general ways: minimizing the amount of essential
    complexity that anyone's brain has to deal with at any one time, and keeping
    accidental complexity from proliferating needlessly.
    («Code Complete» [#fncodec]_)

Однако совокупный баланс преимуществ и недостатков делает Django REST framework весьма привлекательным для разработки, особенно если Вам нужно привлекать к работе новых (или временных) специалистов или отдать часть работы на аутсорсинг.

Просто нужно учитывать, что существует определенный входной барьер, который требует определенных затрат на его преодоление, и Вы должны понимать какую выгоду Вы с этого можете получить, ибо не всегда эта выгода стоит потраченных усилий для преодоления входного барьера.

На критике проектных решений я останавливаться не буду, конструктивно Django REST framework меня ни в чем не ограничивает, а это самое главное.


Суффиксирование внешних ключей Django REST framework
----------------------------------------------------

Когда на стороне клиента используются инструменты для обработки внешних ключей, возникает желание для значений внешнего ключа использовать поле с \*_id суффиксом. Здесь приводится `пример реализации <https://github.com/OpenSlides/OpenSlides/commit/f6c50a966d84b6c8251b9b8e7556623bae40f8f6>`__ как это можно достигнуть.
Этот же пример в виде `gist <https://gist.github.com/ostcar/eb78515a41ab41d1755b>`__ и `обсуждение <https://github.com/encode/django-rest-framework/issues/3121>`__.


SQLAlchemy
----------

Огромным преимуществом Django REST framework является то, что он ORM agnostic.
Он имеет прекрасную интергацию с Django ORM, но он легко может работать с голой реализацией паттерна Data Mapper который будет возвращать `namedtuple`_ для `Data Transfer Object`_.
Так же он имеет хорошую интеграцию с `SQLAlchemy`_ в виде стороннего приложения `djangorest-alchemy <https://github.com/dealertrack/djangorest-alchemy>`_ (`документация <http://djangorest-alchemy.readthedocs.io/en/latest/>`__).
См. `обсуждение интеграции <https://github.com/encode/django-rest-framework/issues/2439>`__.


OpenAPI и Swagger
-----------------

Django REST framework позволяет `генерировать схему <www.django-rest-framework.org/api-guide/schemas/>`_ в формате OpenAPI и интегрируется с `swagger <https://swagger.io/>`_ с помощью библиотеки `django-rest-swagger <https://django-rest-swagger.readthedocs.io/en/latest/>`_.

Это открывает неограниченные возможности по генерированию `стабов <Service Stub_>`__ для клиента.
Что, в свою очередь, позволяет тестировать client-side без использования server-side, разграничить ответственность между разработчиками client-side и server-side, быстро диагностировать причину проблем, фиксировать протокол обмена, а главное, позволяет вести параллельную разработку client-side даже если server-side еще не готов.

Схема OpenAPI так же может быть использована для автоматической генерации тестов с помощью `pyresttest <https://github.com/svanoort/pyresttest>`_.


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts

.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Robert C. Martin: http://informit.com/martinseries
.. _Code Complete: http://www.informit.com/store/code-complete-9780735619678
.. _Steve McConnell: http://www.informit.com/authors/bio/754ffba3-b7b2-45ef-be37-3d9995e8e409
.. _Refactoring\: Improving the Design of Existing Code: https://martinfowler.com/books/refactoring.html
.. _Martin Fowler: https://martinfowler.com/aboutMe.html

.. _ActiveRecord: http://www.martinfowler.com/eaaCatalog/activeRecord.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _DataMapper: http://martinfowler.com/eaaCatalog/dataMapper.html
.. _Data Transfer Object: http://martinfowler.com/eaaCatalog/dataTransferObject.html
.. _Domain Model: https://martinfowler.com/eaaCatalog/domainModel.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Layer: https://martinfowler.com/eaaCatalog/serviceLayer.html
.. _Service Stub: https://martinfowler.com/eaaCatalog/serviceStub.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html

.. _Single responsibility principle: https://en.wikipedia.org/wiki/Single_responsibility_principle

.. _Django REST framework: http://www.django-rest-framework.org/
.. _Dstore: http://dstorejs.io/
.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _cache-dependencies: https://bitbucket.org/emacsway/cache-dependencies
