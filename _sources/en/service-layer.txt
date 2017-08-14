
Design of Service Layer
=======================

.. post:: Jul 17, 2017
   :language: en
   :tags: Design, Architecture, ORM, Django Model
   :category:
   :author: Ivan Zakrevsky

This article is devoted to the issues of designing `Service Layer`_ and considers the widespread mistakes.


.. contents:: Contents


Purpose of Service Layer
========================

    Defines an application's boundary with a layer of services that establishes a set of available
    operations and coordinates the application's response in each operation.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

    SERVICE - An operation offered as an interface that stands alone in the model, with no encapsulated state.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

..

    The benefit of Service Layer is that it defines a common set of application operations available to many kinds
    of clients and it coordinates an application's response in each operation. The response may involve application
    logic that needs to be transacted atomically across multiple transactional resources. Thus, in an application
    with more than one kind of client of its business logic, and complex responses in its use cases involving
    multiple transactional resources, it makes a lot of sense to include a Service Layer with container-managed
    transactions, even in an undistributed architecture.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

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

The most important thing to understand is that the `Service Layer`_ is an Application layer logic.
This is important because this implies that the Service Layer is over the Domain Layer (i.e. layer of real world objects, which is also called "business rules").
This means that the objects of the Domain Layer should not be aware of the Service Layer.

Note that Eric Evans understands the logic of the Domain Layer under the term "business rules":

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

While Martin Fowler understands by the term "business logic" not only the logic of the Domain Layer:

    Like Transaction Script (110) and Domain Model (116), Service Layer is a pattern for organizing **business logic**.
    Many designers, including me, like to divide "**business logic**" into two kinds: "domain logic," having to
    do purely with the problem domain (such as strategies for calculating revenue recognition on a contract), and
    "application logic," having to do with application responsibilities [Cockburn UC] (such as notifying contract
    administrators, and integrated applications, of revenue recognition calculations). Application logic is
    sometimes referred to as "workflow logic," although different people have different interpretations of
    "workflow."
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

We will understand by the term "business rules" only the logic of the Domain Layer, especially since Martin Fowler indirectly indicates this:

    The problem came with domain logic: business rules, validations, calculations, and
    the like.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

    Then there's the matter of what comes under the term "business logic." I find this a curious term because there
    are few things that are less logical than business logic.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

In addition to the above, the Service Layer can carry the following responsibilities:

- To combine the parts of an atomic operation (for example, application should save the data to several storages, e.g. database, redis, file system within a single business transaction or should roll back all).
- To hide the data source (here it duplicates the responsibility of the pattern `Repository`_) and can be omitted if there are no other reasons.
- To aggregate the application level operations that are being reused by several clients (for example, some part of application-level logic is used in several different controllers).
- As basis for implementation of `Remote Facade`_.
- When you have a large controller method, you have to do decomposition. Thus, you apply `Extract Method`_ to separate each responsibility into own method. When you did it, you found that the class lost its focus. The quantity of methods has been increased that means the `Cohesion`_ (i.e. coefficient of sharing the class' properties by the class' methods) has been reduced. To restore the `Cohesion`_ you have to extraсt these methods into separate `Method Object <Replace Method with Method Object_>`__, which can be used as a Service Layer.
- The Service Layer can be used as an aggregator for queries if it is over the `Repository`_ pattern and uses the `Query object`_ pattern. The fact is that the Repository pattern limits its interface using the Query Object interface. And since class does not have to make assumptions about its clients, it is impossible to accumulate pre-defined queries in the `Repository`_ class, because it can not be aware about the all needs of all clients. Clients should take care of themselves. But the Service Layer was created for client service. Therefore, it's a responsibility of the Service Layer.

In other cases, the logic of the Service Layer can be placed directly at the application level (usually a controller).

    The easier question to answer is probably when not to use it. You probably don't need a Service Layer if your
    application's business logic will only have one kind of client say, a user interface and its use case responses
    don't involve multiple transactional resources. In this case your Page Controllers can manually control
    transactions and coordinate whatever response is required, perhaps delegating directly to the Data Source
    layer.
    But as soon as you envision a second kind of client, or a second transactional resource in use case responses, it
    pays to design in a Service Layer from the beginning.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

