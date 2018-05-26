
Проектирование Сервисного Слоя
==============================

.. post:: Jul 17, 2017
   :language: ru
   :tags: Design, Architecture, ORM, Django Model
   :category:
   :author: Ivan Zakrevsky

Эта статья посвящена вопросам проeктирования Сервисного Слоя (`Service Layer`_) и рассматривает широко распространенные ошибки.


.. contents:: Содержание


Назначение Сервисного Слоя
==========================

    Слой служб определяет границы приложения и множество операций, предоставляемых
    им для интерфейсных клиентских слоев кода. Он инкапсулирует бизнес-логику
    приложения, управляет транзакциями и координирует реакции надействия.

    Defines an application's boundary with a layer of services that establishes a set of available
    operations and coordinates the application's response in each operation.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

    SERVICE - An operation offered as an interface that stands alone in the model, with no encapsulated state.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Самое главное что следует усвоить, так это то, что Сервисный Слой относится к логике уровня Приложения.
Это важно, поскольку из этого следует, что Сервисный Слой находится выше слоя уровня предметной области (domain logic), т.е. слоя объектов реального мира, который также называет деловыми регламентами (business rules).
Из этого также следует и то, что объекты предметной области не должны быть осведомлены о наличии Сервисного Слоя.

Следует обратить внимание на тот факт, что под термином "business rules" Eric Evans понимает логику предметной области:

    User Interface (or Presentation Layer)
        Responsible for showing information to the user and interpreting the user's
        commands. The external actor might sometimes be another computer
        system rather than a human user.
    Application Layer
        Defines the jobs the software is supposed to do and directs the expressive
        domain objects to work out problems. The tasks this layer is responsible
        for are meaningful to the business or necessary for interaction with the
        application layers of other systems.
        This layer is kept thin. It **does not contain business rules** or knowledge, but
        only coordinates tasks and delegates work to collaborations of domain
        objects in the next layer down. It does not have state reflecting the
        business situation, but it can have state that reflects the progress of a task
        for the user or the program.
    Domain Layer (or Model Layer)
        Responsible for representing concepts of the business, information about
        the **business situation, and business rules**. State that reflects the business
        situation is controlled and used here, even though the technical details of
        storing it are delegated to the infrastructure. This layer is the heart of
        business software.
    Infrastructure Layer
        Provides generic technical capabilities that support the higher layers:
        message sending for the application, persistence for the domain, drawing
        widgets for the UI, and so on. The infrastructure layer may also support
        the pattern of interactions between the four layers through an
        architectural framework.

    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

В то время как Martin Fowler понимает под термином "business logic" не только логику предметной области:

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Мы будем рассматривать под термином "business rules" (правила делового регламента) исключительно логику предметной области, тем более, что Martin Fowler на это косвенно указывает:

    The problem came with domain logic: business rules, validations, calculations, and
    the like.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

    Then there's the matter of what comes under the term "business logic." I find this a curious term because there
    are few things that are less logical than business logic.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Кроме перечисленного выше, сервисный слой может выполнять следующие обязанности:

- Компоновки атомарных операций (например, требуется одновременно сохранить данные в БД, редисе, и на фаловой системе, в рамках одной бизнес-транзакции, или откатить все назад).
- Сокрытия источника данных (здесь он дублирует функции паттерна `Repository`_) и может быть опущен, если нет других причин.
- Компоновки реиспользуемых операций уровня приложения (например, некая часть логики уровня приложения используется в нескольких различных контроллерах).
- Как основа для реализации `Интерфейса удаленного доступа <Remote Facade_>`__.
- Когда контроллер имеет какой-то большой метод, он нуждается в декомпозиции, и к нему применяется `Extract Method`_ для вычленения обязанностей в отдельные методы. При этом растет количество методов класса, что влечет за собой падение его сфокусированности или `Связанности <Cohesion_>`__ (т.е. коэффициент совместного использования свойств класса его методами). Чтобы восстановить связанность, эти методы выделяются в отдельный класс, образуя `Method Object <Replace Method with Method Object_>`__. И вот этот метод-объект и может быть преобразован в сервисный слой.
- Сервисный слой можно использовать в качестве концентратора запросов, если он стоит поверх паттерна `Repository`_ и использует паттерн `Query object`_. Дело в том, что паттерн Repository ограничивает свой интерфейс посредством интерфейса Query Object. А так как класс не должен делать предположений о своих клиентах, то накапливать предустановленные запросы в классе `Repository`_ нельзя, ибо он не может владеть потребностями всех клиентов. Клиенты должны сами заботиться о себе. А сервисный слой как раз и создан для обслуживания клиентов.

