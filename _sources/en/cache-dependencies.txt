
About problems of cache invalidation. Cache tagging.
====================================================


.. post:: May 21, 2016
   :language: en
   :tags: cache
   :category:
   :author: Ivan Zakrevsky

About my experience of solving problems of cache invalidation and principles of the library `cache-dependencies`_.

.. contents:: Contents


The problem of cache dependencies
=================================

When some data has been updated, all dependent caches should be reset.
Suppose, the cache of main page of a company site contains an instance of Product model.
When the instance of Product model has been updated, the cache should be updated too.
Another example, when attributes of User model (for example, last_name) has been updated, all caches of posts of the user, contained the last_name, should be reset too.

Usually, the pattern `Observer`_ (or its variety pattern Multicast) is responsible for the cache invalidation.
But even in this case the invalidation logic becomes too complicated, the achieved accuracy is too low, the `Coupling`_ is growing fast, and encapsulation is disclosed.

The solution of the issue can be cache tagging (i.e. marking cache by tags).
For example, the cache of main page can be marked by tag ``product.id:635``.
The all user's posts can be marked by tag ``user.id:10``.
Post lists can be marked by composite tag, composed of selection criteria, for example ``type.id:1;category.id:15;region.id:239``.

Now it's enough to invalidate a tag to invalidate all dependent caches.
This approach is not new, and widely used in other programming languages.
At one time it was even implemented in memcache, see `memcached-tag <http://code.google.com/p/memcached-tag/>`_.

See also:

- `Cache dependency in wheezy.caching <https://pypi.python.org/pypi/wheezy.caching>`_
- `TaggableInterface of ZF <http://framework.zend.com/manual/current/en/modules/zend.cache.storage.adapter.html#the-taggableinterface>`_
- `TagDependency of YII framework <http://www.yiiframework.com/doc-2.0/yii-caching-tagdependency.html>`_
- `Dklab_Cache: правильное кэширование — тэги в memcached, namespaces, статистика <http://dklab.ru/lib/Dklab_Cache/>`_


Overhead of cache reading vs overhead of cache creation
=======================================================

How to implement invalidation of caches dependent on the tag?
There are two options:

\1. Destroy physically all dependent caches on the tag invalidation.
Implementation of this approach requires some overhead on the cache creation to add key of the cache into the cache list (or set) of the tag (for example, using `SADD <http://redis.io/commands/sadd>`_).
The disadvantage is that the invalidation of too many dependent caches takes some time.

\2. Just change the version of tag on the tag invalidation.
Implementation of this approach requires some overhead on the cache reading to verify the version of each tag of the cache with the actual tag version.
So, the cache should contain all tag versions on the cache creation.
If any tag version is expired on the cache reading, the cache is invalid.
The advantage of this approach is immediate invalidation of the tag and all dependent caches.
Another advantage is that premature discarding of a tag info is not possible (using LRU_), because the tag info is read mush often than dependent caches.

I've chosen the second option.


Tagging of nested caches
========================

Because tags are verified at the moment of cache reading, let's imagine, what happens, when one cache will be nested to other cache.
Multi-level cache is not so rarely.
In this case, the tags of inner cache will never be verified, and outer cache will alive with outdated data.
At the moment of creation the outer cache, it must accept the all tags from the inner cache into own tag list.
If we pass the tags from the inner cache to the outer cache in an explicit way, it violates encapsulation!
So, cache system must keep track the relations between all nested caches, and pass automatically all tags from an inner cache to its outer cache.


Replication problem
===================

When tag has been invalidated, a concurrent thread/process can recreate a dependent cache with outdated data from a slave, before the slave will be updated.

The best solution of this problem is a :ref:`locking the tag <tags-lock-en>` for cache creation until slave will be updated.
But, first, this implies a certain overhead, and secondly, all threads (including current one) continue to read outdated data from the slave (unless reading from the master is specified explicitly).

A compromise solution can be simple re-invalidation of the tag after period of time when the slave is guaranteed to be updated.

I saw also an approach of cache regeneration instead of removing/invalidation.
This approach entail ineffective memory usage (in case LRU_ principle).
Also, this approach does not resolve the problem of complexity of invalidation logic.
Usually, this approach is the cause of a lot of bugs.
For example, it requires to use a high quality ORM.
Some ORMs does not perform type conversion of instance attributes on save, therefore, the cache can be wrong (for example, there can be a string instead of a datetime instance).
I saw such case in my practice, the cache saved the string from the HTTP-client instead of the datatime instance. Although the data had been saved correctly, the model logic didn't performed type conversion until some another method had been called (semantic coupling).