However, the widely held view that access to the model should always be made through the Service Layer:

    My preference is thus to have the thinnest Service Layer (133) you can, if you even need one. My usual
    approach is to assume that I don't need one and only add it if it seems that the application needs it. However, I
    know many good designers who always use a Service Layer (133) with a fair bit of logic, so feel free to ignore
    me on this one.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

..

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


Service is not a wrapper for Data Mapper
========================================

Often `Service Layer`_ is mistakenly made in the for of wrapper over `DataMapper`_.
This is not quite the right decision.
Data Mapper serves Domain, while Service Layer serves client (or client group).
The Service Layer can manipulate multiple Data Mappers and other Services within a business transaction or for the interests of the client.
Therefore, the Service's methods usually contain the name of the returned Domain as a suffix (for example, getUser()), while the methods of the Data Mapper do not need this suffix (since the Domain name is present in the name of the Data Mapper class, and the Data Mapper serves only one Domain).

    Identifying the operations needed on a Service Layer boundary is pretty straightforward. They're determined
    by the needs of Service Layer clients, the most significant (and first) of which is typically a user interface.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)


Implementation of Service Layer
===============================

There is a few examples of Service Layer implementations:

- https://github.com/in2it/zfdemo/blob/master/application/modules/user/services/User.php
- https://framework.zend.com/manual/2.4/en/in-depth-guide/services-and-servicemanager.html
- https://framework.zend.com/manual/2.4/en/user-guide/database-and-models.html#using-servicemanager-to-configure-the-table-gateway-and-inject-into-the-albumtable
- https://github.com/zendframework/zf2-tutorial/blob/master/module/Album/src/Album/Model/AlbumTable.php


Inversion of control
====================

