
Проектирование Сервисного Слоя и Логики Приложения
==================================================

.. post:: Jul 17, 2017
   :language: ru
   :tags: Design, Architecture, ORM, Django Model, Service Layer, Redux, Flux, Model, CQRS, Event Sourcing
   :category:
   :author: Ivan Zakrevsky
   :redirect: ru/redux-and-flux-for-oop-programmers, ru/application-logic-management

Эта статья посвящена вопросам управления Логикой Приложения и проектированию Сервисного Слоя (`Service Layer`_), Use Case, CQRS, Event Sourcing, MVC и др.


.. contents:: Содержание


Виды логики
===========

Прежде чем копнуть вглубь, было бы неплохо разобраться с тем, что такое Логика Приложения (Application Logic) и чем она отличается от Бизнес-Логики (Business Logic).


Layered Architecture
--------------------

Одно из наиболее часто-цитируемых определений основных концептуальных слоев дает Eric Evans:

    **User Interface (or Presentation Layer)**
        Responsible for showing information to the user and interpreting the user's
        commands. The external actor might sometimes be another computer
        system rather than a human user.
    **Application Layer**
        Defines the jobs the software is supposed to do and directs the expressive
        domain objects to work out problems. The tasks this layer is responsible
        for are meaningful to the business or necessary for interaction with the
        application layers of other systems.
        This layer is kept thin. It **does not contain business rules** or knowledge, but
        only coordinates tasks and delegates work to collaborations of domain
        objects in the next layer down. It does not have state reflecting the
        business situation, but it can have state that reflects the progress of a task
        for the user or the program.
    **Domain Layer (or Model Layer)**
        Responsible for representing concepts of the business, information about
        the **business situation, and business rules**. State that reflects the business
        situation is controlled and used here, even though the technical details of
        storing it are delegated to the infrastructure. This layer is the heart of
        business software.
    **Infrastructure Layer**
        Provides generic technical capabilities that support the higher layers:
        message sending for the application, persistence for the domain, drawing
        widgets for the UI, and so on. The infrastructure layer may also support
        the pattern of interactions between the four layers through an
        architectural framework.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_ by Eric Evans

Но что означает сам термин Бизнес (Business)?
Непонимание этого термина часто приводит к серьезным проблемам проектирования.
В это трудно поверить, но большинство разработчиков, даже с многолетним стажем, этого не понимают, и полагают что это что-то связанное с финансами.


Что такое Бизнес-Логика (Business Logic)?
------------------------------------------

Самое авторитетное пояснение термина `Business <http://wiki.c2.com/?CategoryBusiness>`__ можно найти, как обычно, на сайте Ward Cunningham:

    Software intersects with the Real World. Imagine that.


Там же можно найти и определение термина `Business Rule <http://wiki.c2.com/?BusinessRule>`__:

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

**Бизнес-Логика (деловые регламенты, доменные модели)** -
    это моделирование объектов и процессов предметной области (т.е. реального мира).
    Это то, что программа должна делать (от слова "дело" - именно так переводится слово "business"), и ради чего она создается.
**Логика приложения** -
    это то, что обеспечивает и координирует работу Бизнес-Логики.


Подвиды Бизнес-Правил (Business Rules)
--------------------------------------

Robert Martin в "Clean Architecture" подразделяет Бизнес-Правила на два вида:

- Application-specific Business Rules
- Application-independent Business Rules

    То есть систему можно разделить на горизонтальные уровни: пользовательский интерфейс, Бизнес-Правила, характерные для приложения, Бизнес-Правила, не зависящие от приложения, и база данных — кроме всего прочего.

    Thus we find the system divided into decoupled horizontal layers—the UI, application-specific Business Rules, application-independent Business Rules, and the database, just to mention a few.

    \- "Clean Architecture" by Robert Martin

Главы 16, 20 и 22 of Clean Architecture разъясняют в подробностях типы Бизнес-Правил.

И, хотя, Robert Martin выделяет отдельную категорию классов UseCase (Interactor) для Application-specific Business Rules, на практике этот уровень часто округляется до уровня Application Logic.
Так, например, Martin Fowler и Randy Stafford разделяют "Business Logic" на два вида - Логика Домена (Domain Logic) и Логика Приложения (Application Logic):

    Подобно сценарию транзакции (Transaction Script, 133) и модели предметной области
    (Domain Model, 140), слой служб представляет собой типовое решение по организации
    бизнес-логики. Многие проектировщики, и я в том числе, любят разносить **бизнес-логику**
    по двум категориям: логика домена (domain logic) имеет дело только с предметной
    областью как таковой (примером могут служить стратегии вычисления зачтенного дохода
    по контракту), а логика приложения (application logic) описывает сферу ответственности
    приложения [11] (скажем, уведомляет пользователей и сторонние приложения о протекании
    процесса вычисления доходов). Логику приложения часто называют также
    "логикой рабочего процесса", несмотря на то что под "рабочим процессом" часто понимаются
    совершенно разные вещи.

    Like Transaction Script (110) and Domain Model (116), Service Layer is a pattern for organizing **business logic**.
    Many designers, including me, like to divide "**business logic**" into two kinds: "domain logic," having to
    do purely with the problem domain (such as strategies for calculating revenue recognition on a contract), and
    "application logic," having to do with application responsibilities [Cockburn UC] (such as notifying contract
    administrators, and integrated applications, of revenue recognition calculations). Application logic is
    sometimes referred to as "workflow logic," although different people have different interpretations of
    "workflow."

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_ by Martin Fowler, Randy Stafford

Местами он склонен относить "Business Rules" к Доменой Логике (Domain Logic):

    Проблемы возникли с усложнением доменой логики - бизнес-правил, алгоритмов вычислений, условий проверок и т.д.

    The problem came with domain logic: business rules, validations, calculations, and the like.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_ by Martin Fowler

И даже признает наличие определенной расплывчатости:

    Не стоит забывать и о том, что принято обозначать расплывчатым термином бизнес-логика.
    Я нахожу его забавным, поскольку могу припомнить только несколько вещей, менее логичных, нежели так называемая бизнес-логика.

    Then there's the matter of what comes under the term "business logic."
    I find this a curious term because there are few things that are less logical than business logic.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_ by Martin Fowler


Почему важно отделять Business Rules от Application Logic?
----------------------------------------------------------

