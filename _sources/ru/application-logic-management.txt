
Управление логикой приложения. Про MVC, Use Case, Service Layer, CQRS, Event Sourcing и др.
===========================================================================================

.. post:: Dec 02, 2018
   :language: ru
   :tags: Design, Architecture, Service Layer, Redux, Flux, Model, CQRS, Event Sourcing
   :category:
   :author: Ivan Zakrevsky

В свое время Гради Буч сказал, что "Архитектура отражает важные проектные решения по формированию системы, где важность определяется стоимостью изменений".
Одним из важных таких решений является управление Логикой Приложения.
В этом посте мы попытаемся разобраться с тем, почему это важно, как управлять Логикой Приложения, и как это может снизить стоимость изменений.


.. contents:: Содержание


Способы организации Логики Приложения (Application Logic)
=========================================================

Широко распространены три способа организации Application Logic:

1. `Service Layer (сервисный слой) <https://martinfowler.com/eaaCatalog/serviceLayer.html>`__.
Который, в свою очередь, делится на Оркестровый ("request/response", т.е. сервис осведомлен об интерфейсе других сервисов) и Хореографический (Event-Driven, т.е. loosely coupled).

Последний является разновидностью паттерна Command, и используется в CQRS-приложениях (reducers в Redux - наглядный пример).

Подробней Оркестровые Сервисные Слои рассматриваются в статье

- ":doc:`./service-layer`",

а Хореографические - в статье

- ":doc:`./role-of-service-layer-in-cqrs-and-event-sourcing-using-redux-in-angular-as-an-example`".

2. `Front Controller <https://martinfowler.com/eaaCatalog/frontController.html>`__ и `Application Controller <https://martinfowler.com/eaaCatalog/applicationController.html>`__ (которые тоже, по сути, является разновидностью паттерна Command).

..

    "A Front Controller handles all calls for a Web site, and is usually structured in two parts: a Web handler and a command hierarchy."

    \- "Patterns of Enterprise Application Architecture" by Martin Fowler and others.

..

    "For both the domain commands and the view, the application controller needs a way to store something it can invoke.
    A Command [Gang of Four] is a good choice, since it allows it to easily get hold of and run a block of code."

    \- "Patterns of Enterprise Application Architecture" by Martin Fowler and others.

3. `Use Case <https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html>`__, который также, является разновидностью паттерна Command.
На 15:50 Robert C. Martin проводит `параллель между Use Case и паттерном Command <https://youtu.be/Nsjsiz2A9mg?t=15m45s>`__.

Собственно говоря, производной паттерна Command является даже `Method Object <https://refactoring.com/catalog/replaceFunctionWithCommand.html>`__.

Use Case обязан своим существованием именно наличию Бизнес-Логики, которая  application specific, и не имеет смысла вне контекста приложения.
Его задача сводится к освобождению этих application specific Business Rules от зависимостей от приложения путем инверсии контроля (IoC).

Если бы Use Case не содержал Бизнес-Логики, то не было бы и смысла отделять его от Page Controller, иначе приложение пыталось бы абстрагироваться от самого себя же.

Но, в любом случае, это все способы организации в первую очередь Логики Приложения, и лишь во вторую очередь, Бизнес-Логики, которая не обязательно должна присутствовать, кроме случая Use Case, иначе он утратил бы причины для существования.

При правильной организации Бизнес-Логики, и при использовании качественного ORM, зависимость Бизнес-Логики от приложения будет минимальна.
Здесь основная проблема заключается в том, чтобы организовать доступ к связанным объектам, но не подмешивать Логику Приложения (и логику доступа к данным) в Domain Models, эту темы мы подробно рассмотрим в одном из следующих постов.


Проблема параллельного обновления
=================================

Интернет открыл доступ к огромному количеству данных, которое несопоставимо велико с возможностями одного сервера.
Возникла необходимость в масштабировании и в распределенном хранении и обработке данных.

Одна из самых острых проблем - это проблема параллельного обновления данных.
Все состояния гонки (race condition), взаимоблокировки (deadlocks) и другие проблемы параллельного обновления обусловлены изменяемостью переменных.

Любой порядок выражается в правильном наложении ограничений.


CQRS
====