Use Inversion of control, desirable in the form of Passive [#fnccode]_ "`Dependency Injection`_ Principle" (DIP).

    True Dependency Injection goes one step further. The class takes no direct steps to
    resolve its dependencies; it is completely passive. Instead, it provides setter methods or
    constructor arguments (or both) that are used to inject the dependencies. During the con-
    struction process, the DI container instantiates the required objects (usually on demand)
    and uses the constructor arguments or setter methods provided to wire together the depen-
    dencies. Which dependent objects are actually used is specified through a configuration
    file or programmatically in a special-purpose construction module.
    «Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_

One of the main responsibilities of Service Layer is the hiding of data source.
It allows you to use `Service Stub`_ for testing.
The same approach can be used for parallel development, when the implementation of the Service Layer is not ready yet.
Sometimes it is useful to replace the Service with a fake data generator.
In general, the Service Layer will be of little use if it is not possible to substitute it (or to substitute the dependencies used by it).


Widespread problem of Django applications
=========================================

A common mistake is to use the django.db.models.Manager class (and even django.db.models.Model) as a Service Layer.
Often you can see how some method of the class django.db.models.Model takes as an argument the HTTP-request object django.http.request.HttpRequest, for example, to check the permissions.

The HTTP request object is the Application Layer logic, while the model class is the logic of the Domain Layer, i.e. objects of the real world, which are also called business rules.
Checking permissions is also the logic of Application Layer.

The lower layer should not be aware of the higher layer.
Domain-level logic should not be aware of application-level logic.

The class django.db.models.Manager corresponds most closely to the class Finder described in «Patterns of Enterprise Application Architecture» [#fnpoeaa]_.

    With a Row Data Gateway you're faced with the questions of where to put the find operations that generate this
    pattern. You can use static find methods, but they preclude polymorphism should you want to substitute
    different finder methods for different data sources. In this case it often makes sense to have separate finder
    objects so that each table in a relational database will have one finder class and one gateway class for the results.

    It's often hard to tell the difference between a Row Data Gateway and an Active Record (160). The crux of the
    matter is whether there's any domain logic present; if there is, you have an Active Record (160). A Row Data
    Gateway should contain only database access logic and no domain logic.
    (Chapter 10. "Data Source Architectural Patterns : Row Data Gateway", «Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

Although Django does not use the `Repository`_ pattern, it uses an abstraction of the selection criteria in the form similar to the `Query Object`_ pattern.
Like the Repository pattern, the model class (`ActiveRecord`_) limits its interface using the Query Object interface.
Clients should use the provided interface, rather than impose their responsibilities on the Model and its Manager on knowledge of their queries.
And since class does not have to make assumptions about its clients, it is impossible to accumulate pre-defined queries in the Model class, because it can not be aware about the all needs of all clients.
Clients should take care of themselves.
But the Service Layer was created for client service.
Therefore, it's a responsibility of the Service Layer.

Attempts to exclude the Serving Layer from Django applications leads to the appearance of Managers with a lot of methods.

A good practice would be to hide the implementation (in the form of `ActiveRecord`_) of Django models by the Service Layer.
This will allow painless ORM replace if necessary.

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

In the article "`Clean Architecture in Django <https://engineering.21buttons.com/clean-architecture-in-django-d326a4ab86a9>`__" you can find an example of using the Repository pattern to hide the data source for Django-application.


Taming of swollen models
========================

It is often possible to find models with a large number of methods (I met several hundred).
If you analyze such models, you can often find outside responsibilities in the class.
As you know, the size of the class is measured by the amount of its responsibilities.
All responsibilities that are not related to the Domain Layer should be moved to the Service Layer.
But what to do with other methods?

Suppose some Model has several dozen methods that do not have a common application, but are used by only one client.
You can not assign them to the responsibility of the client, as this would lead to "G14: Feature Envy" [#fnccode]_.

As mentioned previously, Service Layer is usually implemented as a stateless object.
If the client belongs to the Application level logic, the solution may be to create a Service Layer.

    Domain Models (116) are preferable to Transaction Scripts (110) for avoiding domain logic duplication and
    for managing complexity using classical design patterns. But putting application logic into pure domain object
    classes has a couple of undesirable consequences. First, domain object classes are less reusable across
    applications if they implement application-specific logic and depend on application-specific packages.
    Second, commingling both kinds of logic in the same classes makes it harder to reimplement the application
    logic in, say, a workflow tool if that should ever become desirable. For these reasons Service Layer factors
    each kind of business logic into a separate layer, yielding the usual benefits of layering and rendering the pure
    domain object classes more reusable from application to application.
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

But if the client belongs to the Domain layer, then this client may not be aware of the Application Layer logic.
But Service Layer is the logic of the Application Layer.

In other words, the client requires an interface from the Domain Model, which should not be implemented by the Domain Model.
For interface equalization we have to use the pattern Adapter (aka Wrapper), see «Design Patterns Elements of Reusable Object-Oriented Software» [#fngof]_ for more info.

In other words, it is a wrapper over the Model instance that wraps it and gives it additional behavior that is required by the client.
Sometimes such wrappers are wrongly called Aspect or Decorator, but this is incorrect, since they do not change the interface of the original object.

Let's return to the case when the client belongs to the Application logic.
Is it possible to use the Adapter pattern in this case?

Martin Fowler says:

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

Since Martin Fowler perfectly understands the difference between "`Domain Model`_" and "`DataMapper`_", this quote strongly reminds me "Cross-Cutting Concerns" [#fnccode]_ with the only difference being that "Cross-Cutting Concerns" implements the interface of the original object, while the domain facade complements it.


Problems of Django annotation
=============================

I often observed the problem when a new field was added to the Django Model, and multiple problems started to occur, since this name was already used either with the annotation interface or with Raw-SQL.
Also, the implementation of annotations by Django ORM makes it impossible to use the pattern `Identity Map`_.
Storm ORM / SQLAlchemy implement annotations more successfully.
If you still had to work with Django Model, refrain from using Django annotation mechanism in favor of bare pattern `DataMapper`_.


Services of infrastructure layer
================================

You have to distinguish the Service Layer from infrastructure layer services.

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


Further Reading
===============

- «Clean Code: A Handbook of Agile Software Craftsmanship» by Robert C. Martin [#fnccode]_, chapters:
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

Эта статья на Русском языке ":doc:`../ru/service-layer`".

.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fnpoeaa] «`Patterns of Enterprise Application Architecture`_» by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans
.. [#fngof] «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994


.. update:: 07 Aug, 2017


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

.. _Extract Method: https://www.refactoring.com/catalog/extractMethod.html
.. _Replace Method with Method Object: https://www.refactoring.com/catalog/replaceMethodWithMethodObject.html