.. update:: Nov 10, 2016

    Added description of implementation of tag locking.


.. _tags-lock-en:

Implementation of tag locking
=============================

The main purpose of tag locking is a preventing of substitution of actual data by outdated data by concurent threads/processes, if it's needed by transaction isolation level or a delay of replication.

The tag locking is implemented by library as preventing the dependent cache creation by concurent threads/processes while the tag is locked.

Why was not implemented a `Pessimistic Offline Lock`_ or `Mutual Exclusion`_?
This is a :ref:`resonable <thundering-herd-en>` question, because the cached logic can be too resource intensive.
This implementation requires concurent threads/processes are waiting untile the locked tag will be released.


Constructive obstacle to implementing pessimistic locking
---------------------------------------------------------

The main purpose of the library is cache invalidation.

Suppose, the process P1 has begun transaction with isolation level of "Repeatable read".

Then the process P2 has begun the transaction, updated data in the DB, invalidated tag T1, and ascuired the lock for the tag T1 until the transaction will be committed.

Process P1 are trying to read the cache with key C1, which is tagged by the tag T1, and is not valid anymore.
Not being able to read the invalid cache C1, the process P1 receives the outdated data from the DB (remember, the transaction isolation level is "Repeatable read").
Then the process P1 are trying to create the cache C1, and waiting while the tag T1 will be released.

When the transaction of process P2 is committed, the process P2 releases the tag T1.
Then the process P1 writes the outdated data into the cache C1.
This locking does not make sense.

But what will be happened, if we check the status of tag T1 on the cache reading (not writing)?
Can this approach to change something?

Yes, it can.
First, it adds an overhead to reading logic.
The second, it can has an effect if transaction isolation level is not higher than "Read committed".
For the transaction isolation level "Repeatable read" (which is default for some DB, and at least required for the correct work of pattern `Identity Map`_) and higher, it does not has any effect.
In this case, the process P2 would be locked before the transaction beginning.

Thus, this solution would be partial, not universal, and would contain an uncontrolled dependence.
For 2 from 4 of transaction isolation level it would not work.


Accompanying obstacle to implementing pessimistic locking
---------------------------------------------------------

Except the constructive obstacle to implementing pessimistic locking, there is also some other obstacles.

The library is focused mainly on web applications.
Waiting for parallel process until the end of the transaction, or until the slave is updated, which in some cases can take 8 seconds or more, is practically not feasible in web applications.

There is the 3 main reasons:

- The quickness of response is important for web-application, otherwise a client simply can not wait for the response.
- There is no any reason to wait for lock release longer than it takes time to create the cache itself.
- An increase in the number of pending processes can lead to a memory overflow, or reaching of available workers of the server, or reaching of the maximum allowed number of connections to the database or other resources.

Also, there would be a problem with the implementation, since it is impossible to correctly block all tags by single query.

- First, we have to use method ``cache.add()`` instead of ``cache.set_many()`` for locking, to ensure the atomicity of the existence check and cache creation.
- Second, each tag should be locked by separate query, that increases the overhead.
- Third, the locking by single query per tag can lead to Deadlock_, the probability of which can be significantly reduced by topological sorting.

We should also mention the possibility of `row-level locking by DB <https://www.postgresql.org/docs/9.5/static/explicit-locking.html>`__ using `SELECT FOR UPDATE <https://www.postgresql.org/docs/9.5/static/sql-select.html#SQL-FOR-UPDATE-SHARE>`_. But it works only when both transactions use `SELECT FOR UPDATE`_, otherwise `it does not work <https://www.postgresql.org/docs/9.5/static/transaction-iso.html#XACT-READ-COMMITTED>`__:

    When a transaction uses this isolation level, a SELECT query (without a FOR UPDATE/SHARE clause) sees only data committed before the query began; it never sees either uncommitted data or changes committed during query execution by concurrent transactions. In effect, a SELECT query sees a snapshot of the database as of the instant the query begins to run.

