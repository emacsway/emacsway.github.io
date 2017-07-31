
О моем опыте использования Django Framework
===========================================

.. post:: Jul 26, 2017
   :language: ru
   :tags: Django, ORM
   :category:
   :author: Ivan Zakrevsky
   :exclude:

   Django framework позволяет быстро решать огромный спектр задач и легко находить исполнителей. При грамотном подходе, можно использовать все преимущества Django и не стать заложником ее недостатков.

В свое время кто-то красиво сказал, что безопасность - это баланс между затратами на защиту и потенциальной выгодой от взлома.
Нет смысла превышать этот баланс.

Принимая решение относительно IT-технологий, мы тоже пытаемся найти баланс между затратами на содержание технологии (в том числе поиск и обучение новых специалистов) и обретаемой функциональностью.

Django framework, безусловно, доставляет определенные хлопоты, но вместе с тем он позволяет решать огромный спектр задач достаточно быстро, и легко находить исполнителей.
При грамотном подходе, можно использовать все преимущества Django framework и не стать заложником его недостатков.

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
`django-idmapper <https://github.com/dcramer/django-idmapper>`_,
`django-idmap <https://pypi.python.org/pypi/django-idmap>`_.
Но они, никаких функций кроме кэширования не выполняют, и за транзакционной согласованностью данных не следят.
Правда, вы вряд-ли заметите эту проблему, так как Django приложение обычно обрабатывает HTTP-запрос одной транзакцией.


Транзакционная согласованность данных
-------------------------------------

Мало того, что Вы получаете несколько экземпляров одного и тоже же объекта в памяти потока, что может привести к утрате данных из-за рассинхронизации состояния этих экземпляров, так эти экземпляры еще и никак не согласовываются с их записами в БД в момент фиксации (отката) транзакции.

Джанго поддерживает транзакции, но не поддерживает транзакционной согласованности данных, в отличии от Storm ORM / SQLAlchemy.
Вы должны самостоятельно заботиться о состоянии экземпляров моделей в памяти в момент фиксации (отката) транзакции.

Так например, если Вы используете уровень изоляции транзакции "Repeatable read", то после фиксации транзакции состояние Ваших экземпляров моделей в памяти может утратить актуальность.
Соответственно, при откате транзакции вы должны вернуть им начальное состояние.

Как уже упоминалось ранее, для обработки HTTP-запроса это не критично, так как Django framework обычно обслуживает его одной транзакцией.
А вот при разработке командных скриптов и задач по расписанию этот момент следует учитывать.

Вы должны так же самостоятельно заботиться о предотвращении взаимных блокировок (Deadlock_), так как Django ORM не реализует паттерна `Unit of Work`_ и не использует топологической сортировки.

Здесь стоит так же упомянуть частую проблему начинающих разработчиков, которые пытаются обработать большую коллекцию объектов не используя `select_for_update() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#select-for-update>`_.
Обработка коллекции занимает значительное время, которое достаточно для того, чтобы состояние записи в БД для загруженного объекта, ожидающего своей обработки, успело измениться, что при неумелом использовании транзакций приводит к утрате параллельных изменений (а при умелом может привести к неразрешимому конфликту).

Кроме того, следует внимательно ознакомиться со всеми предостережениями метода `iterator() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#iterator>`_, использование которого не гарантирует отсутствия утечки памяти, если Вы не используете `SSCursor <https://github.com/farcepest/MySQLdb1/blob/master/doc/user_guide.rst#using-and-extending>`_ для MySQL.


Сервисный слой и django.db.models.Manager
-----------------------------------------

Широко распространенная ошибка - использование класса django.db.models.Manager в качестве сервисного слоя.
Этот вопрос детально был рассмотрен в статье ":doc:`service-layer`".


Выполнение сложных SQL-запросов
-------------------------------

Возможностей интерфейса Django ORM для создания сложных SQL-запросов недостаточно.
В таком случае приходится или использовать сторонние инструменты, которые будут рассмотрены далее, или использовать Raw-SQL.
В любом случае, детали реализации должны быть инкапсулированы внутри фабрики запроса.

