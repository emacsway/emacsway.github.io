
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

Наибольшим преимуществом полноценных `Моделей предметной области <Domain Model_>`__ в программе является возможность использования принципов Domain-Driven Design (DDD) [#fnddd]_.
Если Модели содержат исключительно бизнес-логику, и освобождены от служебной логики, то они могут легко читаться специалистами предметной области (т.е. представителем заказчика), что освобождает Вас от создания UML-диаграмм для обсуждений, и позволяет реализовывать модели максимально качественно.

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

    Нельзя разделять до бесконечности, у человеческого ума есть свои пределы, до которых он еще способен соединять разделенное;
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

Впоследствии модели вернули себе свои концептуальные контуры и читаемость кода, и вместе с тем сохранили механизм реакций при добавлении, изменении или удалении объектов.
Для достижения этого результата пришлось своими силами создать библиотеку реализующую паттерн Repository, так как существующих решений для реляционных данных с качественной кодовой базой я не смог найти.


Парадигма реактивного программирования
======================================

Сегодня модно увлекаться реактивным программированием.
Знаете ли Вы, что разработчики dojo впервые `применили реактивное программирование <https://github.com/dojo/dojo/commit/4bd91a5939d4dbc8a43d673cc279bb3d39ed0895#diff-48ec1f2998cbe6d644df0c9abd32d9d0R35>`__ в своей реализации паттерна Repository еще 13 сентября 2010?

Реактивное программирование дополняет (а не противопоставляет) паттерн `Repository`_, о чем красноречиво свидетельствует опыт `dojo.store`_, `Dstore`_ и нового `Dojo 2 - data stores <https://github.com/dojo/stores>`_.

Разработчики dojo - команда высококвалифицированных специалистов, их библиотеки используют такие серьезные компании как IBM.
Примером того, насколько серьезно и комплексно они подходят к решению проблем, может служить `история библиотеки RequireJS <http://requirejs.org/docs/history.html>`_.


Примеры реализаций
==================

Примеры реализации паттерна Repository в проекте `todomvc.com <http://todomvc.com/>`_:

- Angular2: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angular2/app/services/store.ts
- Angular1: https://github.com/tastejs/todomvc/blob/gh-pages/examples/angularjs/js/services/todoStorage.js
- React: https://github.com/tastejs/todomvc/blob/gh-pages/examples/react-alt/js/stores/todoStore.js

Другие реализации:

- `Dojo2 Stores <https://github.com/dojo/stores>`_ - \
  Excellent implementation of `Repository`_ pattern in paradigm of `Reactive Programming`_ for non-relational data.
- `Dstore <http://dstorejs.io/>`_ - \
  yet another excellent implementation of `Repository`_ pattern.
- `Dojo1 Store <https://dojotoolkit.org/reference-guide/1.10/dojo/store.html>`_ - \
  Dojo1 implementation of `Repository`_ pattern.
- `JS-Data <http://www.js-data.io/>`_ - \
  ORM written by JavaScript for relational data. Does not support composite relations.
- `9 JavaScript Libraries for Working with Local Storage <https://www.sitepoint.com/9-javascript-libraries-working-with-local-storage/>`_ - \
  article with interesting comments.
- `Kinvey Data Store <http://devcenter.kinvey.com/angular/guides/datastore>`_ - \
  implementation of `Repository`_ pattern by MBaaS Kinvey, `source code <https://github.com/Kinvey/js-sdk/tree/master/src/datastore/src>`__


Реляционные связи
=================

На заре появления ORM, мапперы делали таким образом, чтобы они выбирали одним запросом все связанные объекты (`пример реализации <https://bitbucket.org/emacsway/openorm/src/default/python/>`_).

Domain-Driven Design подходит к связям более строго, и рассматривает связи с позиции концептуальных контуров агрегата вложенных объектов [#fnddd]_.
Здесь также особую роль играет направление связей, и соблюдение принципа минимальной достаточности.

С появлением ORM в синхронном программировании активно начали применяться ленивые вычисления для разрешения связей.
В Python для этого активно используются `Descriptors <https://docs.python.org/3/howto/descriptor.html>`__, а в Java - AOP и Cross-Cutting Concerns [#fnccode]_.

Ключевым моментом является освобождение Domain Model от логики доступа к источнику данных.
Это необходимо как из принципах чистоты архитектуры и проектных решений, чтобы снизить сопряжение (`Coupling`_), так из из принципов простоты тестирования.
Наибольших успехов здесь достих принцип Cross-Cutting Concerns, который полностью освобождает модель от служебной логики.

Организация связей стала настолько легкой, что о ней перестали думать.
Там где требуются однонаправленные связи, разработчики с легкостью применяют двунаправленные связи.
Появлились механизмы оптимизации связей, которые неявно предзагружают все связанные объекты, что значительно сокращает количество обращений в базу данных.

Существует также распространенная точка зрения, что объект не должен отвечать за свои связи, а исключительное право на доступ к объекту должно принадлежать только Repository.
Такой точки зрения придерживаются некоторые уважаемые мною друзья.

Рост популярности асинхронных приложений заставил пересмотреть устоявшиеся представления на реализацию связей.
Асинхронное обращение к каждой связи каждого объекта значительно усложняет ясность программного года, и препятствует оптимизации.

Это привело к росту популярности объекто-ориентированных баз данных в асинхронном программировании, которые позволяют сохранять агрегат целиком.
Все чаще REST-frameworks стали использоваться для передачи клиенту `агрегата вложенных объектов <http://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects>`_.
Необходимость обслуживания агрегатов активизировала интерес к функциональному программированию, особенно в сочетании с парадигмой реактивного программирования.

Однако, решение одной проблемы порождало другую проблему.

Функциональное программирование горадо сложнее структурировать логически, что приводит к появлению плохо читаемого кода, который выражает не "что" он делает, а "как" он это делает.
А между тем, неясность намерений и целей автора - это ключевая проблема при чтении чужого кода.

    Шестимесячное исследование, проведенное в IBM, показало, что программисты,
    отвечавшие за сопровождение программы, «чаще всего говорили, что
    труднее всего было понять цель автора кода» (Fjelstad and Hamlen, 1979).

    A six-month study
    conducted by IBM found that maintenance programmers "most
    often said that understanding the original programmer's intent was
    the most difficult problem" (Fjelstad and Hamlen 1979).
    («Code Complete» [#fncodec]_)

Как упоминалось в статье :doc:`../en/how-to-quickly-develop-high-quality-code`, в процессе конструирования кода разработчик 91% времени читает код, и только 9% времени он печатает символы на клавиатуре.
А это значит, что плохо читаемый код на 91% может затормозить темпы разработки.

Я не хочу навлекать тень на парадигму функционального программирования, я просто говорю что она более требовательна к уровню квалификации разработчика, требует соответствующих навыков, и имеет свою нишу, в которой ее преимущества очевидны.
Универсальных инструментов не существует, нельзя совместить микроскоп и молоток.

Также такой подход разрушает все выгоды использования Domain-Driven Design, и разделяет элементы, реализующие концептуальные объекты, которые оказываются физически разделенными, что приводит к появлению кода, который больше не выражает модель.

Все `это привело к появлению <https://groups.google.com/d/msg/reactjs/jbh50-GJxpg/82CHQKeaG54J>`__ в сообществе ReactJS таких библиотек как:

- `Normalizr <https://github.com/paularmstrong/normalizr>`_ - \
  Normalizes (decomposes) nested JSON according to a schema.
- `Denormalizr <https://github.com/gpbl/denormalizr>`_ - \
  Denormalize data normalized with normalizr.

Принцип физической предустановки связанных объектов `реализован и в js-data <http://www.js-data.io/v3.0/docs/relations#section-eagerly-loading-relations>`__.

В нашей библиотеки мы предусмотрели как возможность декомпозиции агрегатов вложенных объектов, так и их композиции из плоских данных.
Причем, агрегат всегда сохраняет актуальное состояние, и при добавлении объекта в Repository он автоматически появляется в соответствующем агрегате.
Библиотека реализует это поведение либо в парадигме реактивного программирования, либо в парадигме Событийно-ориентированного программирования (на выбор).


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnpoeaa] «`Patterns of Enterprise Application Architecture`_» by `Martin Fowler`_, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
.. [#fnddd] «Domain-Driven Design: Tackling Complexity in the Heart of Software» by Eric Evans
.. [#fngof] «Design Patterns Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, 1994
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts

.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Code Complete: http://www.informit.com/store/code-complete-9780735619678
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

.. _Coupling: http://wiki.c2.com/?CouplingAndCohesion
.. _Cohesion: http://wiki.c2.com/?CouplingAndCohesion
.. _Observer: https://en.wikipedia.org/wiki/Observer_pattern
.. _Reactive Programming: https://en.wikipedia.org/wiki/Reactive_programming
.. _dojo.store: https://dojotoolkit.org/reference-guide/1.10/dojo/store.html
.. _Dstore: http://dstorejs.io/
