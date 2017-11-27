
Implementation of Repository pattern for browser's JavaScript
=============================================================

.. post:: 06 Aug, 2017
   :language: en
   :tags: Repository, ORM, JavaScript, Model, DDD
   :category:
   :author: Ivan Zakrevsky


Good architecture makes you free from certain implementation.
It allows you to postpone the moment of decision on implementation and `begin code construction even without the decision <Service Stub_>`__.
The most important point is that you gain the opportunity to make a decision at the time of the greatest awareness, and you can also easily replace a specific implementation with any other.
This responsibility is assigned to the `Repository`_.


.. contents:: Contents


Thus, you have a complete abstraction from the data source, whether it's REST-API, MBaaS, SaaS, IndexedDB, HTML, third-party service for JSON-RPC protocol or `Service Stub`_.

    "We often forget that it is also best to postpone decisions until the last possible moment.
    This isn’t lazy or irresponsible; it lets us make informed choices with the best possible information.
    A premature decision is a decision made with suboptimal knowledge. We will have that
    much less customer feedback, mental reflection on the project, and experience with our
    implementation choices if we decide too soon."
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_)

..

    A good architecture allows major decision to be deferred! (`Robert Martin <https://youtu.be/Nltqi7ODZTM?t=19m40s>`__)

.. A good architecture allows you to defer critical decisions, it doesn’t force you to defer them. However, if you can defer them, it means you have lots of flexibility.
   («Clean Architecture» [#fnca]_)

..

    You would make big decisions as
    late in the process as possible, to defer the cost of making the decisions and to have
    the greatest possible chance that they would be right. You would only implement
    what you had to, in hopes that the needs you anticipate for tomorrow wouldn't come
    true.
    (Kent Beck [#fnxp]_)

In addition, you have the opportunity to implement patterns `Identity Map`_ and `Unit of Work`_.
The last one is very often in demand, since it allows you to save only changed objects of the finally formed aggregate of nested objects on the server, or roll back the state of local objects in case the data can not be saved (the user has changed his mind or entered invalid data).


Domain Model
============

The greatest advantage of the `Domain Model`_ in the program is the ability to use the principles of Domain-Driven Design (DDD) [#fnddd]_.
If the Models contain only business logic, and are devoid of service logic, then they can easily be read by domain expert (ie, the customer's representative).
This frees you from the need to create UML diagrams for discussions and allows you to achieve the highest level of mutual understanding, productivity, and quality of implementation of the models.

In one project I tried to implement a fairly complex domain logic (which contained about 20 domain model) in the paradigm of reactive programming with push-algorithm, when the attributes of the model instance, containing the aggregation annotations or dependent on them, change its values by reacting to changes in other models and storages.
The bottom line is that all this reactive logic no longer belonged to the domain model itself, and was located in a different sort of `Observers <Observer_>`__ and handlers.

    "The whole point of objects is that they are a technique to package data with the processes used
    on that data. A classic smell is a method that seems more interested in a class other than the one
    it actually is in. The most common focus of the envy is the data."
    («Refactoring: Improving the Design of Existing Code» [#fnrefactoring]_)

..

    "Good design puts the logic near the data it operates on."
    (Kent Beck [#fnxp]_)

..

    "If the framework's partitioning conventions pull apart the elements implementing the
    conceptual objects, the code no longer reveals the model.

    There is only so much partitioning a mind can stitch back together, and if the framework uses 
    it all up, the domain developers lose their ability to chunk the model into meaningful pieces."
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

This led to such a huge number of intricacies of listeners that the superiority in performance was lost, but before that was lost readability.
Even I could not understand the next day what a particular code fragment does, I'm not talking about the domain expert.
This radically destroyed the principles of Domain-Driven Design, and significantly :doc:`reduced the speed of developing new project features <../en/how-to-quickly-develop-high-quality-code>`.

Hopes for this approach finally collapsed when it was revealed that each instance of the model is to change the values of its attributes that contain aggregate annotations or dependent upon, depending on the context of use (display selected group or filter criteria).

Subsequently, the models recovered their conceptual outlines and code readability, the push algorithm was replaced by a pull-algorithm (to more more precisely, a hybrid push-pull), and at the same time there was preserved the mechanism of reactions for adding, changing or deleting objects.
To achieve this result, I had to create my own library implementing the Repository pattern, since I could not find existing solutions for relational data with quality code base.
This is similar to Object-Relational Mapping (ORM) for JavaScript, including the Data Mapper pattern (the data can be mapped between objects and a persistent data storage).


Reactive programming paradigm
=============================

Today it is fashionable to get involved in reactive programming.
Did you know that dojo developers first `applied reactive programming <https://github.com/dojo/dojo/commit/4bd91a5939d4dbc8a43d673cc279bb3d39ed0895#diff-48ec1f2998cbe6d644df0c9abd32d9d0R35>`__ in their implementation of the Repository pattern as early as September 13, 2010?

Reactive programming complements (rather than contrasts) the `Repository`_ pattern, as it's evidenced by the experience of `dojo.store`_, `Dstore`_ and the new `Dojo 2 - data stores <https://github.com/dojo/stores>`_.

The developers of dojo are a team of highly qualified specialists whose libraries are used by such reputable companies as IBM.
An example of how seriously and comprehensively they solves problems is the `history of the RequireJS library <http://requirejs.org/docs/history.html>`_.


Examples of implementations of Repository pattern and ORM by JavaScript
=======================================================================

Examples of the simplest implementations of the Repository pattern by JavaScript in the project `todomvc.com <http://todomvc.com/>`_:

- Angular2: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angular2/app/services/store.ts
- Angular1: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angularjs/js/services/todoStorage.js
- React: https://github.com/tastejs/todomvc/blob/gh-pages/examples/react-alt/js/stores/todoStore.js

Other implementations:

- `Dojo2 Stores <https://github.com/dojo/stores>`_ - \
  Excellent implementation of `Repository`_ pattern in paradigm of `Reactive Programming`_ for non-relational data.
- `Dstore <http://dstorejs.io/>`_ - \
  yet another excellent implementation of `Repository`_ pattern.
- `Dojo1 Store <https://dojotoolkit.org/reference-guide/1.10/dojo/store.html>`_ - \
  Dojo1 implementation of `Repository`_ pattern.
- `JS-Data <http://www.js-data.io/>`_ - \
  Object-Relational Mapping (ORM) written by JavaScript for relational data. Does not support composite relations.
- `9 JavaScript Libraries for Working with Local Storage <https://www.sitepoint.com/9-javascript-libraries-working-with-local-storage/>`_ - \
  article with interesting comments.
- `Kinvey Data Store <http://devcenter.kinvey.com/angular/guides/datastore>`_ - \
  implementation of `Repository`_ pattern by MBaaS Kinvey, `source code <https://github.com/Kinvey/js-sdk/tree/master/src/datastore/src>`__
- `Pocket.js <https://github.com/vincentracine/pocketjs>`_ - \
  a wrapper for the window.localStorage. It provides helpful methods which utilise MongoDB's proven syntax and provides a powerful lightweight abstraction from the complexity of managing and querying local storage.

I would like to add here `Ember.js <https://emberjs.com/>`_, but it implements the `ActiveRecord`_ pattern.


Implementation of relational relations
======================================


Synchronous programming
-----------------------

At the dawn of ORM, the Data Mappers retrieved from the database all related objects with a single query (see `example of implementation <https://bitbucket.org/emacsway/openorm/src/default/python/>`_).

Domain-Driven Design approaches relations more strictly, and considers relations from the point of view of conceptual contour of an aggregate of nested objects [#fnddd]_.
The object can be accessed either by reference (from the parent object to the embedded object) or through the Repository.
It is also important the direction of relations and the principle of minimal sufficiency ("distillation of models" [#fnddd]_).

    In real life, there are lots of many-to-many associations, and a great number are naturally
    bidirectional. The same tends to be true of early forms of a model as we brainstorm and explore
    the domain. But these general associations complicate implementation and maintenance.
    Furthermore, they communicate very little about the nature of the relationship.

    There are at least three ways of making associations more tractable.

    1. Imposing a traversal direction
    2. Adding a qualifier, effectively reducing multiplicity
    3. Eliminating nonessential associations

    It is important to constrain relationships as much as possible. A bidirectional association means
    that both objects can be understood only together. When application requirements do not call for
    traversal in both directions, adding a traversal direction reduces interdependence and simplifies
    the design. Understanding the domain may reveal a natural directional bias.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

..

    Minimalist design of associations helps simplify traversal and limit the explosion of relationships
    somewhat, but most business domains are so interconnected that we still end up tracing long,
    deep paths through object references. In a way, this tangle reflects the realities of the world,
    which seldom obliges us with sharp boundaries. It is a problem in a software design.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

With the advent of ORM, lazy evaluation actively began to use to resolve ties synchronous programming.
Python community actifely uses `Descriptors <https://docs.python.org/3/howto/descriptor.html>`__ for this purpose, but Java - AOP and Cross-Cutting Concerns [#fnccode]_.

The key is to free the Domain Model from the data access logic.
This is required by the principle of clean architecture to reduce coupling (`Coupling`_), and by the principle of simplicity of testing.
The greatest success is achieved by the principle of Cross-Cutting Concerns which completely frees the model from the service logic.

With the advent of ORM the implementation of relations has become so easy that no one longer think about it.
Where unidirectional relations are required, developers can easily apply bidirectional relations.
Utilities for optimizing the selection of related objects have appeared, which implicitly preload all related objects, which significantly reduces the number of calls to the database.


Rejecting relations
-------------------

It is worth mentioning another widespread point of view, which says that an object should not be responsible for its relations, and only Repository can have an exclusive right to access the object.
Some respected by me friends adhere to this point of view.


Asynchronous programming
------------------------

The rise in popularity of asynchronous applications has forced us to reconsider the established notions about the implementation of lazy relations.
Asynchronous access to each lazy relation of each object significantly complicates the clarity of the program code and prevents optimization.

This has increased the popularity of object-oriented database in asynchronous programming that allows to save aggregates entirely.
Increasingly, REST-frameworks began to be used to `transfer aggregates of nested objects to the client <http://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects>`_.

    To do anything with an object, you have to hold a reference to it. How do you get that reference?
    One way is to create the object, as the creation operation will return a reference to the new
    object. A second way is to traverse an association. You start with an object you already know and
    ask it for an associated object. Any object-oriented program is going to do a lot of this, and these
    links give object models much of their expressive power. But you have to get that first object.

    I actually encountered a project once in which the team was attempting, in an enthusiastic
    embrace of MODEL-DRIVEN DESIGN , to do all object access by creation or traversal! Their objects
    resided in an object database, and they reasoned that existing conceptual relationships would
    provide all necessary associations. They needed only to analyze them enough, making their entire
    domain model cohesive. This self-imposed limitation forced them to create just the kind of endless
    tangle that we have been trying to avert over the last few chapters, with careful implementation of
    ENTITIES and application of AGGREGATES . The team members didn't stick with this strategy long, but
    they never replaced it with another coherent approach. They cobbled together ad hoc solutions
    and became less ambitious.

    Few would even think of this approach, much less be tempted by it, because they store most oftheir objects in relational databases.
    This storage technology makes it natural to use the third way
    of getting a reference: Execute a query to find the object in a database based on its attributes, or
    find the constituents of an object and then reconstitute it.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

The need for processing aggregates has intensified interest in functional programming, especially in combination with reactive programming paradigm.

However, the solution to one problem creates another problem.


Functional Programming
----------------------

Functional programming is more difficult to use for domain objects, since it is more difficult to structure logically (especially if programming language does not support `multiple dispatching <https://en.wikipedia.org/wiki/Multiple_dispatch>`__).
This often leads to unreadable code that expresses not "what" it does, but "how" it does something incomprehensible.

    If you wanted polymophism in C, you’d have to manage those pointers yourself;
    and that’s hard. If you wanted polymorphism in Lisp you’d have to manage those pointers yourself (pass them in as arguments to some higher level algorithm (which, by the way IS the Strategy pattern.))
    But in an OO language, those pointers are managed for you.
    The language takes care to initialize them, and marshal them, and call all the functions through them.

    ... There really is only one benefit to Polymorphism; but it’s a big one. It is the inversion of source code and run time dependencies.
    («OO vs FP» [#fnoovsop]_)

..

    However, my experience is that the cost of change rises
    more steeply without objects than with objects.
    (Kent Beck [#fnxp]_)

And yet, not clear intentions and objectives of the author - is a key issue when reading someone else's code.

    A six-month study
    conducted by IBM found that maintenance programmers "most
    often said that understanding the original programmer's intent was
    the most difficult problem" (Fjelstad and Hamlen 1979).
    («Code Complete» [#fncodec]_)

As it mentioned in the article ":doc:`../en/how-to-quickly-develop-high-quality-code`", the developer reads the code 91% of the time while constructing the code, and only 9% of the time he enters the characters with keyboard.
And this means that poorly readable code affects 91% of the development velocity.

Also, this approach destroys all the benefits of using Domain-Driven Design and pull apart the elements implementing the conceptual objects, which leads to the code that no longer expresses the model.

All this `contributed to the appearance <https://groups.google.com/d/msg/reactjs/jbh50-GJxpg/82CHQKeaG54J>`__ in the ReactJS community of such libraries as:

- `Normalizr <https://github.com/paularmstrong/normalizr>`_ - \
  Normalizes (decomposes) nested JSON according to a schema.
- `Denormalizr <https://github.com/gpbl/denormalizr>`_ - \
  Denormalize data normalized with normalizr.


Minor offtopic
--------------

Despite the fact that functional programming techniques are often used together with the paradigm of reactive programming, in their essence these paradigms are not always suitable for combination in the canonical form for web development.

This is because reactive programming is based on the propagation of changes, i.e. it implies the existence of variables and assignment.

    This means that it becomes possible to express static (e.g. arrays) or dynamic (e.g. event emitters) data streams with ease via the employed programming language(s), and that an inferred dependency within the associated execution model exists, which facilitates the automatic propagation of the change involved with data flow.

    For example, in an imperative programming setting, ``a := b + c`` would mean that ``a`` is being assigned the result of ``b + c`` in the instant the expression is evaluated, and later, the values of ``b`` and/or ``c`` can be changed with no effect on the value of ``a``.
    However, in reactive programming, the value of ``a`` is automatically updated whenever the values of ``b`` and/or ``c`` change;
    without the program having to re-execute the sentence ``a := b + c`` to determine the presently assigned value of ``a``.

    ... For example, in an model–view–controller (MVC) architecture, reactive programming can facilitate changes in an underlying model that automatically are reflected in an associated view, and contrarily.
    ("`Reactive programming <https://en.wikipedia.org/wiki/Reactive_programming>`__", wikipedia)

That is why reactive programming paradigm `can be combined with different paradigms <https://en.wikipedia.org/wiki/Reactive_programming#Approaches>`__, imperative, object-oriented and functional.

However, the whole point of the matter is that in the canonical form of functional programming does not has variables (from the word "vary"), i.e. changeable state:

    A true functional programming language has no assignment operator.
    You cannot change the state of a variable.
    Indeed, the word “variable” is a misnomer in a functional language because you cannot vary them.

    ...The overriding difference between a functional language and a non-functional language is that functional languages don’t have assignment statements.

    ... The point is that a functional language imposes some kind of ceremony or discipline on changes of state. You have to jump through the right hoops in order to do it.

    And so, for the most part, you don’t.
    («OO vs FP» [#fnoovsop]_)

Therefore, the use of functional programming techniques does not make the program functional until the program has a variable state - it's just procedural programming.
And if so, then the rejection of Domain-Driven Design just takes away the superiority of both approaches (neither object-oriented programming polymorphism nor the immutability of functional programming), and combines the all worst, similar to hybrid objects [#fnccode]_, and does not make program really functional.

    Hybrids

    This confusion sometimes leads to unfortunate hybrid structures that are half object and
    half data structure. They have functions that do significant things, and they also have either
    public variables or public accessors and mutators that, for all intents and purposes, make
    the private variables public, tempting other external functions to use those variables the
    way a procedural program would use a data structure (this is sometimes called Feature Envy from "Refactoring" [#fnrefactoring]_).
    Such hybrids make it hard to add new functions but also make it hard to add new data
    structures. They are the worst of both worlds. Avoid creating them. They are indicative of a
    muddled design whose authors are unsure of—or worse, ignorant of—whether they need
    protection from functions or types.
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_)

Canonical functional programming has no state and therefore ideally suited for distributed computing and data flow processing.

    The benefit of not using assignment statements should be obvious.
    You can’t have concurrent update problems if you never update anything.

    Since functional programming languages do not have assignment statements, programs written in those languages don’t change the state of very many variables.
    Mutation is reserved for very specific sections of the system that can tolerate the high ceremony required.
    Those sections are inherently safe from multiple threads and multiple cores.

    The bottom line is that functional programs are much safer in multiprocessing and multiprocessor environments.
    («OO vs FP» [#fnoovsop]_)

Does this mean that the object-oriented programming paradigm is opposed to the functional programming programming?

Despite the fact that the OOP paradigm is traditionally considered as a kind of imperative paradigm, i.e. based on the state of the program, Robert C. Martin makes an amazing conclusion - as objects provide their interface, i.e. behavior, and hide their state, they do not contradict the functional programming paradigm.

    "Objects are not data structures.
    Objects may use data structures; but the manner in which those data structures are used or contained is hidden.
    This is why data fields are private.
    From the outside looking in you cannot see any state.
    All you can see are functions.
    Therefore Objects are about functions not about state."
    («OO vs FP» [#fnoovsop]_)

That's why some classical functional programming languages support OOP:

- `Enhanced Implementation of Emacs Interpreted Objects <https://www.gnu.org/software/emacs/manual/html_mono/eieio.html>`_
- `Common Lisp Object System <https://en.wikipedia.org/wiki/Common_Lisp_Object_System>`_

    Are these two disciplines mutually exclusive?
    Can you have a language that imposes discipline on both assignment and pointers to functions?
    Of course you can.
    These two things don’t have anything to do with each other.
    And that means that OO and FP are not mutually exclusive at all.
    It means that you can write OO-Functional programs.

    It also means that all the design principles, and design patterns, used by OO programmers can be used by functional programmers if they care to accept the discipline that OO imposes on their pointers to functions.
    («OO vs FP» [#fnoovsop]_)

Of course, objects in functional programming `must be immutable <https://youtu.be/7Zlp9rKHGD4?t=50m>`__.

Objects can be emulated even by functional programming languages using closures, see article "`Function As Object <https://martinfowler.com/bliki/FunctionAsObject.html>`_" by Martin Fowler.
Here you can not ignore the wonderful book "`Functional Programming for the Object-Oriented Programmer <https://leanpub.com/fp-oo>`_" by Brian Marick.

Let's remember the chapter "Chapter 6. Working Classes: 6.1. Class Foundations: Abstract Data Types (ADTs): Handling Multiple Instances of Data with ADTs in Non-Object-Oriented Environments" книги «Code Complete» [#fncodec]_.

    An abstract data type is a collection of data and operations that work on that data.
    («Code Complete» [#fncodec]_)

..

    Abstract data types form the foundation for the concept of classes.
    («Code Complete» [#fncodec]_)

..

    Thinking about ADTs first and classes second is an example of programming into a language vs. programming in one.
    («Code Complete» [#fncodec]_)

I'm not here to rewrite all the advantages of ADT, you can read it in this chapter of this book.

But the original question was whether we should abandon the ADT in an object-oriented language for the design of domain objects in favor of "`Anemic Domain Model`_"?
And should we sacrifice all the benefits of Domain-Driven Design for the sake of the convenience of a particular implementation of relation resolving?

    The bottom, bottom line here is simply this.
    OO programming is good, when you know what it is.
    Functional programming is good when you know what it is.
    And functional OO programming is also good once you know what it is.
    («OO vs FP» [#fnoovsop]_)

It is also worth noting that not all kinds of relationships fit into the concept of aggregate.
If the object does not logically belong to the aggregate, then we can not put it into the aggregate for the sake of the convenience of resolving the relations.
For in this case, the interface will follow the implementation, which fundamentally destroys the fundamental principle of abstraction.
Also, the concept of an aggregate can not be used to emulate Many-To-Many relations and cross-link hierarchies.


Implementation of relations by assigning
----------------------------------------

The principle of physical assignment of related objects is `implemented also by the library js-data <http://www.js-data.io/v3.0/docs/relations#section-eagerly-loading-relations>`__.

In our library, we implemented both the ability to decompose aggregates of nested objects and the ability to compose aggregates from flat data of Repositories.
Moreover, the aggregate always keeps the actual state.
When you add, change, delete an object in the Repository, the changes automatically propagate to the structures of the corresponding aggregates.
The library implements this behavior as in the paradigm of reactive programming, as well as in the paradigm of event-driven programming (optional).

There is also the ability to create bidirectional relations.
But, despite the fact that modern interpreters able to easily collect garbage with reference cycles, it's better when child objects are not aware of their parents from a conceptual point of view, if you don't have a strong reason for that.

Thus, the implementation of communications does not require any service data access logic for the object, that provides zero `Coupling`_ and absolutly clear domain models.
This means that domain model can be instance of the "class" Object.

I also took into account the point of view that the domain model should not be responsible for the relations.
Therefore, there is the possibility of easy access to any object through its Repository.


Source code
===========

* Edge (unstable) repo - https://github.com/emacsway/store
* Canonical repo - https://github.com/joor/store-js-external

Эта статья на Русском языке ":doc:`../ru/javascript-and-repository-pattern`".


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnpoeaa] «`Patterns of Enterprise Application Architecture`_» by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans
.. [#fngof] «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#fnoovsop] «`OO vs FP`_» by Robert C. Martin
.. [#fnca] «`Clean Architecture`_» by Robert C. Martin
.. [#fntca] «`The Clean Architecture`_» by Robert C. Martin
.. [#fnxp] «`Extreme Programming Explained`_» by Kent Beck


.. update:: 04 Oct, 2017


.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Code Complete: http://www.informit.com/store/code-complete-9780735619678
.. _Robert C. Martin: http://informit.com/martinseries
.. _Patterns of Enterprise Application Architecture: https://www.martinfowler.com/books/eaa.html
.. _Refactoring\: Improving the Design of Existing Code: https://martinfowler.com/books/refactoring.html
.. _Martin Fowler: https://martinfowler.com/aboutMe.html
.. _Extreme Programming Explained: http://www.informit.com/store/extreme-programming-explained-embrace-change-9780321278654
.. _OO vs FP: http://blog.cleancoder.com/uncle-bob/2014/11/24/FPvsOO.html
.. _Clean Architecture: https://8thlight.com/blog/uncle-bob/2011/11/22/Clean-Architecture.html
.. _The Clean Architecture: https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html

.. _ActiveRecord: http://www.martinfowler.com/eaaCatalog/activeRecord.html
.. _Domain Model: http://martinfowler.com/eaaCatalog/domainModel.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _Query Object: http://martinfowler.com/eaaCatalog/queryObject.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Stub: http://martinfowler.com/eaaCatalog/serviceStub.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html
.. _Anemic Domain Model: http://www.martinfowler.com/bliki/AnemicDomainModel.html

.. _Coupling: http://wiki.c2.com/?CouplingAndCohesion
.. _Cohesion: http://wiki.c2.com/?CouplingAndCohesion
.. _Observer: https://en.wikipedia.org/wiki/Observer_pattern
.. _Reactive Programming: https://en.wikipedia.org/wiki/Reactive_programming
.. _dojo.store: https://dojotoolkit.org/reference-guide/1.10/dojo/store.html
.. _Dstore: http://dstorejs.io/