But no one uses cache of select for update (it doesn't make sense to do it, and usually select for update is not used by web-applications because business transaction is used instead). Also, this approach is not able to solve the problem of replication.


.. _thundering-herd-en:

Thundering herd
===============

But what we can to do if cached logic is really resource intensive?

Dogpile is also known as `Thundering Herd`_ effect or cache stampede.

The answer is simple - Pessimistic Lock. But we have to lock not tags, but the key of the cache (or group of related keys, see `Coarse-Grained Lock`_, especially when using aggregate queries).
It's because of when the cache key is released, the cache must be guaranteed to be created (but tags has many-to-many relation to caches).

The lock must cover the entire code fragment from reading the cache to creating it.
And this responsibility is not related to invalidation.

There is a lot of libraries which solve the issue, for example:

- `wheezy.caching.patterns.OnePass <https://bitbucket.org/akorn/wheezy.caching/src/586b4debff62f885d97e646f0aa2e5d22d088bcf/src/wheezy/caching/patterns.py?at=default&fileviewer=file-view-default#patterns.py-348>`_
- `memcached_lock <https://pypi.python.org/pypi/memcached_lock>`_
- `memcachelock <https://pypi.python.org/pypi/memcachelock>`_
- `unimr.memcachedlock <https://pypi.python.org/pypi/unimr.memcachedlock>`_
- `DistributedLock <https://pypi.python.org/pypi/DistributedLock>`_

- `distributing-locking-python-and-redis <https://chris-lamb.co.uk/posts/distributing-locking-python-and-redis>`_
- `mpessas/python-redis-lock <https://github.com/mpessas/python-redis-lock/blob/master/redislock/lock.py>`_
- `pylock <https://pypi.python.org/pypi/pylock>`_
- `python-redis-lock <https://pypi.python.org/pypi/python-redis-lock>`_
- `redis-py <https://github.com/andymccurdy/redis-py/blob/master/redis/lock.py>`_
- `redlock <https://pypi.python.org/pypi/redlock>`_
- `retools <https://github.com/bbangert/retools/blob/master/retools/lock.py>`_
- `score.distlock <https://pypi.python.org/pypi/score.distlock>`_


Transaction problem
===================

When web-application has good traffic, it's possible the concurrent process recreates the cache with the outdated data since the tag has been invalidated but before the transaction is committed.
In contrast to replication problem, here is the manifestation of the problem strongly depends on the quality of the ORM, and the probability of problems is reduced when you use a pattern `Unit of Work`_.

Let to consider the problem for each `transaction isolation level <Isolation_>`_ separately.


Read uncommitted
----------------

This is a simple case without any problems. If replication is used, it's enough to repeat invalidation when the slave is guaranteed to be updated.


Read committed
--------------

There is a problem, especially when you are using the pattern `ActiveRecord`_.
The probability of the problem can be reduced by using the pattern `DataMapper`_ together with `Unit of Work`_, this reduces the interval of time between data saving and transaction commit. But the problem is still possible.

In contrast to the replication problem, it would be preferable to use tag locking here until the transaction will be committed, because the current process reads different data than concurrent processes.
It's impossible to say which process (the current process or concurrent one) will have created the cache, thus it would be desirable to avoid cache creation until transaction is committed.

But this transaction isolation level is not so serious, and most often used to increase the degree of parallelism, i.e. has the same purpose as replication.
In this case, the problem of the transaction isolation level "Read committed" is usually absorbed by the replication problem, because process usually reads data from a slave.

Therefore, the expensive lock can be replaced by a re-invalidation when transaction is committed, as tradeoff.


Repeatable read
---------------

This case is more interesting.
We can't avoid tag locking here because we have to know not only the list of cache's tags, but also the time of each transaction commit which has invalidated the tag.

Thus, we have to lock the tag from the moment of the invalidation, but, moreover, we are not able to create cache in transactions which has been begun earlier than the current transaction is committed.

The good news is that we can lock the tag until the slave will be updated, if we have to use tag locking in any case.


Serializable
------------

Because non-existent objects usually are not cached, we are able to limit the problem of this transaction isolation level by the level of `Repeatable read`_.


Multiple connections to Database
================================

When you use multiple databases, and its transactions are synchronous, or you use simple replication, then you can use by one instance of outer cache (wrapper) per one instance of inner cache (backend).
The transaction of the cache does not have to strictly follow to system transactions of the DB.
It is enough to fulfill its purpose - to prevent the substitution of the cached actual data by concurrent process until the actual data will be visible for the concurrent process.
Therefore, a single transaction of the cache can cover several system database transactions.

When you use multiple connections to the same database (it sounds a little strange, but theoretically it's possible, for example, when you don't have ability to share connection between several ORMs in the single application), or the system database transactions are not synchronous, then you can configure the outer cache (wrapper) in the way to have by one instance of outer cache (wrapper) per one connection to DB for each instance of inner cache (backend).


Non-cached fragment. Dynamic window in cache.
=============================================

There are two mutually complementary patterns based on diametrically opposite principles - `Decorator`_ и `Strategy`_.
The first one places variable logic around a code, 
In the first case, the variable logic is placed around the declared code, in the second case it is passed into it.
Usual cache is similar to the pattern `Decorator`_, when the dynamic logic is located around the cached logic.
But sometimes a little fragment of the logic should not to be cached inside the cache.
For example, it can be some data of user, permission checking etc.

This problem can be solved by using `Server Side Includes`_.

Another approach is using two-phase template rendering, for example `django-phased <https://pypi.python.org/pypi/django-phased>`_.
To be honest, this approach has a considerable resource consumption, and in some cases the achieved effect can be gone.
Probably, due to this reason the approach is not widely used.

The popular template engine Smarty written by PHP has the function `{nocache} <http://www.smarty.net/docs/en/language.function.nocache.tpl>`_.

But the more interesting approach would be to use python code inside the dynamic window to abstract from third-party technologies.


.. update:: Nov 06, 2016

    Added abstract dependency manager.


Abstract dependency manager
===========================

For a long time I did not like the fact that several classes with different responsibilities were aware about the logic of tags handling.

It would be good to encapsulate this logic into separate `class strategy <Strategy_>`_, for example, similar to `TagDependency of YII framework`_,
but this approach creates overhead as `extra query per each cache key to verify its tags <https://github.com/yiisoft/yii2/blob/32f4dc8997500f05ac3f62f0505c0170d7e58aed/framework/caching/Cache.php#L187>`_, that means depriving the method ``cache.get_many()`` of the sense - aggregation queries.
I think, the overhead should not be more than one extra query per action, even for case this action is aggregated like ``cache.get_many()``.

Also I had another method with tangled responsibilities to provide aggregation queries, that does not cause delight.

But I like the idea to extract an abstract dependency manager, and obtain ability to use not only tags for invalidation, but any another principle, even an composite principle.

The problem was solved by class `Deferred <https://bitbucket.org/emacsway/cache-dependencies/src/default/cache_dependencies/defer.py>`_.
It's not pure Deferred as we know it from asynchronous programming, otherwise I would like to use this `elegant and lightweight library <https://pypi.python.org/pypi/defer>`_, kindly provided by the guys from Canonical.

My case requires not only delay the query execution, but also aggregation queries when it possible, for example, by using of ``cache.get_many()``.

Probably, the name Queue or Aggregator would be better, but since from the interface point of view we just postpone the task execution without going into details of its implementation, I preferred to leave the name Deferred.

This approach allows me to extract the abstract dependency manager, and now the logic of invalidation by cache tagging is simple an implementation of the intarface as class strategy `TagsDependency <https://bitbucket.org/emacsway/cache-dependencies/src/default/cache_dependencies/dependencies.py>`_.

This opens prospects for the creation of other implementations of dependency management, for example, by observing a file changing, or SQL query, or some system events.


Gratitude
=========

Thanks a lot to `@akorn <https://bitbucket.org/akorn>`_ for the meaningful discussion of the problem of caching.

Эта статья на Русском языке :doc:`../ru/cache-dependencies`.


.. _cache-dependencies: https://bitbucket.org/emacsway/cache-dependencies

.. _Coupling: http://wiki.c2.com/?CouplingAndCohesion
.. _Cohesion: http://wiki.c2.com/?CouplingAndCohesion
.. _Deadlock: https://en.wikipedia.org/wiki/Deadlock
.. _Decorator: https://en.wikipedia.org/wiki/Decorator_pattern
.. _Isolation: https://en.wikipedia.org/wiki/Isolation_(database_systems)
.. _LRU: https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
.. _Mutual Exclusion: https://en.wikipedia.org/wiki/Mutual_exclusion
.. _Observer: https://en.wikipedia.org/wiki/Observer_pattern
.. _Server Side Includes: https://en.wikipedia.org/wiki/Server_Side_Includes
.. _Strategy: https://en.wikipedia.org/wiki/Strategy_pattern
.. _Thundering Herd: http://en.wikipedia.org/wiki/Thundering_herd_problem

.. _ActiveRecord: http://www.martinfowler.com/eaaCatalog/activeRecord.html
.. _Coarse-Grained Lock: http://martinfowler.com/eaaCatalog/coarseGrainedLock.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _DataMapper: http://martinfowler.com/eaaCatalog/dataMapper.html
.. _Pessimistic Offline Lock: http://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html
