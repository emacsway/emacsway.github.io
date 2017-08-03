
Реализация паттерна Repository в браузерном JavaScript
======================================================

.. post:: 
   :language: ru
   :tags: Repository, ORM, JavaScript
   :category:
   :author: Ivan Zakrevsky

Хорошая архитектура освобождает Вас от привязки к конкретной реализации.
Она позволяет Вам отложить момент принятия решения о реализации, и `начать конструирование кода еще не имея этого решения <Service Stub_>`__.
Принципиально важным моментом является то, что Вы обретаете возможность принять решение в момент наибольшей информированности, а также всегда можете легко подменить конкретную реализацию на любую другую.
Вот эта обязанность возложена на паттерн `Repository`_.

.. contents:: Содержание

Таким образом, у Вас появляется полная абстракция от источника данных, будь то REST-API, MBaaS, SaaS, IndexedDB, HTML, сторонний сервис по протоколу JSON-RPC или `Service Stub`_.

    "Однако мы часто забываем, что принятие решений лучше всего откладывать до последнего момента.
    Дело не в лени или безответственности;
    просто это позволяет принять информированное решение с максимумом возможной информации. 
    Преждевременное решение принимается на базе неполной информации.
    Принимая решение слишком рано, мы лишаемся всего полезного, что происходит на более поздних стадиях:
    обратной связи от клиентов, возможности поразмышлять над текущим состоянием проекта и опыта применения решений из области реализации."

    "We often forget that it is also best to postpone decisions until the last possible moment.
    This isn’t lazy or irresponsible; it lets us make informed choices with the best possible information.
    A premature decision is a decision made with suboptimal knowledge. We will have that
    much less customer feedback, mental reflection on the project, and experience with our
    implementation choices if we decide too soon."
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_)

Кроме того, у Вас появляется возможность реализовать паттерны `Identity Map`_ и `Unit of Work`_.
Последний очень часто востребован, так как позволяет сохранить на сервере уже полностью завершенный агрегат вложенных объектов, либо выполнить откат состояния локальных объектов в случае, если сохранить данные невозможно (пользователь передумал или ввел невалидные данные).


Модель предметной области (Domain Model)
========================================

Наибольшим преимуществом полноценных `Моделей предметной области <Domain Model_>`__ в программе является возможность использования Domain-Driven Design (DDD) [#fnddd]_.
Если Модели содержат исключительно бизнес-логику, и освобождены от служебной логики, то они могут легко читаться специалистами предметной области (т.е. представителем заказчика), что освобождает Вас от создания UML-диаграмм для обсуждений.

В одном из проектов я пытался реализовать достаточно сложную доменную логику (которая содержала около 20 доменных Моделей) в парадигме реактивного программирования, когда атрибуты экземпляра Модели изменяли свое значение путем реакции на изменения других моделей.
Суть в том, что вся эта реактивная логика уже не принадлежала самой доменной модели, и располагалась в разного рода `слушателях <Observer_>`_ и обработчиках.

    "Весь смысл объектов в том, что они позволяют хранить данные вместе с процедурами их обработки.
    Классический пример дурного запаха – метод, который больше интересуется не тем классом, в котором он находится, а каким то другим.
    Чаще всего предметом зависти являются данные."

    "The whole point of objects is that they are a technique to package data with the processes used
    on that data. A classic smell is a method that seems more interested in a class other than the one
    it actually is in. The most common focus of the envy is the data."
    («Refactoring: Improving the Design of Existing Code» [#fnrefactoring]_)   

..

    "Если требования архитектурной среды к распределению обязанностей таковы, что элементы, реализующие концептуальные объекты, оказываются физически разделенными, то код больше не выражает модель.

    Нельзя разделять до бесконечности, у человеческого ума есть свои пределы, до которых он еще способен соединять пазделенное;
    если среда выходит ха это пределы, разработчики предметной области теряют способность расчленять модель на осмысленные фрагменты."

    "If the framework's partitioning conventions pull apart the elements implementing the
    conceptual objects, the code no longer reveals the model.

    There is only so much partitioning a mind can stitch back together, and if the framework uses 
    it all up, the domain developers lose their ability to chunk the model into meaningful pieces."
    («Domain-Driven Design: Tackling Complexity in the Heart of Software» [#fnddd]_)

Это привело к такому огромному количеству хитросплетений слушателей, что превосходство в performance было утрачено, но еще раньше была утрачена читаемость кода.
Даже я не мог на следующий день сказать что делает тот или иной фрагмент кода, не говоря уже о специалисте предметной области.
Мало того, что это в корне разрушало DDD, так это еще и в значительной мере :doc:`снижало скорость разработки новых функций проекта <../en/how-to-quickly-develop-high-quality-code>`.

Надежды на такой подход окончательно рухнули когда выяснилось, что каждый экземпляр модели должен изменять значения своих атрибутов в зависимости от контекста использования (выбранной группировки отображения или критериев фильтрации).

Впоследствии модели вернули себе свои концептуальные контуры и читаемость кода, и вместе с тем сохранился механизм реакций при добавлении, изменении или удалении объектов.
Для достижения этого результата пришлось своими силами создать библиотеку реализующую паттерн Repository, так как существующих решений для реляционных данных с качественной кодовой базой я не смог найти.


Парадигма реактивного программирования
======================================

Сегодня модно увлекаться реактивным программированием.
Знаете ли Вы, что разработчики dojo впервые `применили реактивное программирование <https://github.com/dojo/dojo/commit/4bd91a5939d4dbc8a43d673cc279bb3d39ed0895#diff-48ec1f2998cbe6d644df0c9abd32d9d0R35>`__ в своей реализации паттерна Repository еще 13 сентября 2010?

Реактивное программирование дополняет (а не противопоставляет) паттерн `Repository`_, о чем красноречиво свидетельствует опыт `dojo.store`_ и `Dstore`_.

Разработчики dojo - команда выскококвалифицированных специалистов, их библиотеки используют такие серьезные компании как IBM.
Примером того, насколько серьезно и комплексно они подходят к решению проблем, может служить `история библиотеки RequireJS <http://requirejs.org/docs/history.html>`_.


Примеры реализаций
==================

Примеры реализации паттерна Repository в проекте `todomvc.com <http://todomvc.com/>`_:

- Angular2: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angular2/app/services/store.ts
- Angular1: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angularjs/js/services/todoStorage.js


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fnpoeaa] «`Patterns of Enterprise Application Architecture`_» by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans
.. [#fngof] «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts

.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Robert C. Martin: http://informit.com/martinseries
.. _Patterns of Enterprise Application Architecture: https://www.martinfowler.com/books/eaa.html
.. _Refactoring\: Improving the Design of Existing Code: https://martinfowler.com/books/refactoring.html
.. _Martin Fowler: https://martinfowler.com/aboutMe.html

.. _Domain Model: http://martinfowler.com/eaaCatalog/domainModel.html
.. _Identity Map: http://martinfowler.com/eaaCatalog/identityMap.html
.. _Query Object: http://martinfowler.com/eaaCatalog/queryObject.html
.. _Repository: http://martinfowler.com/eaaCatalog/repository.html
.. _Service Stub: http://martinfowler.com/eaaCatalog/serviceStub.html
.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html

.. _Observer: https://en.wikipedia.org/wiki/Observer_pattern
.. _dojo.store: https://dojotoolkit.org/reference-guide/1.10/dojo/store.html
.. _Dstore: http://dstorejs.io/