Поскольку целью создания приложения является реализация именно Business Rules - критически важно обеспечить их переносимость, и отделить их от Application Logic.
Эти два вида логики будут изменяться в разное время, с разной частотой и по разным причинам, поэтому их следует разделить
так, чтобы их можно было изменять независимо [#fncarch]_ .
В свое время Гради Буч сказал, что "Архитектура отражает важные проектные решения по формированию системы, где важность определяется стоимостью изменений" [#fncarch]_ .


Способы организации Логики Приложения (Application Logic)
=========================================================

Широко распространены четыре способа организации Логики Приложения (Application Logic):

1. Оркестровый Сервис ("request/response", т.е. сервис осведомлен об интерфейсе других сервисов), он же - Сервисный Слой (Service Layer).

2. Хореографический Сервис (Event-Driven, т.е. loosely coupled), который является разновидностью паттерна Command, и используется, как правило, в Event-Driven Architecture (в частности, в CQRS и Event Sourcing приложениях, наглядный пример - reducer в Redux), и в DDD-приложениях (обработчик Domain/Integration Event).

3. `Front Controller <https://martinfowler.com/eaaCatalog/frontController.html>`__ и `Application Controller <https://martinfowler.com/eaaCatalog/applicationController.html>`__ (которые тоже, по сути, является разновидностью паттерна Command).

..

    "A Front Controller handles all calls for a Web site, and is usually structured in two parts: a Web handler and a command hierarchy."

    \- "Patterns of Enterprise Application Architecture"  [#fnpoeaa]_ by Martin Fowler and others.

..

    "For both the domain commands and the view, the application controller needs a way to store something it can invoke.
    A Command [Gang of Four] is a good choice, since it allows it to easily get hold of and run a block of code."

    \- "Patterns of Enterprise Application Architecture"  [#fnpoeaa]_ by Martin Fowler and others.

4. `Use Case <https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html>`__, который также, является разновидностью паттерна Command.
На 15:50 Robert C. Martin проводит `параллель между Use Case и паттерном Command <https://youtu.be/Nsjsiz2A9mg?t=15m45s>`__.

Собственно говоря, производной паттерна Command является даже `Method Object <https://refactoring.com/catalog/replaceFunctionWithCommand.html>`__.

Use Case обязан своим существованием именно наличию Бизнес-Логики, которая  application specific, и не имеет смысла вне контекста приложения.
Он обеспечивает независимость этих application-specific Business Rules от приложения путем инверсии контроля (IoC).

Если бы Use Case не содержал Бизнес-Логики, то не было бы и смысла отделять его от Page Controller, иначе приложение пыталось бы абстрагироваться от самого себя же.

Мы видим, что в организации Логики Приложения широко применяются разновидности паттерна Команда (Command).

Рассмотренные способы организовывают, в первую очередь, Логику Приложения, и лишь во вторую очередь, Бизнес-Логику, которая не обязательно должна присутствовать, кроме случая использования Use Case, т.к. иначе он утратил бы причины для существования.

При правильной организации Бизнес-Логики, и высоком качестве ORM (в случае его использования, конечно же), зависимость Бизнес-Логики от приложения будет минимальна.
Основная сложность любого ORM заключается в том, чтобы организовать доступ к связанным объектам не подмешивая Логику Приложения (и логику доступа к данным) в Domain Models, - эту тему мы подробно рассмотрим в одном из следующих постов.

Понимание общих признаков в способах управления Логикой Приложения позволяет проектировать более гибкие приложения, и, как результат, более безболезненно заменять архитектурный шаблон, например, из Layered в Event-Driven.
Частично эта тема затрагивается в Chapter 16 "Independence" of "Clean Architecture" by Robert C. Martin и в разделе "Premature Decomposition" of Chapter 3 "How to Model Services" of "Building Microservices" by Sam Newman.


Что такое Сервис?
=================

    SERVICE - An operation offered as an interface that stands alone in the model, with no encapsulated state.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_

..

    In some cases, the clearest and most pragmatic design includes operations that do not
    conceptually belong to any object. Rather than force the issue, we can follow the natural contours
    of the problem space and include SERVICES explicitly in the model.

    There are important domain operations that can't find a natural home in an ENTITY or VALUE
    OBJECT . Some of these are intrinsically activities or actions, not things, but since our modeling
    paradigm is objects, we try to fit them into objects anyway...

    A SERVICE is an operation offered as an interface that stands alone in the model, without
    encapsulating state, as ENTITIES and VALUE OBJECTS do. S ERVICES are a common pattern in technical
    frameworks, but they can also apply in the domain layer.

    The name service emphasizes the relationship with other objects. Unlike ENTITIES and VALUE
    OBJECTS , it is defined purely in terms of what it can do for a client. A SERVICE tends to be named for
    an activity, rather than an entity—a verb rather than a noun. A SERVICE can still have an abstract,
    intentional definition; it just has a different flavor than the definition of an object. A SERVICE should
    still have a defined responsibility, and that responsibility and the interface fulfilling it should be
    defined as part of the domain model. Operation names should come from the UBIQUITOUS
    LANGUAGE or be introduced into it. Parameters and results should be domain objects.

    SERVICES should be used judiciously and not allowed to strip the ENTITIES and VALUE OBJECTS of all
    their behavior. But when an operation is actually an important domain concept, a SERVICE forms a
    natural part of a MODEL-DRIVEN DESIGN . Declared in the model as a SERVICE, rather than as a
    phony object that doesn't actually represent anything, the standalone operation will not mislead
    anyone.

    A good SERVICE has three characteristics.

    1. The operation relates to a domain concept that is not a natural part of an ENTITY or VALUE
    OBJECT .
    2. The interface is defined in terms of other elements of the domain model.
    3. The operation is stateless.

    Statelessness here means that any client can use any instance of a particular SERVICE without
    regard to the instance's individual history. The execution of a SERVICE will use information that is
    accessible globally, and may even change that global information (that is, it may have side
    effects). But the SERVICE does not hold state of its own that affects its own behavior, as most
    domain objects do.

    When a significant process or transformation in the domain is not a natural
    responsibility of an ENTITY or VALUE OBJECT, add an operation to the model as a
    standalone interface declared as a SERVICE. Define the interface in terms of the
    language of the model and make sure the operation name is part of the UBIQUITOUS
    LANGUAGE. Make the SERVICE stateless.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_


Классификация Сервисов по уровням логики
========================================

Eric Evans разделяет Сервисы на три уровня логики:

    Partitioning Services into Layers

    Application
        Funds Transfer App Service

        - Digests input (such as an XML request).
        - Sends message to domain service for fulfillment.
        - Listens for confirmation.
        - Decides to send notification using infrastructure service.
    Domain
        Funds Transfer Domain Service

        - Interacts with necessary Account and Ledger objects, making appropriate debits and credits.
        - Supplies confirmation of result (transfer allowed or not, and so on).
    Infrastructure Send Notification Service
        Sends e-mails, letters, and other communications as directed by the application.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_

..

    Most SERVICES discussed in the literature are purely technical and belong in the infrastructure layer.
    Domain and application SERVICES collaborate with these infrastructure SERVICES.
    For example, a bank might have an application that sends an e-mail to a customer when an account balance falls below a specific threshold.
    The interface that encapsulates the e-mail system, and perhaps alternate means of notification, is a SERVICE in the infrastructure layer.

    It can be harder to distinguish application SERVICES from domain SERVICES.
    The application layer is responsible for ordering the notification.
    The domain layer is responsible for determining if a threshold was met—though this task probably does not call for a SERVICE, because it would fit the responsibility of an "account" object.
    That banking application could be responsible for funds transfers.
    If a SERVICE were devised to make appropriate debits and credits for a funds transfer,that capability would belong in the domain layer.
    Funds transfer has a meaning in the banking domain language, and it involves fundamental business logic.
    Technical SERVICES should lack any business meaning at all.

    Many domain or application SERVICES are built on top of the populations of ENTITIES and VALUES, behaving like scripts that organize the potential of the domain to actually get something done.
    ENTITIES and VALUE OBJECTS are often too fine-grained to provide a convenient access to the capabilities of the domain layer.
    Here we encounter a very fine line between the domain layer and the application layer.
    For example, if the banking application can convert and export our transactions into a spreadsheet file for us to analyze, that export is an application SERVICE.
    There is no meaning of "file formats" in the domain of banking, and there are no business rules involved.

    On the other hand, a feature that can transfer funds from one account to another is a domain SERVICE because it embeds significant business rules (crediting and debiting the appropriate accounts, for example) and because a "funds transfer" is a meaningful banking term.
    In this case, the SERVICE does not do much on its own; it would ask the two Account objects to do most of the work.
    But to put the "transfer" operation on the Account object would be awkward, because the operation involves two accounts and some global rules.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_

..

    Модель предметной области более предпочтительна в сравнении со сценарием транзакции,
    поскольку исключает возможность дублирования бизнес-логики и позволяет
    бороться со сложностью с помощью классических проектных решений.
    Но размещение логики приложения в "чистых" классах домена чревато нежелательными последствиями.
    Во-первых, классы домена допускают меньшую вероятность повторного использования,
    если они реализуют специфическую логику приложения и зависят от тех или иных прикладных
    инструментальных пакетов.
    Во-вторых, смешивание логики обеих категорий в контексте одних и тех же классов затрудняет возможность новой реализации логики
    приложения с помощью специфических инструментальных средств, если необходимость
    такого шага становится очевидной.
    По этим причинам слой служб предусматривает распределение "разной" логики по отдельным слоям, что обеспечивает традиционные
    преимущества расслоения, а также большую степень свободы применения классов домена
    в разных приложениях.

    Domain Models (116) are preferable to Transaction Scripts (110) for avoiding domain logic duplication and
    for managing complexity using classical design patterns.
    But putting application logic into pure domain object classes has a couple of undesirable consequences.
    First, domain object classes are less reusable across applications if they implement application-specific logic and depend on application-specific packages.
    Second, commingling both kinds of logic in the same classes makes it harder to reimplement the application
    logic in, say, a workflow tool if that should ever become desirable.
    For these reasons Service Layer factors each kind of business logic into a separate layer, yielding the usual benefits of layering and rendering the pure domain object classes more reusable from application to application.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_


Сервисы уровня Доменной Логики (Domain Logic)
---------------------------------------------

Политика самого высокого уровня принадлежит Доменной Логике (Domain Logic), поэтому, с нее и начнем.
К счастью, это самый немногочисленный представитель Сервисов.

Подробно тему Сервисов Логики Предметной Области и причины их существования раскрывает Vaughn Vernon:

    Further, don’t confuse a Domain Service with an Application Service.
    We don’t want to house business logic in an Application Service, but we do want business logic housed in a Domain Service.
    If you are confused about the difference, compare with Application.
    Briefly, to differentiate the two, an Application Service, being the natural client of the domain model, would normally be the client of a Domain Service.
    You’ll see that demonstrated later in the chapter.
    Just because a Domain Service has the word service in its name does not mean that it is required to be a coarse-grained, remote-capable, heavyweight transactional operation.

    ...

    You can use a Domain Service to

    - Perform a significant business process
    - Transform a domain object from one composition to another
    - Calculate a Value requiring input from more than one domain object

    \- "Implementing Domain-Driven Design" by Vaughn Vernon


Сервисы уровня Логики Приложения (Application Logic)
----------------------------------------------------

Это самый многочисленный представитель Сервисов.
Именно его часто называют Сервисный Слой (Service Layer).


Сервисы уровня Инфраструктурного Слоя (Infrastructure Layer)
------------------------------------------------------------

Отдельно следует выделять Сервисы уровня Инфраструктурного Слоя (Infrastructure Layer).

    The infrastructure layer usually does not initiate action in the domain layer. Being "below" the
    domain layer, it should have no specific knowledge of the domain it is serving. Indeed, such
    technical capabilities are most often offered as SERVICES . For example, if an application needs to
    send an e-mail, some message-sending interface can be located in the infrastructure layer and the
    application layer elements can request the transmission of the message. This decoupling gives
    some extra versatility. The message-sending interface might be connected to an e-mail sender, a
    fax sender, or whatever else is available. But the main benefit is simplifying the application layer,
    keeping it narrowly focused on its job: knowing when to send a message, but not burdened with
    how.

    The application and domain layers call on the SERVICES provided by the infrastructure layer. When
    the scope of a SERVICE has been well chosen and its interface well designed, the caller can remain
    loosely coupled and uncomplicated by the elaborate behavior the SERVICE interface encapsulates.

    But not all infrastructure comes in the form of SERVICES callable from the higher layers. Some
    technical components are designed to directly support the basic functions of other layers (such as
    providing an abstract base class for all domain objects) and provide the mechanisms for them to
    relate (such as implementations of MVC and the like). Such an "architectural framework" has
    much more impact on the design of the other parts of the program.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_

..

    Infrastructure Layer - Provides generic technical capabilities that support the higher layers:
    message sending for the application, persistence for the domain, drawing
    widgets for the UI, and so on. The infrastructure layer may also support
    the pattern of interactions between the four layers through an
    architectural framework.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_


Классификация Сервисов по способу взаимодействия
================================================

По способу взаимодействия Сервисы разделяются на `Оркестровые <https://en.wikipedia.org/wiki/Orchestration_(computing)>`__ ("request/response", т.е. сервис осведомлен об интерфейсе других сервисов) и `Хореографические <https://en.wikipedia.org/wiki/Service_choreography>`__ (Event-Driven, т.е. loosely coupled) [#fnbm]_.
Их еще называют идиоматическими стилями взаимодействия.
Главный недостаток первого - это высокая осведомленность об интерфейсе других Сервисов, т.е. Высокое Сопряжение (High Coupling), что снижает их реиспользование.
Последний же является разновидностью паттерна Command, и используется, как правило, в Event-Driven Architecture (в частности, в CQRS и Event Sourcing приложениях, наглядный пример - reducer в Redux), и в DDD-приложениях (обработчик Domain/Integration Event).


Оркестровые Сервисы
-------------------

Оркестровые Сервисы являются представителями классического Сервисного Слоя, и подробнее рассматриваются ниже по тексту.


Хореографические Сервисы
------------------------

Существует интересная статья "`Clarified CQRS <http://udidahan.com/2009/12/09/clarified-cqrs/>`__" by Udi Dahan, на которую ссылается Martin Fowler в своей статье "`CQRS <https://martinfowler.com/bliki/CQRS.html>`__".

И в этой статье есть интересный момент.

    The reason you don’t see this layer explicitly represented in CQRS is that it isn’t really there...

    \- "Clarified CQRS" by Udi Dahan

На самом деле, обработчик команды - это и есть Сервис, только событийно-ориентированный, который следует заданному интерфейсу.
Он должен содержать логику уровня приложения (а не бизнес-логику).

    Our command processing objects in the various autonomous components actually make up our service layer.

    \- "Clarified CQRS" by Udi Dahan

Хореографические Сервисы бывают только уровня Логики Приложения, даже если они подписаны на Доменные События (Domain Event).


Частые ошибки проектирования Хореографических Сервисов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Иногда, особенно у frontend-разработчиков, можно наблюдать как они проксируют Оркестровыми Сервисами обращения к Хореографическим Сервисам.
Часто это происходит при использовании Redux/NgRx в Angular-приложении, в котором широко используются Сервисы.
Имея слабо-сопряженные (Low Coupling) событийно-ориентированные Сервисы в виде обработчиков команды, было бы проектной ошибкой пытаться связать их в сильно-зацепленные (High Coupling) классические Сервисы Оркестрового типа (с единственной целью - помочь Логике Приложения скрыть их от самой же себя).

   Each command is independent of the other, so why should we allow the objects which handle them to depend on each other?

   \- "Clarified CQRS" by Udi Dahan


Тут, правда, возникает вопрос осведомленности обработчиков команды и самого приложения об интерфейсе конкретной реализации CQRS.
Для выравнивания интерфейсов служит паттерн Adapter, которому, при необходимости, можно предусмотреть место.

Другой распространенной ошибкой является размещение Бизнес-Логики в Хореографических Сервисах и искусственное вырождение поведения Доменных Моделей с выносом всей бизнес-логики в обработчики команд, т.е. в Сервисы.

Это приводит к появлению проблемы, о которой говорил Eric Evans:

    "Если требования архитектурной среды к распределению обязанностей таковы, что элементы, реализующие концептуальные объекты, оказываются физически разделенными, то код больше не выражает модель.

    Нельзя разделять до бесконечности, у человеческого ума есть свои пределы, до которых он еще способен соединять разделенное;
    если среда выходит за эти пределы, разработчики предметной области теряют способность расчленять модель на осмысленные фрагменты."

    "If the framework's partitioning conventions pull apart the elements implementing the
    conceptual objects, the code no longer reveals the model.

    There is only so much partitioning a mind can stitch back together, and if the framework uses 
    it all up, the domain developers lose their ability to chunk the model into meaningful pieces."

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" by Eric Evans

В приложениях с обширной бизнес-логикой это может сильно ухудшить качество бизнес-моделирования, и препятствовать процессу дистилляции моделей по мере переработки бизнес-знаний [#fnddd]_.
Также такой код обретает признаки "Divergent Change" [#fnr]_ и "Shotgun Surgery" [#fnr]_, что сильно затрудняет исправление ошибок бизнес-моделирования и Итерационное Проектирование (Evolutionary Design).
В конечном итоге это приводит к стремительному росту стоимости изменения программы.

Должен заметить, что Udi Dahan в своей статье допускает и использование `Transaction Script <https://martinfowler.com/eaaCatalog/transactionScript.html>`__ для организации бизнес-логики.
В таком случае, выбор между Transaction Script и `Domain Model <https://martinfowler.com/eaaCatalog/domainModel.html>`__ подробно рассмотрен в "Patterns of Enterprise Application Architecture" by M. Fowler and others.
Transaction Script может быть уместным при сочетании Redux и GraphQL для минимизации сетевого трафика.
При использовании же REST-API, и наличии обширной бизнес-логики, более уместным будет использование Domain Model и DDD.


Классификация Сервисов по способу обмена данными
================================================

По способу обмена данными Сервисы разделяются на Синхронные и Асинхронные.


Классификация Сервисов по состоянию
===================================


Stateless Service
-----------------

Как правило, большинство сервисов являются stateless, т.е. не имеют состояния.
Они хорошо изучены, и добавить по ним нечего.


Statefull Service
-----------------

Классы UseCases/Interactors [#fncarch]_ являются разновидностью паттерна Команда (Command), и, в определенной мере, могут рассматриваться как Statefull Сервис.

Похожую идею выражает и Eric Evans:

    We might like to create a Funds Transfer object to represent the two entries plus the rules and history around the transfer. But we are still left with calls to SERVICES in the interbank networks.
    What's more, in most development systems, it is awkward to make a direct interface between a domain object and external resources. We can dress up such external SERVICES with a FACADE that takes inputs in terms of the model, perhaps returning a Funds Transfer object as its result.
    But whatever intermediaries we might have, and even though they don't belong to us, those SERVICES are carrying out the domain responsibility of funds transfer.

    \- "Domain-Driven Design: Tackling Complexity in the Heart of Software" [#fnddd]_

И Randy Stafford с Martin Fowler:

    Двумя базовыми вариантами реализации слоя служб являются создание интерфейса
    доступа к домену (domain facade) и конструирование сценария операции (operation script).
    При использовании подхода, связанного с интерфейсом доступа к домену, слой служб
    реализуется как набор "тонких" интерфейсов, размещенных "поверх" модели предметной
    области. В классах, реализующих интерфейсы, никакая бизнес-логика отражения не
    находит — она сосредоточена исключительно в контексте модели предметной области.
    Тонкие интерфейсы устанавливают границы и определяют множество операций, посредством
    которых клиентские слои взаимодействуют с приложением, обнаруживая тем самым
    характерные свойства слоя служб.

    Создавая сценарий операции, вы реализуете слой служб как множество более "толстых"
    классов, которые непосредственно воплощают в себе логику приложения, но за бизнес-логикой
    обращаются к классам домена. Операции, предоставляемые клиентам слоя
    служб, реализуются в виде сценариев, создаваемых группами в контексте классов, каждый
    из которых определяет некоторый фрагмент соответствующей логики. Подобные
    классы, расширяющие супертип слоя (Layer Supertype, 491) и уточняющие объявленные
    в нем абстрактные характеристики поведения и сферы ответственности, формируют "службы"
    приложения (в названиях служебных типов принято употреблять суффикс "Service").
    Слой служб и заключает в себе эти прикладные классы.

    The two basic implementation variations are the domain facade approach and the operation script approach. In
    the domain facade approach a Service Layer is implemented as a set of thin facades over a Domain Model
    (116). The classes implementing the facades don't implement any business logic. Rather, the Domain Model
    (116) implements all of the business logic. The thin facades establish a boundary and set of operations through
    which client layers interact with the application, exhibiting the defining characteristics of Service Layer.

    In the operation script approach a Service Layer is implemented as a set of thicker classes that directly
    implement application logic but delegate to encapsulated domain object classes for domain logic. The
    operations available to clients of a Service Layer are implemented as scripts, organized several to a class
    defining a subject area of related logic. Each such class forms an application "service," and it's common for
    service type names to end with "Service." A Service Layer is comprised of these application service classes,
    which should extend a Layer Supertype (475), abstracting their responsibilities and common behaviors.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_ by Martin Fowler, Randy Stafford


Обратите внимание на использование термина "`Domain Model`_".
Эти ребята - последние из числа тех, кто может спутать "`Domain Model`_" и "`DataMapper`_", особенно, при таком количестве редакторов и рецензентов.
Т.е. клиент ожидает от доменной модели интерфейс, который она, по какой-то причине (обычно это Single Responsibility Principle), не реализует и не должна реализовать.
С другой стороны, клиент не может реализовать это поведение сам, так как это привело бы к появлению "G14: Feature Envy" [#fnccode]_.
Для выравнивания интерфейсов служит паттерн Adapter (aka Wrapper), см. "Design Patterns Elements of Reusable Object-Oriented Software" [#fngof]_.
Отличается Statefull Services от обычного Adapter только тем, что он содержит логику более низкого уровня, т.е. Логику Приложения (Application Logic), нежели Доменная Модель.

Этот подход сильно напоминает мне "Cross-Cutting Concerns" [#fnccode]_ с тем только отличием, что "Cross-Cutting Concerns" реализует интерфейс оригинального объекта, в то время как domain facade дополняет его.
Когда объект-обертка реализует интерфейс оригинального объекта, то его обычно называют Aspect или Decorator.
Часто в таких случаях можно услышать термин Proxy, но, на самом деле паттерн Proxy имеет немного другое назначение.
Такой подход часто используется для того, чтобы наделить Доменную Модель логикой доступа к связанным объектам, при этом сохраняя Доменную Модель совершенно "чистой", т.е. отделенной от поведения логики более низкого уровня.

При работе с унаследованным кодом мне доводилось встречать разбухшие Доменные Модели с огромным числом методов (я встречал до нескольких сотен методов).
При анализе таких моделей часто обнаруживаются посторонние обязанности в классе, а размер класса, как известно, измеряется количеством его обязанностей.
Statefull Сервисы и паттерн Adapter - хорошая альтернатива для того, чтобы вынести из модели несвойственные ей обязанности, и заставить похудеть разбухшие модели.


Назначение Сервисного Слоя
==========================

    Слой служб устанавливает множество доступных действий и координирует отклик приложения на каждое действие.

    A Service Layer defines an application's boundary with a layer of services that establishes a set of available
    operations and coordinates the application's response in each operation.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

..

    Корпоративные приложения обычно подразумевают применение разного рода интерфейсов к хранимым данным и реализуемой логике — загрузчиков данных, интерфейсов пользователя, шлюзов интеграции и т.д.
    Несмотря на различия в назначении, подобные интерфейсы часто нуждаются в одних и тех же функциях взаимодействия с приложением для манипулирования данными и выполнения бизнес-логики.
    Функции могут быть весьма сложными и способны включать транзакции, охватывающие многочисленные ресурсы, а также операции по координации реакций на действия.
    Описание логики взаимодействия в каждом отдельно взятом интерфейсе сопряжено с многократным повторением одних и тех же фрагментов кода.

    Слой служб определяет границы приложения и множество операций, предоставляемых им для интерфейсных клиентских слоев кода.
    Он инкапсулирует бизнес-логику приложения, управляет транзакциями и координирует реакции на действия.

    Enterprise applications typically require different kinds of interfaces to the data they store and the logic they implement: data loaders, user interfaces, integration gateways, and others.
    Despite their different purposes, these interfaces often need common interactions with the application to access and manipulate its data and invoke its business logic.
    The interactions may be complex, involving transactions across multiple resources and the coordination of several responses to an action.
    Encoding the logic of the interactions separately in each interface causes a lot of duplication.

    A Service Layer defines an application's boundary and its set of available operations from the perspective of interfacing client layers.
    It encapsulates the application's business logic, controlling transactions and coordinating responses in the implementation of its operations.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

..

    Преимуществом использования слоя служб является возможность определения набора
    общих операций, доступных для применения многими категориями клиентов, и координация
    откликов приложения на выполнение каждой операции. В сложных случаях
    отклики могут включать в себя логику приложения, передаваемую в рамках атомарных
    транзакций с использованием нескольких ресурсов. Таким образом, если у бизнес-логики
    приложения есть более одной категории клиентов, а отклики на варианты
    использования передаются через несколько ресурсов транзакций, использование слоя
    служб с транзакциями, управляемыми на уровне контейнера, становится просто необходимым,
    даже если архитектура приложения не является распределенной.

    The benefit of Service Layer is that it defines a common set of application operations available to many kinds
    of clients and it coordinates an application's response in each operation. The response may involve application
    logic that needs to be transacted atomically across multiple transactional resources. Thus, in an application
    with more than one kind of client of its business logic, and complex responses in its use cases involving
    multiple transactional resources, it makes a lot of sense to include a Service Layer with container-managed
    transactions, even in an undistributed architecture.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

..

    Один из общих подходов к реализации бизнес-логики состоит в расщеплении слоя
    предметной области на два самостоятельных слоя: "поверх" модели предметной области
    или модуля таблицы располагается слой служб (Service Layer, 156). Обычно это целесообразно
    только при использовании модели предметной области или модуля таблицы, поскольку
    слой домена, включающий лишь сценарий транзакции, не настолько сложен,
    чтобы заслужить право на создание дополнительного слоя. Логика слоя представления
    взаимодействует с бизнес-логикой исключительно при посредничестве слоя служб, который
    действует как API приложения.

    Поддерживая внятный интерфейс приложения (API), слой служб подходит также для
    размещения логики управления транзакциями и обеспечения безопасности. Это дает
    возможность снабдить подобными характеристиками каждый метод слоя служб. Для таких
    целей обычно применяются файлы свойств, но атрибуты .NET предоставляют удобный
    способ описания параметров непосредственно в коде.

    A common approach in handling domain logic is to split the domain layer in two. A Service Layer (133) is
    placed over an underlying Domain Model (116) or Table Module (125). Usually you only get this with a
    Domain Model (116) or Table Module (125) since a domain layer that uses only Transaction Script (110) isn't
    complex enough to warrant a separate layer. The presentation logic interacts with the domain purely through
    the Service Layer (133), which acts as an API for the application.

    As well as providing a clear API, the Service Layer (133) is also a good spot to place such things as
    transaction control and security. This gives you a simple model of taking each method in the Service Layer
    (133) and describing its transactional and security characteristics. A separate properties file is a common
    choice for this, but .NET's attributes provide a nice way of doing it directly in the code.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

Традиционно Сервисный Слой относится к логике уровня Приложения.
Т.е. Сервисный Слой имеет более низкий уровень, чем слой предметной области (domain logic), именуемый так же деловыми регламентами (business rules).
Из этого также следует и то, что объекты предметной области не должны быть осведомлены о наличии Сервисного Слоя.

Кроме перечисленного выше, сервисный слой может выполнять следующие обязанности:

- Компоновки атомарных операций (например, требуется одновременно сохранить данные в БД, редисе, и на файловой системе, в рамках одной бизнес-транзакции, или откатить все назад).
- Сокрытия источника данных (здесь он дублирует функции паттерна `Repository`_) и может быть опущен, если нет других причин.
- Компоновки реиспользуемых операций уровня приложения (например, некая часть логики уровня приложения используется в нескольких различных контроллерах).
- Как основа для реализации `Интерфейса удаленного доступа <Remote Facade_>`__.
- Когда контроллер имеет какой-то большой метод, он нуждается в декомпозиции, и к нему применяется `Extract Method`_ для вычленения обязанностей в отдельные методы. При этом растет количество методов класса, что влечет за собой падение его сфокусированности или `Связанности <Cohesion_>`__ (т.е. коэффициент совместного использования свойств класса его методами). Чтобы восстановить связанность, эти методы выделяются в отдельный класс, образуя `Method Object <Replace Method with Method Object_>`__. И вот этот метод-объект и может быть преобразован в сервисный слой.
- Сервисный слой можно использовать в качестве концентратора запросов, если он стоит поверх паттерна `Repository`_ и использует паттерн `Query object`_. Дело в том, что паттерн Repository ограничивает свой интерфейс посредством интерфейса Query Object. А так как класс не должен делать предположений о своих клиентах, то накапливать предустановленные запросы в классе `Repository`_ нельзя, ибо он не может владеть потребностями всех клиентов. Клиенты должны сами заботиться о себе. А сервисный слой как раз и создан для обслуживания клиентов.

В остальных случаях логику сервисного слоя можно размещать прямо на уровне приложения (обычно - контроллер).


Когда Сервисный Слой не нужен?
==============================

    Гораздо легче ответить на вопрос, когда слой служб не нужно использовать. Скорее
    всего, вам не понадобится слой служб, если у логики приложения есть только одна категория
    клиентов, например пользовательский интерфейс, отклики которого на варианты
    использования не охватывают несколько ресурсов транзакций. В этом случае управление
    транзакциями и выбор откликов можно возложить на контроллеры страниц (Page
    Controller, 350), которые будут обращаться непосредственно к слою источника данных.
    Тем не менее, как только у вас появится вторая категория клиентов или начнет
    использоваться второй ресурс транзакции, вам неизбежно придется ввести слой служб, что
    потребует полной переработки приложения.

    The easier question to answer is probably when not to use it. You probably don't need a Service Layer if your
    application's business logic will only have one kind of client say, a user interface and its use case responses
    don't involve multiple transactional resources. In this case your Page Controllers can manually control
    transactions and coordinate whatever response is required, perhaps delegating directly to the Data Source
    layer.
    But as soon as you envision a second kind of client, or a second transactional resource in use case responses, it
    pays to design in a Service Layer from the beginning.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

Тем не менее, широко распространена точка зрения, что доступ к модели должен всегда производиться через сервисный слой:

    Таким образом, на вашем месте я предпочел бы самый тонкий слой служб, какой
    только возможен (если он вообще нужен). Обычно же я добавляю его только тогда, когда
    он действительно необходим. Впрочем, мне знакомы хорошие специалисты, которые
    всегда применяют слой служб, содержащий взвешенную долю бизнес-логики, так что
    этим моим советом вы можете благополучно пренебречь.

    My preference is thus to have the thinnest Service Layer (133) you can, if you even need one. My usual
    approach is to assume that I don't need one and only add it if it seems that the application needs it. However, I
    know many good designers who always use a Service Layer (133) with a fair bit of logic, so feel free to ignore
    me on this one.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_

..

    Идея вычленения слоя служб из слоя предметной области основана на подходе, предполагающем возможность отмежевания логики процесса от "чистой" бизнес-логики.
    Уровень служб обычно охватывает логику, которая относится к конкретному варианту
    использования системы или обеспечивает взаимодействие с другими инфраструктурами
    (например, с помощью механизма сообщений).
    Стоит ли иметь отдельные слои служб и предметной области — вопрос, достойный обсуждения.
    Я склоняюсь к мысли о том, что подобное решение может оказаться полезным, хотя и не всегда, но некоторые уважаемые мною коллеги эту точку зрения не разделяют.

    The idea of splitting a services layer from a domain layer is based on a separation of workflow logic from
    pure domain logic. The services layer typically includes logic that's particular to a single use case and also
    some communication with other infrastructures, such as messaging. Whether to have separate services and
    domain layers is a matter some debate. I tend to look as it as occasionally useful rather than mandatory, but
    designers I respect disagree with me on this.

    \- "Patterns of Enterprise Application Architecture" [#fnpoeaa]_


Сервис - не обертка для DataMapper
==================================

Часто `Service Layer`_ ошибочно делают как враппер над `DataMapper`_.
Это не совсем верно.
Data Mapper обслуживает одну Domain Model (модель предметной области), Repository обслуживает один Aggregate [#fnnetmsa]_, а Cервис обслуживает клиента (или группу клиентов).
Сервисный слой может манипулировать в рамках бизнес-транзакции или в интересах клиента несколькими мапперами и другими сервисами.
Поэтому методы сервиса обычно содержат имя возвращаемой Модели Домена в качестве суффикса (например, getUser()), в то время как методы Маппера и Хранилища в этом суффиксе не нуждается (так как имя МОдели Домена уже и так присутствует в имени класса Маппера, и Маппер обслуживает только одну Модель Домена).

    Установить, какие операции должны быть размещены в слое служб, отнюдь не сложно.
    Это определяется нуждами клиентов слоя служб, первой (и наиболее важной) из
    которых обычно является пользовательский интерфейс.

    Identifying the operations needed on a Service Layer boundary is pretty straightforward. They're determined
    by the needs of Service Layer clients, the most significant (and first) of which is typically a user interface.
    ("Patterns of Enterprise Application Architecture" [#fnpoeaa]_)


Реализация Сервисного Слоя
==========================

Некоторые примеры реализации:

- https://github.com/in2it/zfdemo/blob/master/application/modules/user/services/User.php
- https://framework.zend.com/manual/2.4/en/in-depth-guide/services-and-servicemanager.html
- https://framework.zend.com/manual/2.4/en/user-guide/database-and-models.html#using-servicemanager-to-configure-the-table-gateway-and-inject-into-the-albumtable
- https://github.com/zendframework/zf2-tutorial/blob/master/module/Album/src/Album/Model/AlbumTable.php


Инверсия Управления
===================

Используйте инверсию управления, желательно в виде "Пассивного внедрения зависимостей" [#fnccode]_, `Dependency Injection`_ (DI).

    Истинное внедрение зависимостей идет еще на один шаг вперед. Класс не
    предпринимает непосредственных действий по разрешению своих зависимостей;
    он остается абсолютно пассивным. Вместо этого он предоставляет set-методы
    и/или аргументы конструктора, используемые для внедрения зависимостей.
    В процессе конструирования контейнер DI создает экземпляры необходимых
    объектов (обычно по требованию) и использует аргументы конструктора или
    set-методы для скрепления зависимостей. Фактически используемые
    зависимые объекты задаются в конфигурационном файле или на программном уровне
    в специализированном конструирующем модуле.

    True Dependency Injection goes one step further. The class takes no direct steps to
    resolve its dependencies; it is completely passive. Instead, it provides setter methods or
    constructor arguments (or both) that are used to inject the dependencies. During the con-
    struction process, the DI container instantiates the required objects (usually on demand)
    and uses the constructor arguments or setter methods provided to wire together the depen-
    dencies. Which dependent objects are actually used is specified through a configuration
    file or programmatically in a special-purpose construction module.
    "Clean Code: A Handbook of Agile Software Craftsmanship" [#fnccode]_

Одна из основных обязанностей Сервисного Слоя - это сокрытие источника данных.
Для тестирования можно использовать фиктивный Сервис (`Service Stub`_).
Этот же прием можно использовать для параллельной разработки, когда реализация сервисного слоя еще не готова.
Иногда бывает полезно подменить Сервис генератором фэйковых данных.
В общем, пользы от сервисного слоя будет мало, если нет возможности его подменить (или подменить используемые им зависимости).


Распространенная проблема Django-приложений
===========================================

Широко распространенная ошибка - использование класса django.db.models.Manager (а то и django.db.models.Model) в качестве сервисного слоя.
Нередко можно встретить, как какой-то метод класса django.db.models.Model принимает в качестве аргумента объект HTTP-запроса django.http.request.HttpRequest, например, для проверки прав.

Объект HTTP-запроса - это логика уровня приложения (application), в то время как класс модели - это логика уровня предметной области (domain), т.е. объекты реального мира, которую также называют правилами делового регламента (business rules).
Проверка прав - это тоже логика уровня приложения.

Нижележащий слой не должен ничего знать о вышестоящем слое.
Логика уровня домена не должна быть осведомлена о логике уровня приложения.

Классу django.db.models.Manager более всего соответствует класс Finder описанный в "Patterns of Enterprise Application Architecture" [#fnpoeaa]_.

    При реализации шлюза записи данных возникает вопрос: куда "пристроить" методы
    поиска, генерирующие экземпляр данного типового решения? Разумеется, можно
    воспользоваться статическими методами поиска, однако они исключают возможность
    полиморфизма (что могло бы пригодиться, если понадобится определить разные методы
    поиска для различных источников данных). В подобной ситуации часто имеет смысл
    создать отдельные объекты поиска, чтобы у каждой таблицы реляционной базы данных
    был один класс для проведения поиска и один класс шлюза для сохранения результатов
    этого поиска.

    Иногда шлюз записи данных трудно отличить от активной записи (Active Record, 182).
    В этом случае следует обратить внимание на наличие какой-либо логики домена; если
    она есть, значит, это активная запись. Реализация шлюза записи данных должна включать
    в себя только логику доступа к базе данных и никакой логики домена.

    With a Row Data Gateway you're faced with the questions of where to put the find operations that generate this
    pattern. You can use static find methods, but they preclude polymorphism should you want to substitute
    different finder methods for different data sources. In this case it often makes sense to have separate finder
    objects so that each table in a relational database will have one finder class and one gateway class for the results.

    It's often hard to tell the difference between a Row Data Gateway and an Active Record (160). The crux of the
    matter is whether there's any domain logic present; if there is, you have an Active Record (160). A Row Data
    Gateway should contain only database access logic and no domain logic.
    (Chapter 10. "Data Source Architectural Patterns : Row Data Gateway", "Patterns of Enterprise Application Architecture" [#fnpoeaa]_)

Хотя Django не использует паттерн `Repository`_, она использует абстракцию критериев выборки, своего рода разновидность паттерна `Query Object`_.
Подобно паттерну Repository, класс модели (`ActiveRecord`_) ограничивает свой интерфейс посредством интерфейса Query Object.
Клиенты должны пользоваться предоставленным интерфейсом, а не возлагать на модель и ее менеджер свои обязанности по знанию своих запросов.
А так как никакой класс не должен делать предположений о своих клиентах, то накапливать предустановленные запросы в классе модели нельзя, ибо он не может владеть потребностями всех клиентов.
Клиенты должны сами заботиться о себе.
А сервисный слой как раз и создан для обслуживания клиентов.

Попытки исключить Сервинсый Слой из Django-приложений приводит к появлению менеджеров с огромным количеством методов.

Хорошей практикой было бы сокрытие посредством сервисного слоя способа реализации Django Models в виде `ActiveRecord`_.
Это позволит безболезненно подменить ORM в случае необходимости.

    Можно было бы поспорить и о размещении логики приложения. Думаю, некоторые
    предпочли бы реализовать ее в методах объектов домена, таких, как
    Contract. calculateRevenueRecognitions (), ИЛИ вообще В слое источника данных, ЧТО
    позволило бы обойтись без отдельного слоя служб. Тем не менее подобное размещение
    логики приложения кажется мне весьма нежелательным, и вот почему. Во-первых, классы
    объектов домена, которые реализуют логику, специфичную для приложения (и зависят
    от шлюзов и других объектов, специфичных для приложения), менее подходят для
    повторного использования другими приложениями. Это должны быть модели частей
    предметной области, представляющих интерес для данного приложения, поэтому подобные
    объекты вовсе не обязаны описывать возможные отклики на все варианты использования
    приложения. Во-вторых, инкапсуляция логики приложения на более высоком
    уровне (каковым не является слой источника данных) облегчает изменение реализации
    этого слоя, возможно, посредством некоторых специальных инструментальных средств.

    Some might also argue that the application logic responsibilities could be implemented in domain object
    methods, such as Contract.calculateRevenueRecognitions(), or even in the data source layer,
    thereby eliminating the need for a separate Service Layer. However, I find those allocations of responsibility
    undesirable for a number of reasons. First, domain object classes are less reusable across applications if they
    implement application-specific logic (and depend on application-specific Gateways (466), and the like). They
    should model the parts of the problem domain that are of interest to the application, which doesn't mean all of
    application's use case responsibilities. Second, encapsulating application logic in a "higher" layer
    dedicated to that purpose (which the data source layer isn't) facilitates changing the implementation of that
    layer perhaps to use a workflow engine.
    ("Patterns of Enterprise Application Architecture" [#fnpoeaa]_)


Проблема Django-аннотаций
=========================

Я часто наблюдал такую проблему, когда в Django Model добавлялось какое-то новое поле, и начинали сыпаться проблемы, так как это имя уже было использовано либо с помощью аннотаций, либо с помощью Raw-SQL.
Также реализация аннотаций в Django ORM делает невозможным использование паттерна `Identity Map`_.
Storm ORM/SQLAlchemy реализуют аннотации более удачно.
Если Вам все-таки пришлось работать с Django Model, воздержитесь от использования механизма Django аннотаций в пользу голого паттерна `DataMapper`_.


Особенности сервисного слоя на стороне клиента
==============================================

Использование концепции `агрегата <Aggregate_>`__ и библиотек реактивного программирования, таких как `RxJS <https://github.com/ReactiveX/rxjs>`_, позволяет реализовывать Сервисный Слой с помощью простейшего паттерна Gateway_, смотрите, например, `учебный пример из документации Angular <https://angular.io/tutorial/toh-pt6>`__.
В таком случае, `Query Object`_ обычно реализуется в виде простого словаря, который преобразуется в список GET-параметров URL.
Общается такой Сервис с сервером обычно либо посредством JSON-RPC, либо посредством `REST-API Actions <http://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions>`__.

Все работает хорошо до тех пор, пока не возникает необходимость выражать приоритезированные запросы, например, использующие логический оператор OR, который использует меньший приоритет чем логический оператор AND.
Это порождает вопрос, кто должен отвечать за построение запроса, Сервисный Слой клиента или Сервисный Слой сервера?

С одной стороны, сервер не должен делать предположений о своих клиентах, и должен ограничивать свой интерфейс посредством интерфейса `Query Object`_.
Но это резко увеличивает уровень сложности клиента, в частности, при реализации `Service Stub`_.
Для облегчения реализации можно использовать библиотеку `rql <https://github.com/persvr/rql>`__, упомянутую в статье ":doc:`./javascript-and-repository-pattern`".

С другой стороны, Сервисный Слой, пусть и удаленного вызова, предназначен для обслуживания клиентов, а значит, может концентрировать в себе логику построения запросов.
Если клиент не содержит сложной логики, позволяющей интерпретировать приоритезированные запросы для Service Stub, то нет необходимости его усложнять этим.
В таком случае проще добавить новый метод в сервисе удаленного вызова, и избавиться от необходимости в приоритезированных запросах.


Проблема параллельного обновления
=================================

Появление интернета открыло доступ к огромному количеству данных, которое несопоставимо велико с возможностями одного сервера.
Возникла необходимость в масштабировании и в распределенном хранении и обработке данных.

Одна из самых острых проблем - это проблема параллельного обновления данных.

    Все состояния гонки (race condition), взаимоблокировки (deadlocks) и проблемы параллельного обновления обусловлены изменяемостью переменных.
    Если в программе нет изменяемых переменных, она никогда не окажется в состоянии гонки и никогда не столкнется с проблемами одновременного изменения.
    В отсутствие изменяемых блокировок программа не может попасть в состояние взаимоблокировки.

    All race conditions, deadlock conditions, and concurrent update problems are due to mutable variables.
    You cannot have a race condition or a concurrent update problem if no variable is ever updated.
    You cannot have deadlocks without mutable locks.

    \- "Clean Architecture: A Craftsman's Guide to Software Structure and Design" [#fncarch]_ by Robert C. Martin

Любой порядок выражается в правильном наложении ограничений.


CQRS
====

Проблему параллельного обновления в значительной мере можно уменьшить наложением ограничения на двунаправленные изменения состояния путем введения однонаправленных изменений, т.е. путем отделения чтения от записи.
Именно такой подход используется в Redux.

    "it allows us to host the two services differently eg: we can host the read service on 25 servers and the write service on two.
    The processing of commands and queries is fundamentally asymmetrical, and scaling the services symmetrically does not make a lot of sense."

    \- "`CQRS, Task Based UIs, Event Sourcing agh! <http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/>`__" by Greg Young

Управление Логикой Приложения и Бизнес-Логикой хорошо раскрывается в статье "`Clarified CQRS <http://udidahan.com/2009/12/09/clarified-cqrs/>`__" by Udi Dahan.

Использование CQRS способствует использованию парадигмы Функционального Программирования.

Функциональное Программирование по своей сути не может порождать побочных эффектов (т.к. Функциональное Программирование накладывает ограничение на присваивание (изменяемость)), и именно этим обусловлен рост его популярности в эпоху распределенных вычислений.
Нет изменяемого состояния - нет проблем параллельного обновления.

Следует отличать парадигму Функционального Программирования от языков, поддерживающих эту парадигму, поскольку нередко языки, поддерживающие эту парадигму, позволяют не следовать ей.

Однако, несмотря на открывшиеся возможности использовать Функциональное Программирование в коде, само хранилище данных (IO-устройство) все еще подвержено проблемам параллельного обновления, поскольку имеет изменяемые записи, а значит, имеет побочный эффект.

Решением этой проблемы обычно является замена CRUD (Create, Read, Update, Delete) на CR, т.е. наложение ограничения на изменение (Update) и удаление (Delete) записей в хранилище, что получило распространение под термином Event Sourcing.
Существуют специализированные хранилища, реализующие его, но он реализуется не обязательно специализированными инструментами.


Event Sourcing
==============

Если CQRS позволяет работать с хранилищами данных в Императивном стиле, и отделяет действия (побочный эффект) от запроса (чтения) данных, то Event Sourcing идет еще дальше, и накладывает ограничение на изменение и удаление данных, превращая CRUD в CR.
Такой шаблон позволяет работать с хранилищами данных в Функциональном стиле, и предоставляет такие же выгоды: нет изменяемого состояния - нет проблемы параллельного обновления.
И такие же недостатки - потребность в большом количестве памяти и процессорной мощности.
Именно поэтому, данный шаблон широко используется в распределенных системах, где остро проявляется потребность в его достоинствах, и, вместе с тем, не проявляются его недостатки (ведь распределенные системы не лимитированы ни в памяти, ни в процессорной мощности).

Наглядным примером Event Sourcing может быть принцип организации банковского счета в базе данных, когда счет не является источником истины, а просто отражает совокупное значение всех транзакций (т.е. событий).

Наиболее ясно эта тема раскрывается в Chapter 6 "Functional Programming" of "Clean Architecture" by Robert C. Martin.

    Что особенно важно, никакая информация не удаляется из такого хранилища и не изменяется.
    Как следствие, от набора CRUD-операций в приложениях остаются только CR.
    Также отсутствие операций изменения и/или удаления с хранилищем устраняет любые проблемы конкурирующих
    обновлений.

    Обладая хранилищем достаточного объема и достаточной вычислительной мощностью, мы можем сделать свои приложения полностью неизменяемыми — и, как следствие, **полностью функциональными**.

    Если это все еще кажется вам абсурдным, вспомните, как работают системы управления версиями исходного кода.

    More importantly, nothing ever gets deleted or updated from such a data store.
    As a consequence, our applications are not CRUD; they are just CR. Also, because neither updates nor deletions occur in the data store, there cannot be any concurrent update issues.

    If we have enough storage and enough processor power, we can make our applications entirely immutable—and, therefore, **entirely functional**.

    If this still sounds absurd, it might help if you remembered that this is precisely the way your source code control system works.

    \- "Clean Architecture: A Craftsman's Guide to Software Structure and Design" [#fncarch]_ by Robert C. Martin

..

    **Event Sourcing is naturally functional.**
    It's an append only log of facts that have happened in the past.
    You can say that any projection any state is a left fold over your previous history.

    \- Greg Young, "`A Decade of DDD, CQRS, Event Sourcing <https://youtu.be/LDW0QWie21s?t=1004>`__" at 16:44

..

    I have always said that Event Sourcing is "Functional Data Storage".
    In this talk we will try migrating to a idiomatic functional way of looking at Event Sourcing.
    Come and watch all the code disappear!
    By the time you leave you will never want an "Event Sourcing Framework (TM)" ever again!

    \- Greg Young, "`Functional Data <https://vimeo.com/131636650>`__", NDC Conferences


Что почитать
============

- "Clean Code: A Handbook of Agile Software Craftsmanship" by Robert C. Martin [#fnccode]_, главы:
    - Dependency Injection ... 157
    - Cross-Cutting Concerns ... 160
    - Java Proxies ... 161
    - Pure Java AOP Frameworks ... 163
- "Patterns of Enterprise Application Architecture" by Martin Fowler [#fnpoeaa]_, главы:
    - Part 1. The Narratives : Chapter 2. Organizing Domain Logic : Service Layer
    - Part 1. The Narratives : Chapter 8. Putting It All Together
    - Part 2. The Patterns : Chapter 9. Domain Logic Patterns : Service Layer
- "Domain-Driven Design: Tackling Complexity in the Heart of Software" by Eric Evans [#fnddd]_, глава:
    - Part II: The Building Blocks of a Model-Driven Design : Chapter Five. A Model Expressed in Software : Services
- "Design Patterns Elements of Reusable Object-Oriented Software" by Erich Gamma [#fngof]_, главы:
    - Design Pattern Catalog : 4 Structural Patterns : Adapter ... 139
    - Design Pattern Catalog : 4 Structural Patterns : Decorator ... 175
- "`CQRS <https://martinfowler.com/bliki/CQRS.html>`__"
- "`Event Sourcing <https://martinfowler.com/eaaDev/EventSourcing.html>`__"
- "`What do you mean by "Event-Driven"? <https://martinfowler.com/articles/201701-event-driven.html>`__"
- "`CQRS, Task Based UIs, Event Sourcing agh! <http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/>`__" by Greg Young
- "`Clarified CQRS <http://udidahan.com/2009/12/09/clarified-cqrs/>`__" by Udi Dahan

This article in English ":doc:`../en/service-layer`".

.. rubric:: Footnotes

.. [#fnccode] "`Clean Code: A Handbook of Agile Software Craftsmanship`_" by `Robert C. Martin`_
.. [#fncarch] "Clean Architecture: A Craftsman's Guide to Software Structure and Design" by Robert C. Martin
.. [#fnpoeaa] "`Patterns of Enterprise Application Architecture`_" by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] "Domain-Driven Design: Tackling Complexity in the Heart of Software" by Eric Evans
.. [#fngof] "Design Patterns Elements of Reusable Object-Oriented Software" by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994
.. [#fnr] "Refactoring: Improving the Design of Existing Code" by Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#fnbm] "Building Microservices. Designing Fine-Grained Systems" by Sam Newman
.. [#fnnetmsa] "`.NET Microservices: Architecture for Containerized .NET Applications <https://docs.microsoft.com/en-us/dotnet/standard/microservices-architecture/index>`__" edition v2.2.1 (`mirror <https://aka.ms/microservicesebook>`__) by Cesar de la Torre, Bill Wagner, Mike Rousos

.. update:: 12 Oct, 2019


.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Robert C. Martin: http://informit.com/martinseries
.. _Patterns of Enterprise Application Architecture: https://www.martinfowler.com/books/eaa.html
.. _Martin Fowler: https://martinfowler.com/aboutMe.html

.. _Coupling: http://wiki.c2.com/?CouplingAndCohesion
.. _Cohesion: http://wiki.c2.com/?CouplingAndCohesion
.. _Dependency Injection: https://martinfowler.com/articles/injection.html

.. _ActiveRecord: http://www.martinfowler.com/eaaCatalog/activeRecord.html
.. _DataMapper: http://martinfowler.com/eaaCatalog/dataMapper.html
.. _Domain Model: https://martinfowler.com/eaaCatalog/domainModel.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _Query Object: http://martinfowler.com/eaaCatalog/queryObject.html
.. _Remote Facade: https://www.martinfowler.com/eaaCatalog/remoteFacade.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Layer: https://martinfowler.com/eaaCatalog/serviceLayer.html
.. _Service Stub: https://martinfowler.com/eaaCatalog/serviceStub.html
.. _Gateway: https://martinfowler.com/eaaCatalog/gateway.html
.. _Aggregate: https://martinfowler.com/bliki/DDD_Aggregate.html

.. _Extract Method: https://www.refactoring.com/catalog/extractMethod.html
.. _Replace Method with Method Object: https://www.refactoring.com/catalog/replaceMethodWithMethodObject.html