В остальных случаях логику сервисного слоя можно размещать прямо на уровне приложения (обычно - контроллер).

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

    Идея вычленения слоя служб из слоя предметной области основана на подходе, пред-
    полагающем возможность отмежевания логики процесса от "чистой" бизнес-логики.
    Уровень служб обычно охватывает логику, которая относится к конкретному варианту
    использования системы или обеспечивает взаимодействие с другими инфраструктурами
    (например, с помощью механизма сообщений). Стоит ли иметь отдельные слои служб и
    предметной области — вопрос, достойный обсуждения. Я склоняюсь к мысли о том, что
    подобное решение может оказаться полезным, хотя и не всегда, но некоторые уважае-
    мые мною коллеги эту точку зрения не разделяют.

    The idea of splitting a services layer from a domain layer is based on a separation of workflow logic from
    pure domain logic. The services layer typically includes logic that's particular to a single use case and also
    some communication with other infrastructures, such as messaging. Whether to have separate services and
    domain layers is a matter some debate. I tend to look as it as occasionally useful rather than mandatory, but
    designers I respect disagree with me on this.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

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
    responsibility of an ENTITY or VALUE OBJECT , add an operation to the model as a
    standalone interface declared as a SERVICE . Define the interface in terms of the
    language of the model and make sure the operation name is part of the UBIQUITOUS
    LANGUAGE . Make the SERVICE stateless.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)


Сервис - не обертка для DataMapper
==================================

Часто `Service Layer`_ ошибочно делают как враппер над `DataMapper`_.
Это не совсем верно.
Маппер обслуживает Domain (объект предметной области), а сервисный слой обслуживает клиента (группу клиентов).
Сервисный слой может манипулировать в рамках бизнес-транзакции или в интересах клиента несколькими маперами и другими сервисами.
Поэтому методы сервиса обычно содержат имя возвращаемого домена в качестве суффикса (например, getUser()), в то время как методы маппера в этом суффиксе не нуждается (так как имя домена присутствует в имени класса маппера, и маппер обслуживает только один домен).

    Установить, какие операции должны быть размещены в слое служб, отнюдь не сложно.
    Это определяется нуждами клиентов слоя служб, первой (и наиболее важной) из
    которых обычно является пользовательский интерфейс.

    Identifying the operations needed on a Service Layer boundary is pretty straightforward. They're determined
    by the needs of Service Layer clients, the most significant (and first) of which is typically a user interface.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)


Реализация Сервисного Слоя
==========================

Некоторые примеры реализации:

- https://github.com/in2it/zfdemo/blob/master/application/modules/user/services/User.php
- https://framework.zend.com/manual/2.4/en/in-depth-guide/services-and-servicemanager.html
- https://framework.zend.com/manual/2.4/en/user-guide/database-and-models.html#using-servicemanager-to-configure-the-table-gateway-and-inject-into-the-albumtable
- https://github.com/zendframework/zf2-tutorial/blob/master/module/Album/src/Album/Model/AlbumTable.php


Инверсия Управления
===================