В моей практике был случай когда нужно было в `админке <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/>`__ реализовать выборку пользователей с поиском по шаблону (LIKE '%keyword%') как по строкам в таблице пользователей так и в присоединенной (LEFT JOIN) таблице профилей, причем критерии поиска должны были сочетаться условием ИЛИ (OR), что приводило к полному проходу по присоединенной таблице на каждую строку таблицы пользователей.
Записей в БД MySQL было несколько миллионов, и это работало очень медленно.
В той версии MySQL еще не поддерживался ngram FULLTEXT index.
Для оптимизации запроса нужно было присоединять уже профильтрованную выборку из таблицы профилей, а не всю таблицу профилей, переместив критерий выборки в подзапрос.
Подобный пример Вы можете найти в книге «High Performance MySQL» [#hpmysql]_.
Для решения проблемы моему коллеге пришлось ":doc:`сделать адаптер для sqlbuilder Storm ORM <storm-orm>`" наподобие `sqlalchemy-django-query <https://github.com/mitsuhiko/sqlalchemy-django-query>`__.
В результате была достигнута возможность выразить SQL-запрос любого уровня сложности в интерфейсе django.db.models.query.QuerySet.


Реализация сложных моделей
--------------------------

Очень часто приходится иметь дело с объектами, которые содержат агрегированную информацию, аннотации, или сочетают в себе данные нескольких таблиц.

SQLAlchemy, безусловно, предоставляет `более гибкие возможности <http://docs.sqlalchemy.org/en/rel_1_1/orm/nonstandard_mappings.html>`_.
Но даже этих возможностей `хватает не всегда <http://robbygrodin.com/2017/04/18/wayfair-blog-post-orm-bankruptcy/>`__.

Механизм аннотаций в Storm ORM / SQLAlchemy реализован более удачно.
Механизм аннотаций Django ORM лучше не использовать вообще, в пользу голого паттерна Data Mapper.
Дело в том, что схема модели постоянно эволюционирует, и в нее постоянно добавляются новые поля.
И нередко случается так, что имя нового поля уже используется аннотацией, из-за чего возникает конфликт в пространстве имен.
Решением проблемы может быть разделение пространства имен, используя для аннотаций отдельную модель или обертку (Wrapper) над экземпляром модели.

Identity Map - еще одна из причин чтобы не использовать механизм аннотаций Django ORM (а так же отнестись с большой осторожностью к prefetch_related()).
Ведь если в потоке может быть только один экземпляр объекта, то его состояние не может нести никаких отличий для каждого конкретного запроса.

Вот почему важно скрывать детали реализации доступа к данным последством слоя `Repository`_ или `Service Layer`_.
В таком случае я просто выполняю реализацию в виде голого паттерна `DataMapper`_ и чистой `Domain Model`_.

Как показывает практика, обычно такие случаи не превышают 10%, что не настолько существенно для отказа от Django ORM, ибо привлекательность легкого поиска специалистов все равно перевешивает.


Сторонние инструменты
---------------------


SQLAlchemy
^^^^^^^^^^

Джанго имеет несколько приложений для интеграции SQLAlchemy:

- `django-sqlalchemy <https://github.com/auvipy/django-sqlalchemy>`_
- `aldjemy <https://github.com/Deepwalker/aldjemy>`_
- `django-sabridge <https://github.com/johnpaulett/django-sabridge>`_
- `sqlalchemy-django-query <https://github.com/mitsuhiko/sqlalchemy-django-query>`_


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

Честно говоря, Django REST framework заставляет изрядно посидеть в отладчике, и потратить на него определенное время, что, разумеется, характеризует используемые им проектные решения не с лучшей стороны.
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
Этот же пример на `gist <https://gist.github.com/ostcar/eb78515a41ab41d1755b>`__ и `обсуждение <https://github.com/encode/django-rest-framework/issues/3121>`__.


SQLAlchemy
----------

Огромным преимуществом Django REST framework является то, что он ORM agnostic.
Он имеет прекрасную интергацию с Django ORM, но он легко может работать с голой реализацией паттерна Data Mapper который будет возвращать `namedtuple`_ для `Data Transfer Object`_.
Так же он имеет хорошую интеграцию с `SQLAlchemy`_ в виде стороннего приложения `djangorest-alchemy <https://github.com/dealertrack/djangorest-alchemy>`_ (`документация <http://djangorest-alchemy.readthedocs.io/en/latest/>`__).
См. `обсуждение интеграции <https://github.com/encode/django-rest-framework/issues/2439>`__.


OpenAPI и Swagger
-----------------

Django REST framework позволяет `генерировать схему <www.django-rest-framework.org/api-guide/schemas/>`_ в формате OpenAPI и интегрируется с `swagger <https://swagger.io/>`_ с помощью библиотеки `django-rest-swagger <https://django-rest-swagger.readthedocs.io/en/latest/>`_.

Это открывает неограниченные возможности по генерированию `стабов <Service Stub_>`__ для клиента и позволяет использовать один из существующих генераторов стабов для swagger.
Что, в свою очередь, позволяет тестировать client-side без использования server-side, разграничить ответственность между разработчиками client-side и server-side, быстро диагностировать причину проблем, фиксировать протокол обмена, а главное, позволяет вести параллельную разработку client-side даже если server-side еще не готов.

Схема OpenAPI так же может быть использована для автоматической генерации тестов, например, с помощью `pyresttest <https://github.com/svanoort/pyresttest>`_.

Мой товарищ работает над библиотекой `python-easytest <https://bitbucket.org/sergeyglazyrindev/python-easytest>`_, которая избавляет от необходимости написания интеграционных тестов и тестирует приложение на основании схемы OpenAPI.


Проблема JOIN-ов
----------------

Django REST framework часто используется вместе с `django-filter <https://pypi.python.org/pypi/django-filter>`_.
И тут возникает проблема, которая отражена в документации как:

        "To handle both of these situations, Django has a consistent way of processing filter() calls.
        Everything inside a single filter() call is applied simultaneously to filter out items matching
        all those requirements. Successive filter() calls further restrict the set of objects,
        but for multi-valued relations, they apply to any object linked to the primary model,
        not necessarily those objects that were selected by an earlier filter() call."

        See more info on:
        https://docs.djangoproject.com/en/1.8/topics/db/queries/#lookups-that-span-relationships

Решается эта проблема легко, в классе FilterSet() следует использовать обертку с ленивым вычислением  вместо реального django.db.models.query.QuerySet, которая будет полность повторять его интерфейс, но вызвать метод filter() однократно, передавая ему все накопленные критерии выборки.


Генерация \*.csv, \*.xlsx
-------------------------

Django и Django REST framework содержит огромное количество расширений.
Это то главное преимущество, ради которого есть смысл терпеть их недостатки.
Можно даже генерировать \*.csv, \*.xlsx файлы:

- `django-rest-framework-excel <https://github.com/diegueus9/django-rest-framework-excel>`_
- `django-rest-framework-csv <https://github.com/mjumbewu/django-rest-framework-csv>`_
- `django-rest-pandas <https://github.com/wq/django-rest-pandas>`_
- и др.

Здесь, правда, возникает проблема с трансляцией вложенных структур данных в плоский список, и наоборот, с парсингом плоского списка во вложенную структуру.
Частично эту проблему можно решить с помощью библиотеки `jsonmapping <https://github.com/pudo/jsonmapping>`_.
Но мне это решение не подошло, и я делал полноценный декларативный маппер данных.


Плюсы и минусы
==============


Плюсы
-----

Джанго имеет удачный `View <https://docs.djangoproject.com/en/1.11/topics/http/views/>`__,  который представляет собой разновидность паттерна `Page Controller`_, достаточно удачные формы и шаблонизатор (если использовать `django.template.loaders.cached.Loader <https://docs.djangoproject.com/en/1.11/ref/templates/api/#django.template.loaders.cached.Loader>`_).

Несмотря на все недостатки Django ORM, его интерфейс построения запросов хорошо подходит для REST API.

Django имеет огромное сообщество с огромным количеством готовых приложений.
Находить специалистов для Django и Django REST framework очень легко.

Django декларирует такой способ разработки, который не требователен к уровню разработчиков.

Django способен экономить много времени при правильном использовании.


Минусы
------

Уровень сложности Django растет с каждым релизом, зачастую опережая реализуемые ею возможности, и от этого ее привлекательность постоянно уменьшается.

Если Вам нужно адаптировать Django ORM для своих потребностей, то сделать это с последним релизом будет, пожалуй, сложнее, чем адаптировать SQLAlchemy.
При том что в адаптации он нуждается чаще чем SQLAlchemy.
Простота больше не является главной прерогативой Django, как это было в ранних версиях.
Практически во всех проектах, с которыми мне приходилось иметь дело, Django ORM дополнялся (или заменялся) сторонними инструментами либо голой реализацией паттерна Data Mapper.

В кругу моих друзей Django framework используется в основном в силу привычки и по инерции.

Несмотря на то, что Django framework имеет огромное количество готовых приложений, их качество зачастую оставляет желать лучшего, а то и вовсе содержит баги, причем, попадаются очень коварные баги, которые проявляются только в многопоточной среде под нагрузками, и которые отлаживать весьма затруднительно.

Качество специалистов, имеющих опыт работы с Django, тоже зачастую невысокое.
Квалифицированные специалисты среди моих друзей стараются избегать работу с Django.


Заключение
==========

Использовать или не использовать Django framework зависит от того, какие цели Вы перед собой ставите, и командой какой квалификации Вы располагаете.

Если Ваша команда высоко-квалифицированная в области архитектуры и проектирования, вы используете :doc:`методики совместной разработки <../en/how-to-quickly-develop-high-quality-code>` для распространения опыта, чувствуете в себе силы сделать проект более качественным без Django, и располагаете достаточными ресурсами и финансами для этого, тогда есть смысл использовать другой стэк технологий.

В противном случае, Django framework может сослужить Вам хорошую пользу.
Много самонадеянных команд так и не смогли без Django сделать свои проекты лучше, чем сделали бы это с ней.

Никто не обязывает Вас использовать Django всегда и везде.
Django REST framework позволяет Вам абстрагироваться от Django ORM и даже от своего сериализатора.

Если Вы занимаетесь аутсорсингом, Ваш средний проект длится не больше года, бюджет невысокий а сроки сжатые, то у Django есть что Вам предложить.

Если Вы работаете над большим действующим проектом, то выгоды уже не столь очевидны.
Все дело в балансе, который Вы должны сами для себя определить.

Но если Вы используете `ограниченные контексты <https://martinfowler.com/bliki/BoundedContext.html>`_ или `микросервисную архитектуру <https://martinfowler.com/articles/microservices.html>`_, то каждая команда может принимать решение о стэке технологий самостоятельно.
Вы можете использовать Джангу только для части проекта, или использовать только некоторые компоненты Джанги.

А можете не использовать вообще. Среди альтернатив я советую обратить внимание на web-framework который мне импонирует `wheezy.web <https://pypi.python.org/pypi/wheezy.web>`_.


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#hpmysql] «High Performance MySQL» by Baron Schwartz, Peter Zaitsev, and Vadim Tkachenko


.. update:: 29 Jul, 2017


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
.. _Page Controller: https://martinfowler.com/eaaCatalog/pageController.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Layer: https://martinfowler.com/eaaCatalog/serviceLayer.html
.. _Service Stub: https://martinfowler.com/eaaCatalog/serviceStub.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html

.. _ACID: https://en.wikipedia.org/wiki/ACID
.. _Deadlock: https://en.wikipedia.org/wiki/Deadlock
.. _Single responsibility principle: https://en.wikipedia.org/wiki/Single_responsibility_principle

.. _Django REST framework: http://www.django-rest-framework.org/
.. _Dstore: http://dstorejs.io/
.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _cache-dependencies: https://bitbucket.org/emacsway/cache-dependencies
