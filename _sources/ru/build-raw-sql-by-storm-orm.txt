
Построение Raw-SQL cредствами Storm-ORM
=======================================

.. post:: Dec 08, 2015
   :language: ru
   :tags: ORM, Storm ORM, DataMapper, DB, SQL, Python
   :category:
   :author: Ivan Zakrevsky


Возникло у меня желание попробовать построить чистый, сырой запрос (Raw-SQL) с помощью `storm.expr`_ для одного самописного специфического маппера, сочетающего в себе паттерны `Single Table Inheritance`_ и `Entity Attribute Value`_.

Причем, параметризирование запроса должно выполняться именованными (а не позиционными) аргументами, без участия `Storm ORM`_.

И :download:`вот что <../_media/ru/build-raw-sql-by-storm-orm/storm_expr_raw_sql_example.py>` у меня получилось (конкретная реализация, структура и названия, естественно, изменены):

.. literalinclude:: ../_media/ru/build-raw-sql-by-storm-orm/storm_expr_raw_sql_example.py
   :language: python
   :linenos:

На выходе получается запрос вида:

.. literalinclude:: ../_media/ru/build-raw-sql-by-storm-orm/storm_expr_raw_sql_example.sql
   :language: mysql

.. _Entity Attribute Value: https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model
.. _Single Table Inheritance: http://martinfowler.com/eaaCatalog/singleTableInheritance.html
.. _Storm ORM: https://storm.canonical.com/
.. _storm.expr: http://bazaar.launchpad.net/~storm/storm/trunk/view/head:/storm/expr.py
