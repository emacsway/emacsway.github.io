
.. post:: Oct 10, 2015
   :language: en
   :tags: ORM, Storm ORM, DataMapper, DB, SQL, Python
   :category:
   :author: Ivan Zakrevsky


Why I prefer Storm ORM for Python
=================================

I began using `KISS`_-style `Storm ORM`_ for enterprise applications on Python, let me explain why.

.. contents:: Contents


.. _orm-criteria-en:

My requirements for ORM
=======================

\- **Quickness**. ORM should be fast.
ORM should have `Identity Map`_ to prevent duplicated queries to DB if the object is already loaded to the memory.
This is important for case when several isolated scopes are trying to load the same object to the own namespace.
Also, I think, `Identity Map`_ should be configurable for different transaction isolation levels, for example, to prevent query to DB when object does not exist and transaction isolation level is "Serializable".

\- **Simplicity**. ORM should not scare you from debugger, you have to understand what it does by browsing the source code.
Any product sooner or later can be dead, or author can lose the interest in it, thus you should be able to support the product yourself.
New developers of the team should be able to master the ORM quickly.
The single source of truth about the code is the code itself.
Documentation and comments is good, but they are not always comprehensive and actual.
And often the product should be adapted, extended for your requirements.
Thus, simplicity is important.

\- **Architecture**. Proper separation of abstraction layers, adherence to the basic principles of architecture (such as `SOLID`_).

If you are not able to use some component of the ORM separately, for example SQLBuilder, then, probably, it would be better to use raw pattern DataMapper_ instead of the ORM.
Well designed ORM allows you to use its components separately, such as `Query Object`_ (SQLBuilder), Connection, `DataMapper`_, `Identity Map`_, `Unit of Work`_, `Repository`_.
Does the ORM allow you to use Raw-SQL (entirely or partially)?
Are you able to use only Data Mapper (without Connection, SQLBuilder etc.)?
Are you able to substitute the Data Mapper by `Service Stub`_, to be free from DB for testing?