Используйте инверсию управления, желательно в виде "Пассивного внедрения зависимостей" [#fnccode]_, `Dependency Injection`_ Principle (DIP).

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
    «Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_

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

Классу django.db.models.Manager более всего соответствует класс Finder описанный в «Patterns of Enterprise Application Architecture» [#fnpoeaa]_.

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
    (Chapter 10. "Data Source Architectural Patterns : Row Data Gateway", «Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)


Укрощение разбухших моделей
===========================

Часто можно встретить модели имеющие большое число методов (я встречал несколько сотен).
При анализе таких моделей часто обнаруживаются посторонние обязанности в классе, а размер класса, как известно, измеряется количеством его обязанностей.
Все обязанности, которые не относятся к Доменной области, следует вынести в Сервисный Слой.
Но что делать с другими методами?

Предположим, некая Модель имеет несколько десятков методов, которые не имеют общего применения, а используются только одним клиентом.
Отнести их к обязанности клиентов нельзя, так как это привело бы к появлению "G14: Feature Envy" [#fnccode]_.

Как уже упоминалось ранее, Service Layer обычно реализуется как объект без состояния.
Если клиент относится к логике Приложения, то решением может быть создание Service Layer.

    Модель предметной области более предпочтительна в сравнении со сценарием транзакции,
    поскольку исключает возможность дублирования бизнес-логики и позволяет
    бороться со сложностью с помощью классических проектных решений. Но размещение
    логики приложения в "чистых" классах домена чревато нежелательными последствиями.
    Во-первых, классы домена допускают меньшую вероятность повторного использования,
    если они реализуют специфическую логику приложения и зависят от тех или иных прикладных
    инструментальных пакетов. Во-вторых, смешивание логики обеих категорий
    в контексте одних и тех же классов затрудняет возможность новой реализации логики
    приложения с помощью специфических инструментальных средств, если необходимость
    такого шага становится очевидной. По этим причинам слой служб предусматривает
    распределение "разной" логики по отдельным слоям, что обеспечивает традиционные
    преимущества расслоения, а также большую степень свободы применения классов домена
    в разных приложениях.

    Domain Models (116) are preferable to Transaction Scripts (110) for avoiding domain logic duplication and
    for managing complexity using classical design patterns. But putting application logic into pure domain object
    classes has a couple of undesirable consequences. First, domain object classes are less reusable across
    applications if they implement application-specific logic and depend on application-specific packages.
    Second, commingling both kinds of logic in the same classes makes it harder to reimplement the application
    logic in, say, a workflow tool if that should ever become desirable. For these reasons Service Layer factors
    each kind of business logic into a separate layer, yielding the usual benefits of layering and rendering the pure
    domain object classes more reusable from application to application.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Но если клиент относится к логике Доменной области, то нельзя допустить чтобы слой уровня Доменной логики был осведомлен о логике Приложения.
А Service Layer - это логика уровня приложения.

Иными словами, клиент требует от Доменной Модели интерфейс, который не должен быть реализован Доменной Моделью.
Для выравнивания интерфейсов существует паттерн Adapter (aka Wrapper), см. «Design Patterns Elements of Reusable Object-Oriented Software» [#fngof]_.

Иными словами, это враппер над инстанцией Модели, который оборачивает её и придает ей дополнительное поведение, которое требуется клиентом.
Иногда такие обертки ошибочно называют Аспектом или Декоратором, но это неверно, так как они не изменяют интерфейса оригинального объекта.

Вернемся к случаю, когда клиент относится к логике Приложения.
Можно ли применять паттерн Adapter в этом случае?

Martin Fowler говорит что:

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
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Поскольку Martin Fowler прекрасно понимает отличие между "`Domain Model`_" и "`DataMapper`_", эта цитата сильно напоминает мне "Cross-Cutting Concerns" [#fnccode]_ с тем только отличием, что "Cross-Cutting Concerns" реализует интерфейс оригинального объекта, в то время как domain facade дополняет его.


Проблема Django-аннотаций
=========================

Я часто наблюдал такую проблему, когда в Django Model добавлялось какое-то новое поле, и начинали сыпаться проблемы, так как это имя уже было использовано либо с помощью аннотаций, либо с помощью Raw-SQL.
Также реализация аннотаций в Django ORM делает невозможным использование паттерна `Identity Map`_.
Storm ORM/SQLAlchemy реализуют аннотации более удачно.
Если Вам все-таки пришлось работать с Django Model, воздержитесь от использования механизма Django аннотаций в пользу голого паттерна `DataMapper`_.


Сервисы инфраструктурного уровня
================================

От сервисного слоя следует отличать сервисы инфраструктурного уровня.

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
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

..

    Infrastructure Layer - Provides generic technical capabilities that support the higher layers:
    message sending for the application, persistence for the domain, drawing
    widgets for the UI, and so on. The infrastructure layer may also support
    the pattern of interactions between the four layers through an
    architectural framework.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)


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


Что почитать
============

- «Clean Code: A Handbook of Agile Software Craftsmanship» by Robert C. Martin [#fnccode]_, главы:
    - Dependency Injection ... 157
    - Cross-Cutting Concerns ... 160
    - Java Proxies ... 161
    - Pure Java AOP Frameworks ... 163
- «Patterns of Enterprise Application Architecture» by Martin Fowler [#fnpoeaa]_, главы:
    - Part 1. The Narratives : Chapter 2. Organizing Domain Logic : Service Layer
    - Part 1. The Narratives : Chapter 8. Putting It All Together
    - Part 2. The Patterns : Chapter 9. Domain Logic Patterns : Service Layer
- «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans [#fnddd]_, глава:
    - Part II: The Building Blocks of a Model-Driven Design : Chapter Five. A Model Expressed in Software : Services
- «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma [#fngof]_, главы:
    - Design Pattern Catalog : 4 Structural Patterns : Adapter ... 139
    - Design Pattern Catalog : 4 Structural Patterns : Decorator ... 175

This article in English ":doc:`../en/service-layer`".


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fnpoeaa] «`Patterns of Enterprise Application Architecture`_» by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans
.. [#fngof] «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994


.. update:: 28 May, 2018


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
