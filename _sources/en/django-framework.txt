
About my experience of using Django Framework
=============================================

.. post:: Jul 26, 2017
   :language: en
   :tags: Django, ORM
   :category:
   :author: Ivan Zakrevsky
   :exclude:

   Django framework allows you to quickly solve a huge range of tasks and easily find developers. With a competent approach, you can use all the advantages of Django and not become a hostage of its shortcomings.

At one time, someone beautifully said that security is a balance between the cost of protection and the potential benefits of hacking.
There is no sense to exceed this balance.

Taking a decision on IT-technologies, we are also trying to find a balance between the costs of maintaining technology (including search and training of new staff) and the functionality that is being acquired.

Django framework, of course, brings some trouble, but at the same time it allows you to solve a huge range of tasks quickly and easily find the developers.
In other words, Django framework makes software development cheaper.
With a competent approach, you can use all the advantages of Django and not become a hostage of its shortcomings.

.. contents:: Contents

Django ORM brings the most trouble, so we'll start with it.


Django ORM problems and their solutions
=======================================


Semantic coupling of model validation
-------------------------------------

The principle of "Defensive Programming" [#fncodec]_ requires making it impossible to create an invalid object.
You must use object setters for validation.
In Django, we have to explicitly call the method `Model.full_clean() <https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.full_clean>`_ of an object before saving, that, of course, often no one does, and this often leads to various troubles.
This problem is known as "Semantic Coupling" as well as "G22: Make Logical Dependencies Physical" [#fnccode]_ and "G31: Hidden Temporal Couplings" [#fnccode]_.
You can solve this problem technically, but usually it's enough just to follow the development discipline.


Active Record
-------------

Django ORM implements the `ActiveRecord`_ pattern, which makes it easy to use due to violation of the `Single responsibility principle`_ (SRP) principle, for this reason it is often called antipattern.
This pattern mixes business logic and data access logic in one class.
Unfortunately, this simplicity is appropriate only in simple cases.
In a more serious application, there are more problems than advantages.

Since Django does not use the `Repository`_ layer, it would be desirable to hide the implementation of access to the data source by the Service Layer, see the article ":doc:`service-layer`".
This is necessary because the capabilities of Django ORM are not always enough to build complicated queries or to create complicated models, and you have to replace Django ORM with third-party tools or a bare implementation of `DataMapper`_ pattern (we will return to this issue a little later).
In any case, the implementation of data access must be hidden from the application, and this is one of the responsibilities of the Service Layer.


Identity Map
------------

Django does not implement the pattern `Identity Map`_, and, as a result, creates many duplicate queries.
Part of this weakness is mitigated by the presence of `prefetch_related() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#prefetch-related>`_.
There are implementations of this pattern in the form of third-party libraries,
`django-idmapper <https://github.com/dcramer/django-idmapper>`_,
`django-idmap <https://pypi.python.org/pypi/django-idmap>`_.
But they do not perform any functions except caching, and do not provide transactional data consistency.
However, you hardly notice this problem, since the Django application usually processes an HTTP-request inside one transaction.


Transactional consistency of data
---------------------------------

Django allows you to create multiple instances of the same domain object in the thread's memory, and this can lead to data loss due to the dissynchronization of the state of these instances.
Worse still, these instances do not synchronize their state with their records in the database at the time of the commit (rollback) of the transaction.

Django supports transactions, but does not support the transactional consistency of the data, unlike the Storm ORM / SQLAlchemy.
You have to take care about the state model instances in the memory at the time of the commit (rollback) of the transaction.

For example, if you use the transaction isolation level "Repeatable read", after the transaction is committed, the status of your model instances in the memory may become outdated.
Accordingly, when you roll back a transaction, you must return the initial state to them.

As previously mentioned, this is not critical for HTTP request processing, since Django framework usually serves it with one transaction.
But when you develop command-line scripts or scheduled tasks, you need to take this into account.

You must also take care of yourself to prevent Deadlock_, since the Django ORM does not implement the `Unit of Work`_ pattern and does not use topological sorting.

It is worth also mention the frequent problem of novice developers, who are trying to process a large collection of objects without using `select_for_update() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#select-for-update>`_.
The processing of the collection takes a considerable amount of time, which is enough for the loaded object, waiting for its processing, to change the record in the database.
Unskilful use of transactions can lead to the loss of parallel changes, and skillful use can lead to an unresolvable conflict.

In addition, you should carefully read all the precautions of the `iterator() <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#iterator>`_ method, the use of which does not guarantee that there is no memory leak if you do not use `SSCursor <https://github.com/farcepest/MySQLdb1/blob/master/doc/user_guide.rst#using-and-extending>`_ for MySQL.


Service Layer and django.db.models.Manager
------------------------------------------

A common mistake is using the django.db.models.Manager class as a Service Layer.
This question was considered in detail in the article ":doc:`service-layer`".


Composite foreign keys and Django ORM
-------------------------------------

As you can see from the ticket `#373 <https://code.djangoproject.com/ticket/373>`_ and the discussion of "`Multi-Column Primary Key support <https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys>`_", Django ORM does not yet support composite relations.

This means that you have to create surrogate keys, which can cause certain difficulties in the integration of an existing database, or you have to use one of these libraries:

- `django-compositekey <https://pypi.python.org/pypi/django-compositekey>`_
- `django-composite-foreignkey <https://pypi.python.org/pypi/django-composite-foreignkey>`_
- `django-compositepk <https://pypi.python.org/pypi/django-compositepk>`_

Frankly, I have not used these libraries.
In that case, I just do not use Django ORM.
But you have a choice.


Building of complicated SQL-queries for Django ORM
--------------------------------------------------

The capabilities of the Django ORM interface are not enough to build complicated SQL queries.
In this case, you have to either use third-party tools that will be discussed later, or use Raw-SQL.
In any case, the details of implementation should be encapsulated within a query factory class.

In my practice there was a case when it was necessary to implement a user search by pattern matching (LIKE '% keyword%') in the `admin panel <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/>`__ using the user table joined with the table of profiles (using LEFT JOIN).

Moreover, the search criteria had to be combined with the OR condition, this leaded to a complete pass through the attached table for each row of the user table.
There were several million MySQL database entries, and it worked very slowly.
That version of MySQL did not yet support ngram FULLTEXT index.
To optimize the query, we had to join the already filtered result from the profile table instead of the entire profile table, by moving the selection criterion to a subquery.
A similar example can be found in the book «High Performance MySQL» [#hpmysql]_.
To solve the problem my colleague had to :doc:`make an adapter for sql-builder Storm ORM <storm-orm>` like `sqlalchemy-django-query <https://github.com/mitsuhiko/sqlalchemy-django-query>`__.
As a result, it became possible to express an SQL query of any complexity in the interface of django.db.models.query.QuerySet.


Implementation of complicated Models for Django Framework
---------------------------------------------------------

Very often you have to deal with objects that contain aggregated data, annotations, or combine the data of several tables.

SQLAlchemy certainly provides `more flexible features <http://docs.sqlalchemy.org/en/rel_1_1/orm/nonstandard_mappings.html>`_.
But even these features `are not always enough <http://robbygrodin.com/2017/04/18/wayfair-blog-post-orm-bankruptcy/>`__.

The annotations of Storm ORM / SQLAlchemy are implemented more successfully.
Annotations of Django ORM is better not to use at all, in favor of a bare implementation of the pattern Data Mapper.
The fact is that the model scheme is constantly evolving, and new fields are constantly added to it.
And it often happens that the name of the new field is already used by the annotation that leads the conflict in the namespace.
The solution can be to separate the namespace by using a separate model or Wrapper for annotations over the model instance.

Identity Map is another reason not to use the Django ORM annotations (and also be careful with prefetch_related()).
After all, if there is only one instance of an object in the thread, then its state can not have any differences for each particular request.

That is why it is important to hide the implementation details of the data access using `Repository`_ pattern or `Service Layer`_.
In this case, I just make an implementation in the form of the bare pattern `DataMapper`_ and the plain `Domain Model`_.

Practice shows that such cases usually do not exceed 10%, which is not so significant for refusal from Django ORM, because the attractiveness of easy hiring of specialists still outweighs.


Third-party tools
-----------------


SQLAlchemy
^^^^^^^^^^

Django has several applications for SQLAlchemy integration:

- `django-sqlalchemy <https://github.com/auvipy/django-sqlalchemy>`_
- `aldjemy <https://github.com/Deepwalker/aldjemy>`_
- `django-sabridge <https://github.com/johnpaulett/django-sabridge>`_
- `sqlalchemy-django-query <https://github.com/mitsuhiko/sqlalchemy-django-query>`_


SQLBuilder
^^^^^^^^^^

To build complicated queries for Django ORM, I usually use the library `sqlbuilder <http://sqlbuilder.readthedocs.io/en/latest/>`_.

Good manners require you to create a separate factory class for each query to hide implementation details from the application.
Within the interface of this class, you can easily replace one implementation with another.


Storm ORM
^^^^^^^^^

The issue of integration of Storm ORM has already been considered, so I'll just give the links:

- ":doc:`storm-orm`"
- ":doc:`../ru/build-raw-sql-by-storm-orm`"


Testing
^^^^^^^

If you use several data access technologies, then it's worth mentioning the fake data generator `mixer <https://github.com/klen/mixer>`_, which supports several ORMs.
Other generators `can be found <https://djangopackages.org/grids/g/fixtures/>`__, as usual, on `djangopackages.org <https://djangopackages.org/>`_.


Cache invalidation
------------------

Django ORM implements the `ActiveRecord`_ pattern, which forces us to explicitly call `Model.save() <https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.save>`_ method.
The problem is that the `post_save <https://docs.djangoproject.com/en/1.11/ref/signals/#post-save>`_ and `pre_delete <https://docs.djangoproject.com/en/1.11/ref/signals/#pre-delete>`_ signals are often used by developers to invalidate the cache.
This is not quite the right way, since Django ORM does not use the `Unit of Work`_ pattern, and the time between saving and committing the transaction is sufficient to parallel thread could recreate the cache with outdated data.

On the Internet, you can find libraries that allow you to send a signal when the transaction is committed (use search query "django commit signal" on pypi.python.org).
Django 1.9 and above allows you to use `transaction.on_commit() <https://docs.djangoproject.com/en/1.11/topics/db/transactions/#django.db.transaction.on_commit>`_, which partially solves the problem if you do not use replication.

I use the library `cache-dependencies <https://bitbucket.org/emacsway/cache-dependencies>`_, as I wrote in the article ":doc:`cache-dependencies`".


Django REST framework
=====================

If we have previously considered the shortcomings of Django ORM, the `Django REST framework`_ surprisingly turns its disadvantages into advantages, because the interface for building Django ORM queries is great for REST.

If you were lucky enough to use `Dstore`_ on the client side, then you can use `django-rql-filter <https://pypi.python.org/pypi/django-rql-filter>`_ or `rql <https://pypi.python.org/pypi/rql>`__ on the server side.

Frankly, the Django REST framework makes a lot of time for the debugger, and this, of course, characterizes its design solutions not from the best side.
A good program should be read, not understood, and even more so without the help of a debugger.
This characterizes the observance of the main imperative of software development:

    Software's Primary Technical Imperative is managing complexity. This is greatly
    aided by a design focus on simplicity.
    Simplicity is achieved in two general ways: minimizing the amount of essential
    complexity that anyone's brain has to deal with at any one time, and keeping
    accidental complexity from proliferating needlessly.
    («Code Complete» [#fncodec]_)

However, the overall balance of advantages and disadvantages makes the Django REST framework very attractive for development, especially if you need to involve new (or temporary) developers or allocate some of the work for outsourcing.

You just have to take into account that there is a certain entry barrier, which requires certain costs to overcome it, and you need to understand what benefit you can get from this, because not always this benefit is worth the effort to overcome the entrance barrier.

I will not dwell on the criticism of the design decisions, the Django REST framework does not restrict me in anything constructively, and this is most important.


Related fields with _id suffix for Django REST framework
--------------------------------------------------------

When you use client-side tools to handle foreign keys, you might want to use \*_id suffix for the fields with foreign key values.
Here is an `implementation example <https://github.com/OpenSlides/OpenSlides/commit/f6c50a966d84b6c8251b9b8e7556623bae40f8f6>`__ how this can be achieved.
The same example on the `gist <https://gist.github.com/ostcar/eb78515a41ab41d1755b>`__ and `discussion <https://github.com/encode/django-rest-framework/issues/3121>`__.


SQLAlchemy
----------

The huge advantage of Django REST framework is that it is ORM agnostic.
It has perfect interfacing with Django ORM, but it can easily work with a bare implementation of the Data Mapper pattern which returns a `namedtuple`_ collection for some `Data Transfer Object`_.
It also has good integration with `SQLAlchemy`_ in the form of a third-party application `djangorest-alchemy <https://github.com/dealertrack/djangorest-alchemy>`_ (`docs <http://djangorest-alchemy.readthedocs.io/en/latest/>`__).
See also `discussion of the integration <https://github.com/encode/django-rest-framework/issues/2439>`__.


OpenAPI и Swagger
-----------------

Django REST framework allows you to `generate scheme OpenAPI <www.django-rest-framework.org/api-guide/schemas/>`_ and integrates with `swagger <https://swagger.io/>`_ using the `django-rest-swagger <https://django-rest-swagger.readthedocs.io/en/latest/>`_ library.

This opens up unlimited possibilities for generating `Service Stub`_ for clients and also allows using one of the existing stab generators for swagger.
This allows you to test client-side without any server-side implementation, divide the responsibility between client-side and server-side developers, quickly find the cause of problems, freeze the communication protocol, and, most importantly, allows you to develop client-side in parallel even if server-side implementation is not finished yet.

OpenAPI schema could also be used to automatically generate tests, for example, using the `pyresttest <https://github.com/svanoort/pyresttest>`_.

My friend works on the `python-easytest <https://bitbucket.org/sergeyglazyrindev/python-easytest>`_ library, which eliminates the need for writing integration tests and performs the testing of the application using the OpenAPI scheme.


JOIN-s problem
--------------

The Django REST framework is often used together with `django-filter <https://pypi.python.org/pypi/django-filter>`_.
And here there is a problem, which is reflected in the documentation as:

        "To handle both of these situations, Django has a consistent way of processing filter() calls.
        Everything inside a single filter() call is applied simultaneously to filter out items matching
        all those requirements. Successive filter() calls further restrict the set of objects,
        but for multi-valued relations, they apply to any object linked to the primary model,
        not necessarily those objects that were selected by an earlier filter() call."

        See more info on:
        https://docs.djangoproject.com/en/1.8/topics/db/queries/#lookups-that-span-relationships

To solve this problem, you should use a wrapper with lazy evaluation in the FilterSet() class instead of the real django.db.models.query.QuerySet, which will fully match its interface, but will call the filter() method once, passing all accumulated selection criteria to it.


Generating \*.csv, \*.xlsx
--------------------------

Django and Django REST framework has a lot of extensions.
This is a major advantage for which it makes sense to tolerate their shortcomings.
You can even generate \*.csv, \*.xlsx files:

- `django-rest-framework-excel <https://github.com/diegueus9/django-rest-framework-excel>`_
- `django-rest-framework-csv <https://github.com/mjumbewu/django-rest-framework-csv>`_
- `django-rest-pandas <https://github.com/wq/django-rest-pandas>`_
- etc.

However, there is a problem with translating the nested data structures into the flat list, and vice versa, with the parsing of the flat list into the nested data structure.
Partially this problem can be solved using the library `jsonmapping <https://github.com/pudo/jsonmapping>`_.
But this decision did not suit me, and I have done a complete declarative data mapper.


Graphql
=======

- `graphene-django <https://github.com/graphql-python/graphene-django>`_ - a Django integration for `graphene <https://github.com/graphql-python/graphene>`_.


Advantages and disadvantages of Django Framework
================================================


Advantages
----------

Django has a successful `View <https://docs.djangoproject.com/en/1.11/topics/http/views/>`__, which is a kind of the pattern `Page Controller`_, fairly successful forms and template (if you use `django.template.loaders.cached.Loader <https://docs.djangoproject.com/en/1.11/ref/templates/api/#django.template.loaders.cached.Loader>`_).

Despite all the shortcomings of Django ORM, its query building interface is well suited for the REST API.

Django has a huge community with a huge number of ready-made applications.
It is very easy to find developers (and outsourcing companies) for Django and Django REST framework.

Django declares such a way of development, which is not exacting to the skill level of developers.

Django can save a lot of time and financial resources if used properly.


Disadvantages
-------------

The level of complexity of Django grows with each release, often outstripping the opportunities it implements, and from this its attractiveness is constantly decreasing.

If you need to adapt Django ORM for your needs, then it's probably more difficult to do this with the latest release than to adapt SQLAlchemy.
And it needs to adapt more often than SQLAlchemy.
Simplicity is no longer the main prerogative of Django, as it was in earlier versions.
Almost in all projects that I had to deal with, Django ORM was supplemented (or replaced) with third-party tools or bare implementation of the Data Mapper pattern.

In the circle of my friends Django framework is used mainly because of habit and inertia.

Despite the fact that Django framework has a huge number of ready-made applications, their quality often leaves much to be desired, or even contains bugs.
Moreover, very insidious bugs may appear, which only appear in a multi-threaded environment under high loads, and which are very difficult to debug.

The quality of developers specializing in Django is also often low.
Highly skilled developers from my friends try to avoid working with Django.


Conclusion
==========

Whether to use Django framework depends on what goals you set for yourself and how qualified are the teams you have.

If your team is highly qualified in the field of architecture and design, you use :doc:`collaborative development techniques <../en/how-to-quickly-develop-high-quality-code>` for the dissemination of experience, have sufficient resources and finances to make the project more better without Django, then it makes sense to use another stack of technologies.

Otherwise the Django framework can do you a good favor.
A lot of overconfident teams could not make without Django their projects better than they would have make with it.

Nobody obliges you to use Django anytime and anywhere.
Django REST framework allows you to abstract from Django ORM and even from its serializer.

If you are engaged in outsourcing, your average project lasts no more than a year, the budget is low and the deadlines are short, then Django has a lot to offer you.

If you are working on a large ongoing project, the benefits are not so obvious.
All the matter in the balance that you need to determine for themselves.

But if you use `Bounded Contexts <https://martinfowler.com/bliki/BoundedContext.html>`_ or `Microservice Architecture <https://martinfowler.com/articles/microservices.html>`_, then each team can decide on their own technology stack.
You can use Django only for part of the project, or use only some of the Django Framework components.

And you can not use it at all.
Among the alternatives, I advise you to pay attention to the web-framework that impresses me `wheezy.web <https://pypi.python.org/pypi/wheezy.web>`_.


Эта статья на Русском языке ":doc:`../ru/django-framework`".


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#hpmysql] «High Performance MySQL» by Baron Schwartz, Peter Zaitsev, and Vadim Tkachenko


.. update:: 04 Aug, 2017


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