Usually the possibilities of any ORM have to be expanded.
Are you able to extend your ORM without monkey-patching, forks, patches?
Does the ORM follow to the `Open/Closed Principle`_ (OCP)?

    "The primary occasion for using Data Mapper is when you want the database schema and the object model to evolve independently. The most common case for this is with a Domain Model (116). Data Mapper's primary benefit is that when working on the domain model you can ignore the database, both in design and in the build and testing process. The domain objects have no idea what the database structure is, because all the correspondence is done by the mappers."
    («Patterns of Enterprise Application Architecture» [#fnpoeaa]_)

\- `ACID`_. Good ORM takes care of that the object has always been consistent to the record of the DB.

Suppose, you have loaded the object in the memory, and then executed transaction commit.
The object has a lot of references to it, but the object has been updated by a concurrent process.
If you try to modify the object, the changes of the concurrent process will be lost.
When you are doing transaction commit, you have to synchronize the object to the record of the DB, and at the same time to keep alive all references to the object.
See also this `article <http://techspot.zzzeek.org/2012/11/14/pycon-canada-the-sqlalchemy-session-in-depth/>`__ and `presentation <http://techspot.zzzeek.org/files/2012/session.key.pdf>`__.
To ensure the integrity of data, the transaction support alone is not enough for the application.
Of course, this is not a critical requirement, but without it you can not completely hide the source of data in the code.

\- **Hiding the data source**. A good ORM allows you to forget about its existence, and handle instances of models as if they were ordinary objects.
It would not disclose the source of the data by requiring you to explicitly call the method to save the objects.
It would not oblige you to "reload" objects.
It makes it easy to replace the mapper, even if you change the relational database to non-relational.

Imagine that you have created two new objects, one of which refers to another with foreign key.
Could you create a link between them before at least one of them had been stored in the database and had been received the primary key?
Would the value of the foreign key of the associated object be updated when the first object saved and the primary key is received?

A good ORM prevents the deadlock, because it saves all objects just before the commit, minimizing the time interval from the first save to the commit.
Also it allows you to influence the order of saving objects, for example, using topological sorting to prevent the deadlock.


.. _storm-orm-advantages-en:

Advantages
==========

Despite the release number, the code is fairly stable.
Successful architecture in combination with the KISS_ principle creates a false illusion that the Storm ORM is allegedly not developing.
This is not true.
In fact, there's simply nothing to develop.
For three years of investigation of the source code of Storm ORM, I did not find anything that could be improved.
Storm ORM can be extended, but not improved.
`Commits occur regularly <https://code.launchpad.net/storm>`__.
But they can be described as "polishing".

Storm ORM supports composite keys and relations (after Django ORM I sighed with relief).

It allows you to express SQL queries of almost any complexity (at least constructively).

It works with any number of databases.

It implements `DataMapper`_ pattern, which means classes of models free of metadata and database access logic, as if it were `ActiveRecord`_.
Model class can be inherited from the bare class `object`_.

Due to `Identity Map`_, `Storm ORM`_ is very fast.
On the page of one project, after the introduction of Storm ORM (instead of Django ORM), the time consumption by ORM had been reduced from 0.21 seconds to 0.014 seconds (i.e. 15 times), and the total page generation time had been reduced by half, from 0.48 seconds to 0.24 seconds.
The number of queries to the database had been reduced from 88 to 7.
Identity Map makes also utilities like prefetch_related() unnecessary, but only for foreign keys referencing the primary key.

It is very pleasant to work with the code Storm ORM.
Here you can find a lot of interesting techniques to achieve high performance.
We must pay tribute to the developers Storm ORM, - they made a real intellectual feat.
whole code is carefully thought out.
Any attempt to improve its code usually only convince us of the correctness of existing solutions.

Storm ORM handles transactions correctly.
You can't found find thoughtless reconnect here when connection is lost during an incomplete transaction.
The connection could be restored only if it could not affect the integrity of the data.
The transactions are implemented in two levels.
In the case of transaction rollback, the state of objects in the memory will be also rolled back.

Storm ORM is able to compile a selection criteria to the collection of filters of Python-code, which can be applied to any collection of objects in the memory.
This feature allows you to create a dummy mapper for tests.
To select objects from ``Store()`` by primary key (even from a Foreign Key) you don't have to do anything, because due to `Identity Map`_ pattern you don't have to send objects to the database, thus you are able to use (partially) `Identity Map`_ as dummy mapper.

Storm ORM does not convert values immediately, at the time of loading the object.
Instead, it simply wraps the value in the wrapper (adapter) - the Variable class.

This approach allows you:

- Control the assignment and access policy.
- Optimize resource consumption (call-by-need lazy conversion will delay the action until the value is needed).
- Keep the initial value of each attribute, observe the changes, perform rollback at the object level.
- Watch for value changes (the observer) and update related objects.
- Synchronize the value of the object with the value of the database record.
- Implement "Defensive Programming" and prevent assignment of invalid value. You are not able to forget validation before saving anymore. This solves "G22: Make Logical Dependencies Physical" [#fncc]_ and "G31: Hidden Temporal Couplings" [#fncc]_.
- Validate the value only when it is assigned from the outside, but not from the database. This eliminates the problem of the impossibility of re-saving the objects when validation rules are changed.
- Convert the value to the required representation, depending on the context of the usage (Python or DB).

The last one, however, has some nuances.

For example, we add a selection criterion::

    (GeoObjectModel.point == author_instance.location)

Converter of which attribute should be used here, ``GeoObjectModel.point`` or ``AuthorModel.location``?
Obviously ``AuthorModel.location`` because it provides value.
But here converter of ``GeoObjectModel.point`` will be used.
What happens if these converters have different behavior?
And what happens if we pass such a criterion: ``Func('SOME_FUNCTION_NAME', AuthorModel.location)``?

To be fair, Storm ORM made a major breakthrough in ordering the conversion issue, compared to most other ORMs, and created the right grounding to create the ideal conversion.
If you follow simple rules, converters will work perfectly correctly (to achieve this, you must pass the `Variable() instance  <http://bazaar.launchpad.net/~storm/storm/trunk/view/477/storm/store.py#L597>`__ to the selection criteria, i.e. wrapped value).
Many other ORMs do not have this technical capability at all, because they perform the conversion when the object is created.
In other words, the converters of other ORMs are actually tied to the type of value and not to a particular attribute (as the model definition declares this), which makes them virtually useless, because this `responsibility already is imposed for the connector <http://initd.org/psycopg/docs/advanced.html#adapting-new-python-types-to-sql-syntax>`__.

Storm ORM does not impose you a way to obtain a connection.
You `can easily <http://bazaar.launchpad.net/~storm/storm/trunk/view/477/storm/database.py#L502>`__ share a connection between two ORMs or use `some special way <http://eventlet.net/doc/modules/db_pool.html>`__ of getting a connection.

Storm ORM `does not oblige <https://lists.ubuntu.com/archives/storm/2009-June/001010.html>`__ to declare a database schema in the code.
This corresponds to the `DRY`_ principle, since the schema already exists in the database.
Also, complete control of the database schema `can be achieved easier by the facilities of the database <https://blogs.gnome.org/jamesh/2007/09/28/orm-schema-generation/>`__.
Usually large projects, which use replication and sharding, use own tools to control the database schema.
You also able to use package `storm.schema <http://bazaar.launchpad.net/~storm/storm/trunk/files/477/storm/schema/>`__ from Storm ORM.
`Unlike to SQLAlchemy <http://docs.sqlalchemy.org/en/rel_1_1/core/reflection.html>`__, Storm ORM does not provide automatical loading of undeclared properties of model from the DB.
It can be implemented easily, but there is two points. First, you have to perform DB-query at the level of initialization of the code of module. Second, it's not enough to browse source code to understand the schema of model anymore.
Also, some different types of Python can have the single data-type of DB, thus, the DB schema is not enough to declare model classes correctly.

Other advanteges you can see at the `Tutorial <https://storm.canonical.com/Tutorial>`__ and `Manual <https://storm.canonical.com/Manual>`__


.. _about-sqlalchemy-en:

About SQLAlchemy
================

Any `ORM is good <http://aosabook.org/en/sqlalchemy.html>`__, if it `implements principles <http://techspot.zzzeek.org/2012/02/07/patterns-implemented-by-sqlalchemy/>`__ of popular book «Patterns of Enterprise Application Architecture» [#fnpoeaa]_.
Storm ORM is distinguished by its simplicity from SQLAlchemy, like VIM from Emacs, or jQuery from Dojo.
Ideologically, they have a lot in common, I would say that the Storm ORM is a simplified version of SQLAlchemy.
You would have studied the source code of Storm ORM much faster than introduction of tutorial of SQLAlchemy.
You can extend and adapt Storm ORM for your requirements much faster than you would have understood the way to implement it for SQLAlchemy.

But there is a border that makes SQLAlchemy more preferable than Storm ORM.
If the functionality of Storm ORM suits you, you "wield a pen", and have the time to adapt the library to your needs, then Storm ORM looks more attractive.
Otherwise, SQLAlchemy becomes preferable, even despite the level of complexity, because it provides a lot of solutions "out of the box".


.. _storm-orm-disadvantages-en:

Disadvantages
=============

There were three cases in my practice, when I had to add a few features to Storm ORM, which already was implemented by SQLAlchemy (or its community).

1. `Bulk inserting of objects <http://docs.sqlalchemy.org/en/rel_1_1/orm/session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects>`__, moreover, using the clause ON DUPLICATE KEY UPDATE.
2. Adaptation of `SQL Builder for interface of Django ORM <https://github.com/mitsuhiko/sqlalchemy-django-query>`__.
3. Support the pattern `Concrete Table Inheritance <http://docs.sqlalchemy.org/en/rel_1_1/orm/extensions/declarative/inheritance.html#concrete-table-inheritance>`__

Storm ORM `does not use thread locking <https://bugs.launchpad.net/storm/+bug/1412845>`__ for lazy modification of critical global metadata.
This is not a problem, and can be easily solved (it's enough to fulfill them immediately, under the lock).
But you have to know this, otherwise your server will have gone down for highly concurrent threads.

Most likely, you would have to extend Storm ORM.
The possibilities of SQL-builder should be extended.
Utils like prefetch_related() for OneToMany() would be useful.
Probably, you may need to implement a cascade deletion using ORM, not a database.
And implement an object serializer.
Storm ORM does not implement the topological sort, but allows you to implement it easily.

Class Store (which is an implementation of pattern Repository) combines also the responsibility of DataMapper_ and it's not so well.
For example, this creates a problem for implementing the pattern `Class Table Inheritance`_.
Storm ORM's core developers advice `to replace Inheritance with Delegation <https://storm.canonical.com/Infoheritance>`__ (However, postgresql `supports inheritance <postgresql inheritance_>`__ itself (`DDL <postgresql inheritance DDL_>`__)).
The lack of the dedicated class for DataMapper forces you to clutter the domain model with `service logic <https://storm.canonical.com/Manual#A__storm_pre_flush__>`__.

.. Дескрипторы связей Storm ORM запрашивают store у объекта.
   Таким образом, если объект приаттачен к фиктивному стору, то и связи он будет искать в фиктивном сторе.
   Таким образом, дескрипторы не представляют никаких проблем для подмены реального стора на фиктивный.

.. По этим причинам мне захотелось сделать `ascetic ORM <https://bitbucket.org/emacsway/ascetic>`__ который был бы еще проще (который, впрочем, на сегодня является не более чем сборищем незавершенных мыслей).


.. _storm-orm-ambiguities-en:

About ambiguous
===============

ACID support has led to the fact that the domain model is not really pure.
The domain model has pure interface, behaves like realy plain object, and is inherited from the ``object`` class.
In fact, the instance of the model does not contain data, but refers to the data structure through descriptors.
It's a titanic work to implement it in the KISS style.
Although I'm not sure that the implementation of such a complex mechanism corresponds to the principle of KISS.
Perhaps, simplicity of implementation here would be preferable, rather than simplicity of the interface.
However, this makes one argument less against the ORM.

In addition, this solution does not provide full consistency of all available behaviors for use.
Suppose you have created two new objects, the first of which refers to the second on the foreign key.
Then you created a link between them with a descriptor.
Before commit, you are able `to get the second object using the descriptor of the foreign key of the first object <https://storm.canonical.com/Tutorial#References_and_subclassing>`__.
But you aren't able to get the second objet by using the repository (i.e. class Store).
When you do commit, the both objects receive primary keys, and the value of the foreign key are automatically updated.
From now on you can get the second object by the repository.


.. _storm-orm-faq-en:

FAQ
===

*q: Storm ORM does not support Python3.*

a: If you migrated at least one library in Python3, then you understand that this process does not cause major difficulties.
The command ``2to3`` does 95% of work.
The only significant problem is the migration of the C-extension.
Storm ORM is fast enough even without the C-expansion, and does not lose much in performance.
You can find the C-extension for Python3 `here <http://bazaar.launchpad.net/~martin-v/storm/storm3k/view/head:/storm/cextensions.c>`__ (`diff <http://bazaar.launchpad.net/~martin-v/storm/storm3k/revision/438>`__).
There is also yet another `py3 branch <https://code.launchpad.net/~hackedbellini/storm/py3>`__.


*q: How to use Storm ORM with partial Raw-SQL*

a: It's better to avoid to do it, and extend the SQL-builder. But if you really need::

    >>> from storm.expr import SQL
    >>> from authors.models import Author
    >>> store = get_my_store()
    >>> list(store.find(Author, SQL("auth_user.id = %s", (1,), Author)))
    [<authors.models.Author object at 0x7fcd64cea750>]


*q: In which way I can use Storm ORM with a fully Raw-SQL, to get the result of query with instances of the models?*

A: Since Storm ORM uses the Data Mapper, Identity Map and Unit of Work patterns, you have to specify all the model fields in the query, and use the method ``Store._load_object()``::

    >>> store = get_my_store()
    >>> from storm.info import get_cls_info
    >>> from authors.models import Author

    >>> author_info = get_cls_info(Author)

    >>> # Load single object
    >>> result = store.execute("SELECT " + store._connection.compile(author_info.columns) + " FROM author where id = %s", (1,))
    >>> store._load_object(author_info, result, result.get_one())
    <authors.models.Author at 0x7fcc76a85090>

    >>> # Load collection of objects
    >>> result = store.execute("SELECT " + store._connection.compile(author_info.columns) + " FROM author where id IN (%s, %s)", (1, 2))
    >>> [store._load_object(author_info, result, row) for row in result.get_all()]
    [<authors.models.Author at 0x7fcc76a85090>,
     <authors.models.Author at 0x7fcc76a854d0>]


.. _why-orm-en:

Do you really need ORM?
=======================

Honestly, there is no need to use ORM always and everywhere.
In many cases (for example, if the application needs to simply return a list of JSON values), the simplest `Table Data Gateway`_ is enough, which returns the list of simplest `Data Transfer Object`_.
This is an issue of personal preferences.


.. _why-query-object-en:

Do you really need Query Object?
--------------------------------

The only thing I'm absolutely sure of is that it's difficult (if at all possible) do without without the `Query Object`_ pattern (which is also named as SQLBuilder).

\1. Even the most staunch adherents of the "pure SQL" concept quickly encounter the inability to express the SQL query in the pure form, and then they are forced to dynamically compose the query depending on the conditions.
But this is already a kind of SQLBuilder concept, albeit in a primitive form, and implemented in a particular way.
The particular solutions always take a lot of place, as they depart from the `DRY`_ principle.

Let me explain it with an example.
Imagine a query to select ads from the database by 5 criteria.
You need to allow users to select the ads using a set of any number of the following criteria:

0. Without criteria.
1. By ad type.
2. By country, region, city.
3. By categories, including nested categories.
4. By users (all ads of the same user)
5. By search words.

Altogether, you would have to prepare 2 ^ 5 = 32 fixed SQL-requests on condition you didn't take into account the nestings of tree structures (otherwise 3-d criterion would have to be divided into 3 more criteria, as often the data is stored denormalized).

The list of possible combinations of criteria::

    0
    1
    1,2
    1,2,3
    1,2,3,4
    1,2,3,4,5
    1,2,4
    1,2,4,5
    1,2,5
    1,3
    1,3,4
    1,3,4,5
    1,3,5
    1,4
    1,4,5
    1,5
    2,
    2,3
    2,3,4
    2,3,4,5
    2,3,5
    2,4
    2,4,5
    2,5
    3
    3,4
    3,4,5
    3,5
    4
    4,5
    5

If we added yet another criterion, it would be 2^6=64 combinations, i.e. in 2 times more.
One more, it would be 2^7=128 combinations.

128 fixed queries forces us to abandon the concept of "pure SQL" in favor of the concept of "dynamic building of SQL-query."
The method that creates this query would take a lot of arguments, and this would affect the cleanness of the code.
You could divide the method by responsibilities, so that each method would build its part of the query.
But firstly, this approach would have created the SQL-builder in a particular way (violation of the `DRY`_ principle).
And secondly, if you continued to clean up the methods, to free they from dependencies, and to increase the `Cohesion`_ of the classes, then you would eventually come to the Criteria classes and implement the `Query Object`_ pattern.
Again, attempts to break this method would lead to a reduction in `Cohesion`_ of the class.
To restore the `Cohesion`_, you have to extract Criteria classes.

In other words, you would create actually an SQL-builder which could be extracted to a separate library and could be evolved independently.

But what would happen if you didn't "clean up" the methods, didn't release them from dependencies and didn't increase the `Cohesion`_ of classes? You would get an unreadable messian with a lot of SQL pieces scattered across different methods.
Sometimes such "pieces" can take the form of static methods of a class, which acquires the signs "G18: Inappropriate Static" [#fncc]_, and according to the recommendations of Robert C. Martin, there should be extracted the polymorphic object `Criteria`_.
In any case, the readability (the most important advantage) of such "pure SQL" would be lost (it would be even worse than the readability of the query which is created by SQL-builder).

SQL-builders exists only because they are maximally implement the principle of `Single responsibility principle`_ (SRP).
In the "Chapter 10: Classes. Organizing for Change" of the widely known book «Clean Code: A Handbook of Agile Software Craftsmanship» [#fncc]_, C.Martin demonstrates the achievement of the `SRP`_ principle in the example of SQL-builder.

Similar to hybrid object, that contains disadvantages of data structures and objects, SQL-builder implemented in particular way contains disadvantages of both concepts.
They do not have the readability of Raw-SQL, nor the convenience of complete SQL-builders.
This forces us to abandon the dynamic construction, in favor of readability of the code, or to bring the levels of abstraction up to a complete SQL-builder.

Also the concept of "pure SQL" is not feasible in the implementation of the following patterns and approaches:

- Dynamically change the sorting
- Multilanguage implemented with suffixed columns
- `Concrete Table Inheritance`_
- `Class Table Inheritance`_
- `Entity Attribute Value`_
- etc.

\2. Raw-SQL can not use inheritance without `parsing <https://pypi.python.org/pypi/sqlparse>`__ (for example, to change the ORDER DY clause), this usually entails full copying of the Raw-SQL if you want to change a small its part.
You have to support each copy of the Raw-SQL separately, that makes the support a more difficult.
However, at leisure I had wrote the simplest `mini-builder, which represents the Raw-SQL query in the form of a multilevel list of Raw-SQL pieces <http://sqlbuilder.readthedocs.io/en/latest/#short-manual-for-sqlbuilder-mini>`__. This approach allows you to build conditionally-compound SQL-queries and also preserves the readability of Raw-SQL.

\3. I often had to see diffs of Version Control System with several hundred lines among the files with Raw-SQL just because a new attribute was added to the model. This has the signs of "Divergent Change" [#fnr]_ and "Shotgun Surgery" [#fnr]_.
This is because Raw-SQL queries contain many duplicate expressions.
And it is also true the rule "G5: Duplication" [#fncc]_ ("Duplicated Code" [#fnr]_).
SQLBuilder allows you to avoid this problem, because it keeps all metadata of the query (for example the list of fields) in the single place.

\4. When the concept of Raw-SQL is used, the method to create query usually accepts the selection criteria in the form of method's arguments with plain values.
When you need add yet another selection criteria or field, you have to change interface of the method (or add yet another method), but this violates the `Open/Closed Principle`_ and has signs of "Divergent Change" [#fnr]_ and "Shotgun Surgery" [#fnr]_.

This issue should be solved by using "`Introduce Parameter Object`_" [#fnr]_ in the form of class Criteria of pattern `Query Object`_.
In this case all selection criteria would be encapsulated in the single composite object (see `Composite pattern`_).
This approach also eliminates conditions from the methods, and fulfills the "`Replace Conditional with Polymorphism`_" [#fnr]_.

A human operates objects in his imagination (and in the program code).
The sorting method and its direction - characterize the state of the object.
Selection criteria are also objects that express the database behavior, and have own behavior (they are able to create compositions and render its state in several forms).
And you expect this behavior from they.
When you mean objects, but do not express them in code, the program loses the ability to express the developer's intent ("G16: Obscured Intent" [#fncc]_).

\5. If some value of the model instance requires a special conversion to the DB representation, you have to clutter the code explicitly calling these conversions.

\6. There is a tendency (which I regularly see) to use the pattern `Repository`_ in combination with Raw-SQL.
Since the Repository pattern is designed to hide the data source, it is not clear how to pass the selection criteria in the Repository so that they are completely abstract from the data source, i.e. are abstract from Raw-SQL.

In a primitive case this, of course, is not a problem (you can pass them by keyword arguments to the function, although this causes the problems described in clause 4).

But if your Criteria have an arbitrary quantity and needs to use nested operators ("OR", "AND", "XOR") with different precedences, then there is a problem, and the solution of the problem is the responsibility of the pattern Query Object.
Your method can accept Raw-SQL as arguments, but this approach has the signs "G6: Code at Wrong Level of Abstraction" [#fncc]_ and "G34: Functions Should Descend Only One Level of Abstraction" [#fncc]_.

\7. Quite often string formatting is used to build conditionally-compound SQL-queries.
The problem is that the object that wants to use this SQL-query in a slightly modified form should be aware of the details of implementation of the mechanism for this modification.
This entails the emergence of a logical dependence and a violation of encapsulation.

To save the encapsulation and remove the logical dependence, the object which is aware about details of implementetion of query modification, should contain all methods to create any query required by each client.
But an object should not make assumptions about clients!

Otherwise, we receive a God object which is aware of the needs of all potential clients.

This violates OCP and entails the emergence of "Divergent Change" [#fnr]_ and "Shotgun Surgery" [#fnr]_.
Often there is garbage in the form of unclaimed methods, after removing objects using them.
Very large classes are usually broken up using inheritance or composition.
This leads to the fact that in order to get the complete idea of what the method does, you need to repeatedly interrupt the view for research the contents of various methods, classes, and even files.

The Query Object pattern provides the unified interface for query modification, which frees the object with query state from the need to know about the needs of its clients.

\8. I would like also to raise the issue of using the language syntax constructions to construct the SQL-queries.

There is a few examples:

* `A Query Language extension for Python <https://github.com/pythonql/pythonql>`_: Query files, objects, SQL and NoSQL databases with a built-in query language
* `simpleql <https://bitbucket.org/robertodealmeida/simpleql/>`_ SQL table using nothing but Python to build the query
* `Generator expressions <http://code.activestate.com/recipes/442447/>`__ for database requests (Python recipe)

I'll say subjectively, I like to use objects for this.
Moreover, I like when the syntactic constructions of a language are represented by objects, as in Smalltalk.


.. _why-datamapper-en:

Do you really need Data Mapper?
-------------------------------

First of all, you need to decide whether the application needs the pattern `Domain Model`_ or the pattern `Transaction Script`_.
This question is considered well by «Patterns of Enterprise Application Architecture» [#fnpoeaa]_, so I will not dwell on it.
If the Domain Model is better suited for your application, then it will be difficult to do without an ORM (at least artisanal), for high-quality, convenient and fast work.

There are several arguments against ORM.
I don't consider obsolete issues like the databases do not support inheritance.

First of all, some databases `support inheritance <postgresql inheritance_>`__ (`DDL <postgresql inheritance DDL_>`__).

Secondly, inheritance can be replaced by a composition.
By the way, the usefulness of inheritance in OOP is still a `discussed issue <http://www.javaworld.com/article/2073649/core-java/why-extends-is-evil.html>`__.
Go-lang has no inheritance in favor of the composition.
Inside programming languages inheritance is implemented using the composition.

Thirdly, today only the lazy doesn't know about the patterns
`Single Table Inheritance`_,
`Concrete Table Inheritance`_,
`Class Table Inheritance`_ and
`Entity Attribute Value`_.

Therefore, I will touch only on two important issues in my opinion:

1. Shold be the data in memory an object or an data structure?
2. ACID, consistency of the object in memory and its record in the database.

I do not have the unequivocal opinion on the first question.
We live in the world of objects, and that's why object-oriented programming has emerged.
It's easier for human to think by objects.
In Python, even elementary types are complete objects, with methods, inheritance, and so on.

What is the difference between a data structure and an object? In Python, this difference is highly conditional.
Objects use data presentation on an abstract level.

    "Objects hide their data behind abstractions and expose functions that operate on that data. Data structure expose their data and have no meaningful functions."
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fncc]_)

Again we return to the issue of Domain Model vs Transaction Script, because the domain model grasps behavior (functions) and properties (data).

There is yet another important point.
Suppose we store two columns in the database - the price and the currency.
Or, for example, a data of polymorphic relation - the type of object and its identifier.
Or the coordinates - x and y.
Or the path of a tree structure - a country, a region, a city, a street.
In other words, the aggregate of data form a single entity, and changing one part of this data does not make any sense without a corresponding change to the other part.
How to set data access policy and ensure atomicity of their changes (except the use of objects or immutable types)?

First of all, we need to think about the business problems.
That's why Domain-Driven Design was emerged.
Issues of implementation should not dictate the business logic.
The issue of storage of information must satisfy our requirements, and not specify requirements to us.
If this were not so, then object-oriented programming would not have arisen yet.

    "The whole point of objects is that they are a technique to package data with the processes used
    on that data. A classic smell is a method that seems more interested in a class other than the one
    it actually is in. The most common focus of the envy is the data."
    («Refactoring: Improving the Design of Existing Code» [#fnr]_)    

..

    "Now this design has some problems. Most important, the details of the table structure have leaked
    into the DOMAIN LAYER ; they should be isolated in a mapping layer that relates the domain objects
    to the relational tables. Implicitly duplicating that information here could hurt the modifiability and
    maintainability of the Invoice and Customer objects, because any change to their mappings now
    have to be tracked in more than one place. But this example is a simple illustration of how to keep
    the rule in just one place. Some object-relational mapping frameworks provide the means to
    express such a query in terms of the model objects and attributes, generating the actual SQL in
    the infrastructure layer. This would let us have our cake and eat it too."
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

..

    The greatest value I've seen delivered has been when a narrowly scoped framework automates a
    particularly tedious and error-prone aspect of the design, such as persistence and object-relational
    mapping. The best of these unburden developers of drudge work while leaving them complete
    freedom to design.
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

One of the main principles of object-oriented programming is encapsulation.
The `Single responsibility principle`_ proclaims that each object must have one responsibility and this responsibility must be completely encapsulated in its class.
Depriving the object of behavior, we impose its behavior on another object, which must serve the first.
The question is whether it is justified?
This is obvious for the Active Record partition on Data Mapper and Domain Model, because it's aimed at achieving the Single responsibility principle, but the answer is not so obvious for the object.
The behavior object begins to "envy" the data object "G14: Feature Envy" [#fncc]_, ("Feature Envy" [#fnr]_), with signs "F2: Output Arguments" [#fncc]_, "Convert Procedural Design to Objects" [#fnr]_,  "Primitive Obsession" [#fnr]_ and "Data Class" [#fnr]_.

The arguments on this subject in the article "`Anemic Domain Model`_" of M.Fowler.

    "High class and method counts are sometimes the result of pointless dogmatism. Consider, for example, a coding standard that insists on creating an interface for each and every class. Or consider developers who insist that fields and behavior must always be separated into data classes and behavior classes. Such dogma should be resisted and a more pragmatic approach adopted."
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fncc]_)

..

    "If the framework's partitioning conventions pull apart the elements implementing the
    conceptual objects, the code no longer reveals the model.

    There is only so much partitioning a mind can stitch back together, and if the framework uses 
    it all up, the domain developers lose their ability to chunk the model into meaningful pieces."
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

About the second question.

Of all the ORMs that I met in my practice (not only in Python), ACID support in Storm ORM and SQLAlchemy is implemented in the best way.
Most of the existing ORM do not even try to solve this issue.

Martin Fowler reasoning on this point in the article "`Orm Hate`_".

Article "`Dance you Imps! <https://8thlight.com/blog/uncle-bob/2013/10/01/Dance-You-Imps.html>`__" by Robert Martin.

In general, my attitude towards ORM is ambiguous.
I often use raw DataMapper_ pattern for complicated queries with annotations or aggregations (especially in Django-applications), but I use ORM more often.
Too many existing ORMs create more "code smells" in the code than it eliminates, but Storm ORM is not one of them.

Interview with Gustavo Niemeyer, lead developer on Canonical's Storm project "`Storm: An ORM for Python <http://www.drdobbs.com/storm-an-orm-for-python/201000460>`__".


Afterword
=========

Storm ORM is the tool for highly skilled professionals who understand its superiority and are not afraid to support 300 KB of high-quality code themselves.


Эта статья на Русском языке ":doc:`../ru/storm-orm`".


.. rubric:: Footnotes

.. [#fncc] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» `Robert C. Martin`_
.. [#fnr] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#fnpoeaa] «Patterns of Enterprise Application Architecture» by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans


.. update:: 31 Jul, 2017


.. _Refactoring\: Improving the Design of Existing Code: http://martinfowler.com/books/refactoring.html
.. _Refactoring Ruby Edition: http://martinfowler.com/books/refactoringRubyEd.html
.. _Anemic Domain Model: http://www.martinfowler.com/bliki/AnemicDomainModel.html
.. _Orm Hate: http://martinfowler.com/bliki/OrmHate.html
.. _Martin Fowler: http://martinfowler.com/

.. _ActiveRecord: http://www.martinfowler.com/eaaCatalog/activeRecord.html
.. _Class Table Inheritance: http://martinfowler.com/eaaCatalog/classTableInheritance.html
.. _Concrete Table Inheritance: http://martinfowler.com/eaaCatalog/concreteTableInheritance.html
.. _DataMapper: http://martinfowler.com/eaaCatalog/dataMapper.html
.. _Data Transfer Object: http://martinfowler.com/eaaCatalog/dataTransferObject.html
.. _Domain Model: http://martinfowler.com/eaaCatalog/domainModel.html
.. _Entity Attribute Value: https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model
.. _Gateway: http://martinfowler.com/eaaCatalog/gateway.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _Query Object: http://martinfowler.com/eaaCatalog/queryObject.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Stub: http://martinfowler.com/eaaCatalog/serviceStub.html
.. _Single Table Inheritance: http://martinfowler.com/eaaCatalog/singleTableInheritance.html
.. _Table Data Gateway: http://martinfowler.com/eaaCatalog/tableDataGateway.html
.. _Transaction Script: http://martinfowler.com/eaaCatalog/transactionScript.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html
.. _Criteria: `Query Object`_
.. _SQLBuilder: `Query Object`_

.. _Introduce Parameter Object: http://www.refactoring.com/catalog/introduceParameterObject
.. _Replace Conditional with Polymorphism: http://www.refactoring.com/catalog/replaceConditionalWithPolymorphism.html

.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Robert C. Martin: http://informit.com/martinseries

.. _SOLID: https://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _Open/Closed Principle: https://en.wikipedia.org/wiki/Open/closed_principle
.. _OCP: `Open/Closed Principle`_
.. _Single responsibility principle: https://en.wikipedia.org/wiki/Single_responsibility_principle
.. _SRP: `Single responsibility principle`_

.. _ACID: https://en.wikipedia.org/wiki/ACID
.. _Cohesion: https://en.wikipedia.org/wiki/Cohesion_%28computer_science%29
.. _Composite pattern: https://en.wikipedia.org/wiki/Composite_pattern
.. _DRY: https://en.wikipedia.org/wiki/Don't_repeat_yourself
.. _KISS: https://en.wikipedia.org/wiki/KISS_principle
.. _object: https://docs.python.org/2/library/functions.html#object
.. _Storm ORM: https://storm.canonical.com/
.. _KISS principle: `KISS`_
.. _KISS-style: `KISS`_
.. _postgresql inheritance: http://www.postgresql.org/docs/9.4/static/tutorial-inheritance.html
.. _postgresql inheritance DDL: http://www.postgresql.org/docs/9.4/static/ddl-inherit.html