Проблему параллельного обновления в значительной мере можно уменьшить наложением ограничения на двунаправленные изменения состояния путем введения однонаправленных изменений, т.е. путем отделения чтения от записи.
Именно такой подход используется в Redux.

    "it allows us to host the two services differently eg: we can host the read service on 25 servers and the write service on two.
    The processing of commands and queries is fundamentally asymmetrical, and scaling the services symmetrically does not make a lot of sense."

    \- "`CQRS, Task Based UIs, Event Sourcing agh! <http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/>`__" by Greg Young

Управление Логикой Приложения и Бизнес-Логикой хорошо раскрывается в статье "`Clarified CQRS <http://udidahan.com/2009/12/09/clarified-cqrs/>`__" by Udi Dahan.

Использование CQRS для хранения данных приближает нас к использованию парадигмы Функционального Программирования в коде (как, например, при использовании Redux).

Функциональное Программирование по своей сути не может порождать побочных эффектов (т.к. Функциональное Программирование накладывает ограничение на присваивание (изменяемость)), и именно этим обусловлен рост его популярности в эпоху распределенных вычислений.
Нет изменяемого состояния - нет проблем параллельного обновления.

Следует отличать парадигму Функционального Программирования от языков, поддерживающих эту парадигму, поскольку нередко языки, поддерживающие эту парадигму, позволяют ей не следовать.

Однако, несмотря на открывшиеся возможности использовать Функциональное Программирование в коде, само хранилище данных (IO-устройство) все еще подвержено проблемам параллельного обновления, поскольку имеет изменяемые записи, а значит, имеет побочный эффект.

В распределенных системах решением этой проблемы обычно является замена CRUD (Create, Read, Update, Delete) на CR, т.е. наложение ограничения на изменение (Update) и удаление (Delete) записей в хранилище, что получило распространение под термином Event Sourcing (существуют специализированные хранилища реализующие его, но он реализуется не обязательно специализированными инструментами).


Event Sourcing
==============

Если CQRS выражает принцип Императивного Программирования и отделяет действия (побочный эффект) от запроса (чтения) данных, то Event Sourcing идет еще дальше, и накладывает ограничение на изменение и удаление данных, превращая CRUD в CR.
Такой подход выражает принципы парадигмы Функционального Программирования при хранении данных, и предоставляет такие же выгоды: нет изменяемого состояния - нет проблемы параллельного обновления.
И такие же недостатки: потребность в большом количестве памяти и процессорной мощности.
Именно поэтому, данный шаблон широко используется в распределенных системах, где остро проявляется потребность в его достоинствах, и, вместе с тем, не проявляются его недостатки (ведь распределенные системы не лимитированы ни в памяти, ни в процессорной мощности).

Примером Event Sourcing может быть принцип организации банковского счета в базе данных, когда счет не является источником истины, а просто отражает совокупное значение всех транзакций (т.е. событий).

Наиболее ясно эта тема раскрывается в Chapter 6 "Functional Programming" of "Clean Architecture" by Robert C. Martin.

    Event Sourcing is naturally functional.
    It's an append only log of facts that have happened in the past.
    You can say that any projection any state is a left fold over your previous history.

    \- Greg Young, "`A Decade of DDD, CQRS, Event Sourcing <https://youtu.be/LDW0QWie21s?t=1004>`__" at 16:44

..

    I have always said that Event Sourcing is "Functional Data Storage".
    In this talk we will try migrating to a idiomatic functional way of looking at Event Sourcing.
    Come and watch all the code disappear!
    By the time you leave you will never want an "Event Sourcing Framework (TM)" ever again!

    \- Greg Young, "`Functional Data <https://vimeo.com/131636650>`__", NDC Conferences


Другие ссылки по теме
=====================

- "`CQRS <https://martinfowler.com/bliki/CQRS.html>`__"
- "`Event Sourcing <https://martinfowler.com/eaaDev/EventSourcing.html>`__"
- "`What do you mean by "Event-Driven"? <https://martinfowler.com/articles/201701-event-driven.html>`__"


Заключение
==========

Понимание общих признаков в способах управления Логикой Приложения позволяет проектировать более гибкие приложения, и, как результат, более безболезненно заменять архитектурный шаблон, например, из Layered в Event-Driven.
Частично эта тема затрагивается в Chapter 16 Independence of "Clean Architecture" by Robert C. Martin и в разделе "Premature Decomposition" of Chapter 3 "How to Model Services" of "Building Microservices" by Sam Newman.

