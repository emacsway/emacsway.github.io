
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

Не так давно у меня состоялась весьма конструктивная дискуссия с одним довольно грамотным парнем - `Viktor Turskyi (@koorchik) <https://twitter.com/koorchik>`__.
Эта дискуссия позволила мне систематизировать и обобщить свои знания.
Выводы этой систематизации оказались заслуживающими отдельного блог-поста.

Прежде чем копнуть вглубь, было бы неплохо разобраться с тем, что такое Application Logic (Логика Приложения) и чем она отличается от Business Logic (Бизнес-Логики).

Одно из наиболее часто-цитируемых определений:

    User Interface (or Presentation Layer)
        Responsible for showing information to the user and interpreting the user's
        commands. The external actor might sometimes be another computer
        system rather than a human user.
    Application Layer
        Defines the jobs the software is supposed to do and directs the expressive
        domain objects to work out problems. The tasks this layer is responsible
        for are meaningful to the business or necessary for interaction with the
        application layers of other systems.
        This layer is kept thin. It **does not contain Business Rules** or knowledge, but
        only coordinates tasks and delegates work to collaborations of domain
        objects in the next layer down. It does not have state reflecting the
        business situation, but it can have state that reflects the progress of a task
        for the user or the program.
    Domain Layer (or Model Layer)
        Responsible for representing concepts of the business, information about
        the **business situation, and Business Rules**. State that reflects the business
        situation is controlled and used here, even though the technical details of
        storing it are delegated to the infrastructure. This layer is the heart of
        business software.
    Infrastructure Layer
        Provides generic technical capabilities that support the higher layers:
        message sending for the application, persistence for the domain, drawing
        widgets for the UI, and so on. The infrastructure layer may also support
        the pattern of interactions between the four layers through an
        architectural framework.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" by Eric Evans

Но что означает сам термин Business?
Непонимание этого термина часто приводит к серьезным проблемам проектирования.
В это трудно поверить, но большинство разработчиков этого не понимают.


Что такое Business Rules (Бизнес Логика)
========================================

Самое авторитетное пояснение термина `Business <http://wiki.c2.com/?CategoryBusiness>`__ можно найти, как обычно, на сайте Ward Cunningham:

    Software intersects with the Real World. Imagine that.


Термина `Business Rule <http://wiki.c2.com/?BusinessRule>`__:

    A Business Rule (in a programming context) is knowledge that gets applied to a set of data to create new value. Or it may be a rule about how to create, modify, or remove data. Or perhaps it is a rule that specifies when certain processes occur.

    For example, we have a rule about email addresses -- when the Driver Name field on our object identifier changes, we erase the email address. When we receive a new email address, we make sure that it contains an "@" sign and a valid domain not on our blacklist.


`Business Logic Definition <http://wiki.c2.com/?BusinessLogicDefinition>`__:

    Business logic is that portion of an enterprise system which determines how data is:

    - Transformed and/or calculated. For example, business logic determines how a tax total is calculated from invoice line items.
    - Routed to people or software systems, aka workflow.


Следует отличать термин Business (по сути - синоним слова Domain) от термина `Business Domain <http://wiki.c2.com/?CategoryBusinessDomain>`__:

    A category about the business domain, such as accounting, finance, inventory, marketing, tracking, billing, reporting, charting, taxes, etc.


Также следует отличать Business и от `Business Process <http://wiki.c2.com/?BusinessProcess>`__:

    A Business Process is some reproduceable process within an organization. Often it is a something that you want to setup once and reuse over and over again.

    Companies spend a lot of time and money identifying Business Processes, designing the software that captures a Business Process and then testing and documenting these processes.

    One example of a Business Process is "Take an order on my web site". It might involve a customer, items from a catalog and a credit card. Each of these things is represented by business objects and together they represent a Business Process.


Википедия `дает следующее определение термину Business Logic <https://en.wikipedia.org/wiki/Business_logic>`__:

    In computer software, business logic or domain logic is the part of the program that encodes the real-world Business Rules that determine how data can be created, stored, and changed. It is contrasted with the remainder of the software that might be concerned with lower-level details of managing a database or displaying the user interface, system infrastructure, or generally connecting various parts of the program. 


Резюмируя, я обобщу все своими словами:

Бизнес-Логика (деловые регламенты, доменные модели)
    \- это моделирование объектов и процессов предметной области (т.е. реального мира).
    Это то, что программа должна делать (от слова "дело" - именно так переводится слово "business"), и ради чего она создается.
Логика приложения
    \- это то, что обеспечивает и координирует работу Бизнес-Логики.


Надо заметить, что существуют еще и application-specific Business Rules.

Robert Martin в Clean Architecture разделяет Бизнес-Правила на два вида:

- application-specific Business Rules
- application-independent Business Rules

    Thus we find the system divided into decoupled horizontal layers—the UI, application-specific Business Rules, application-independent Business Rules, and the database, just to mention a few.

    То есть систему можно разделить на горизонтальные уровни: пользовательский интерфейс, Бизнес-Правила, характерные для приложения, Бизнес-Правила, не зависящие от приложения, и база данных — кроме всего прочего.

    \- Clean Architecture by Robert Martin

Главы 16, 20 и 22 of Clean Architecture разъясняют в подробностях типы Бизнес-Правил.


Почему важно отделять Business Rules от Application Logic?
==========================================================

Поскольку целью создания приложения является реализация именно Business Logic - критически важно обеспечить их переносимость, и отделить их от Application Logic.
Это потому, что Логика Приложения будет меняться с другой частотой и по другим причинам.


Способы организации Application Logic (Логики Приложения)
=========================================================

Широко распространены три способа организации Application Logic:

1. `Service Layer (сервисный слой) <https://martinfowler.com/eaaCatalog/serviceLayer.html>`__.
Который, в свою очередь, делится на Оркестровый ("запрос-ответ", т.е. сервис осведомлен об интерфейсе других сервисов) и Хореографический (Event-Driven, т.е. loosely coupled).

Последний является разновидностью паттерна Command, и используется в CQRS-приложениях (reducers в Redux - наглядный пример).

Подробней оркестровые Сервисные Слои рассматриваются в статье

- ":doc:`./service-layer`",

а хореографические - в статье

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

    it allows us to host the two services differently eg: we can host the read service on 25 servers and the write service on two.
    The processing of commands and queries is fundamentally asymmetrical, and scaling the services symmetrically does not make a lot of sense.

    \- `CQRS, Task Based UIs, Event Sourcing agh! <http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/>`__ by Greg Young

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


Другие ссылки по теме
=====================

- `CQRS <https://martinfowler.com/bliki/CQRS.html>`__
- `Event Sourcing <https://martinfowler.com/eaaDev/EventSourcing.html>`__
- `What do you mean by "Event-Driven"? <https://martinfowler.com/articles/201701-event-driven.html>`__


Заключение
==========

Понимание общих признаков в способах управления Логикой Приложения позволяет проектировать более гибкие приложения, и, как результат, более безболезненно заменять архитектурный шаблон, например, из Layered в Event-Driven.
Частично эта тема затрагивается в Chapter 16 Independence of "Clean Architecture" by Robert C. Martin и в разделе "Premature Decomposition" of Chapter 3 "How to Model Services" of "Building Microservices" by Sam Newman.

