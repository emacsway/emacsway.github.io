
Про Anemic Domain Model
=======================

.. post:: Jan 04, 2018
   :language: ru
   :tags: ORM, DataMapper, DB, SQL, Model, DDD, Repository
   :category:
   :author: Ivan Zakrevsky


Время от времени в кругу моих знакомых регулярно поднимается вопрос о том, что Anemic Domain Model - никакой вовсе и не антипаттерн, и в качестве аргументов приводятся ссылки на статью "The Anaemic Domain Model is no Anti-Pattern, it’s a SOLID design" [#fnadminapen]_.
После очередного упоминания этой статьи я решил об этом написать.

Я не знаю, читал ли автор той статьи весь список перечисленной внизу нее литературы, потому что в этом списке присутствует книга "Martin, Robert C. Agile software development: principles, patterns, and practices. Prentice Hall PTR, 2003".

А эта книга дает, на мой взгляд, лучшее представление о том, что делают методы объекта: `они Внедряют Зависимости (Dependency Injection) <https://youtu.be/TMuno5RZNeE?t=33m30s>`__, что делает полиморфизм возможным!
Я всем советую сперва прочесть эту книгу (именно книгу в оригинале, а не краткие выдержки из Википедии), прежде чем читать указанную статью.
Как минимум, просмотрите хотя бы этот видеоролик: "`Bob Martin SOLID Principles of Object Oriented and Agile Design <https://www.youtube.com/watch?v=TMuno5RZNeE>`__".

Я не думаю, что исключение внедрения зависимостей (Dependency Injection) на уровне объекта будет соответствовать пятому принципу "D" в SOLID, а лишение объекта полиморфизма (да еще и в условиях отсутствия `Множественной Диспетчеризации <https://en.wikipedia.org/wiki/Multiple_dispatch>`__) будет соответствовать третьему принципу "L" в SOLID.
В таком случае внедрять зависимости и обеспечивать полиморфизм придется вручную, фактически превращая программу из объектно-ориентированной в процедурную.

Нужно заметить, что на этом месте многие начинают говорить о превосходствах функционального программирования, не понимая отличий межу функциональным программированием и процедурным.
Если говорить о превосходствах функционального программирования, то Роберт Мартин уже все сказал в статье "`OO vs FP <http://blog.cleancoder.com/uncle-bob/2014/11/24/FPvsOO.html>`__".

Нужно отличать Anemic Domain Model в объектно-ориентированной парадигме от Date Type в функциональной парадигме.
Вот `здесь <https://youtu.be/dnUFEg68ESM?t=3085>`_, например, сам Eric Evans говорит о том, что в своей книге "Domain-Driven Design" он не рассматривал глубоко функциональную парадигму, потому что в 2003 она не имела такого применения как сегодня.
А сегодня, в контексте Event Sourcing, она имеет уже совсем другое значение.

    You know, functional is a big thing.
    Maybe more than one thing.
    And so there are people though who have been talking about modeling in the functional realm and very interesting things.
    The things is models are just systems of abstraction.
    And so you have a powerful mechanism for abstraction.
    You should be able to implement, you should be able to express models.
    Furthermore, if you want to, you know, bring that ubiquitous language to life in the code, well, some of the functional languages, I think, are really nice for making making language in the code.
    And it might be a good mate with Event Sourcing.
    I'm just sort of laying out like I'm pointing out that we have so many options.
    Options that were really not there in 2003.

    \- Eric Evans, "`Tackling Complexity in the Heart of Software <https://youtu.be/dnUFEg68ESM?t=3085>`__", Domain-Driven Design Europe 2016 - Brussels, January 26-29, 2016

`Здесь <https://www.infoq.com/interviews/Technology-Influences-DDD/>`__ он возвращается к этому вопросу.
А `здесь <https://vimeo.com/131636650>`__ Greg Young рассматривает переход от OOP к Functional Programming в Event Sourcing.

Под Anemic Domain Model же понимается вырождение поведения модели именно в объектно-ориентированной парадигме, т.е. использование объектно-ориентированных языков в процедурном стиле.

Также следует отличать Anemic Domain Model от `ViewModel <https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice#layers-in-ddd-microservices>`__, ибо ViewModel по определению не предназначено для какого-либо поведения (а именно неверное расположение поведения является сутью антипаттерна Anemic Domain Model), и часто `применяется в CQRS <https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/cqrs-microservice-reads>`__.

Но вернемся к обсуждаемой статье.
Я так и не смог найти имя автора той статьи на том сайте.
Нечего и говорить, что это - весомый аргумент для авторитета статьи, которая с легкостью берется опровергать статью Мартина Фаулера(!) "`Anemic Domain Model <https://www.martinfowler.com/bliki/AnemicDomainModel.html>`__".
Создается впечатление, что подобные статьи - просто способ привлечь внимание к ресурсу, используя общественную резонансность скандальных утверждений.

Автор демонстрирует отсутствие четкого понимания различий между:

#. Логикой уровня приложения
#. Бизнес-логикой (причем, следует отличать предметно-ориентированную бизнес-логику от бизнес-логики, зависящей от приложения)
#. Обязанностью доступа к данным (что не является бизнес-логикой), иногда именуемой слоем данных

Указанная статья целиком построена на ошибках проектирования.
В своем примере он рассматривает вместо бизнес-логики - обязанность доступа к данным (да еще и в виде Active Record(!)).
Жаль, что в его списке литературы нет книги "Clean Code" by Robert C. Martin, в которой рассказывается, как для разделения служебной логики и бизнес-логики вот уже более 10 лет используется :ref:`Cross-Cutting Concerns <domain-model-relationship-implementing-aop-ru>`.

Уникальная способность автора всунуть в доменную модель обязанности слоя доступа к данным, - это, действительно, достаточно весомый аргумент для того, чтобы автор не наделял доменную модель вообще никакими обязанностями.
К тому же Service Layer относится к Application Logic, т.е. имеет политику более низкого уровня, нежели Domain Logic.
А :ref:`у Domain Service есть ограниченный список причин для своего существования <domain-service-ru>`.

Для того чтобы завуалировать неразбериху, автор вводит лишнее понятие Rich Domain Model, вводя тем самым читателя в заблуждение относительно присутствия некой дифференцированности в реализации Domain Model.
Нет никаких Rich Domain Model.
Есть Domain Model (объект моделирующий поведение объекта реального мира (предметной области)), а есть Anemic Domain Model (т.е. структура данных, выраженная объектами без поведения).

В целом, основной мотив сторонников Anemic Domain Model сводится к тому, что, поскольку они не умеют обеспечить разделение реализаций служебной Логики Доступа к Данным и Бизнес-Логики Доменной Модели, т.е. отделить разного рода (Инфраструктурные) Сервисы от Доменной Модели, то, поэтому, они предлагают вынести всю Бизнес-Логику из Доменной Модели к служебной логике в Сервисы.
Ну... хорошо... а что это решает?
В Сервисах их разделять не нужно?
Это же все-таки политики разного уровня...
Получаются те же яйца, только в процедурном стиле.
От перестановки мест слагаемых проблема не решается.

Мне эта ситуация напомнила случай, когда Мартину Фаулеру сказали, что гибкое проектирование невозможно, потому что схему базы данных сложно изменить, а значит, ее нужно проектировать заблаговременно.
Мартин Фаулер `ответил <https://youtu.be/VjKYO6DP3fo?t=16m11s>`__, что если схему базы сложно изменить, значит мы должны подумать о том, как можно сделать процесс миграций проще.
Так появился механизм миграций базы данных, и гибкое проектирование Agile стало возможным.
Т.е. возник вопрос - реакционно застрять на месте, потому что возникло препятствие, или же найти решение, устраняющее это препятствие, и продолжить движение вперед.

Все что не относится к логике предметной области, - это новая обязанность, которая должна быть вынесена за пределы Domain Model, или, по крайней мере, не рассматриваться как бизнес-логика, если Domain Model реализована в виде паттерна Active Record (как в той статье).

Очень часто можно наблюдать разбухшие модели, которые выполняют очень много несвойственных ее предметной области обязанностей, в т.ч. и уровня приложения (управление транзакциями, проверка привилегий и т.п.).
Domain Model должна моделировать только поведение объекта предметной области (реального мира).
Если Domain Model имеет несколько десятков методов, которые не выражают поведение объекта реального мира, не имеют общего применения, а используются только одним клиентом, то мы должны их разместить либо непосредственно внутри клиента, либо в классе, который обслуживает клиента (для обслуживания клиентов уровня приложения существует Sevice Layer, для обслуживания клиентов уровня предметной области и выравнивания интерфейсов существует паттерн Wrapper).
Более подробно эта тема уже рассматривалась в статье ":doc:`service-layer`".

Еще одной частой причиной порождения Anemic Domain Model является недостаточное использование `Domain Event <https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation>`__, либо некорректная его реализация.

Domain Model может быть представлена в виде агрегата, т.е. композиции связанных объектов, что характерно для DDD и NoSQL.
Domain Model может иметь методы, изменяющие ее состояние или композицию, но она не должна заботиться о сохранении этой композиции в базе данных.
Предположим, Вы осознали что NoSQL-хранилище Вам подходит лучше, чем RDBMS, и решили заменить реализацию класса ответственного за сохранение объекта.
С точки зрения архитектуры, база данных - это IO-устройство, от которого приложение стремится быть независимым.
NoSQL хранилища построены вокруг идеи агрегата, что позволяет, в определенной мере, избавиться от реляционных связей и упростить шардинг.
Границами транзакции NoSQL-хранилища являются границы агрегата.
Если у Вас детали реализации сохранения агрегата скрыты за интерфейсом ответственного за это объекта (обычно это Repository + DataMapper), то такой рефакторинг не затронет реализацию самой Доменной Модели.
Если Вы вынуждены изменять реализацию Domain Model, то это значит, что Ваша программа не имеет независимости от IO-устройства, что нарушает Single Responsibility Principle (в виде Code Smell "Shotgun Surgery").

Иногда случается, что Бизнес-Логика Доменной Модели нуждается в доступе к экземпляру связанной Доменной Модели, или даже в доступе к корню другого Агрегата.
Недостаточное понимание способов разделения политики разных уровней (Бизнес-Логики и Логики Доступа к Данным) часто приводит к оправданию Anemic Domain Model.
Между тем, существует целый :ref:`ряд способов решения этой проблемы <domain-model-relationship-ru>`.

Эта тема уже затрагивалась в статьях:

- ":doc:`javascript-and-repository-pattern`"
- ":doc:`service-layer`"
- ":doc:`storm-orm`"

Ключевой признак плохой архитектуры - это ее зависимость от деталей реализации.
Если Вы принимаете проектные решения (а тем более - парадигму) в угоду реализации, то это говорит о проблемах проектирования.
Это - зависимость.
Архитектура должна указывать реализацию, а не подстраиваться под нее.

Да, бывают случаи, когда мы должны использовать структуры данных вместо объектов.
Хорошо эту тему раскрывает Robert C. Martin в главе "Chapter 6: Objects and Data Structures :: Data/Object Anti-Symmetry" книги "Clean Code: A Handbook of Agile Software Craftsmanship".
Но это не имеет никакого отношения к тому, что написал автор.

Автор просто пишет о том, как писать процедурные программы в Объектно-Ориентированных языках.

Попробуйте реализовать в таком стиле паттерн `Class Table Inheritance <https://martinfowler.com/eaaCatalog/classTableInheritance.html>`__ для коллекции полиморфных объектов с достаточно богатой бизнес-логикой, и вы поймете все недостатки Anemic Domain Model.
То же самое справедливо и к случаю использования паттерна `Special Case <https://martinfowler.com/eaaCatalog/specialCase.html>`__, известного также как метод рефакторинга `Introduce Null Object <https://www.refactoring.com/catalog/introduceNullObject.html>`__.
Смотрите также `Replace Conditional with Polymorphism <https://www.refactoring.com/catalog/replaceConditionalWithPolymorphism.html>`__, `Replace Type Code With Polymorphism <https://www.refactoring.com/catalog/replaceTypeCodeWithPolymorphism.html>`__ и `Replace Type Code with State/Strategy <https://www.refactoring.com/catalog/replaceTypeCodeWithStateStrategy.html>`__ (желательно смотреть информацию в книге, номер страницы указан на страницах онлайн-каталога по ссылкам).

Материалы по теме:

- "`What is domain logic? <https://enterprisecraftsmanship.com/posts/what-is-domain-logic/>`__" by Vladimir Khorikov
- "`Domain services vs Application services <https://enterprisecraftsmanship.com/posts/domain-vs-application-services/>`__" by Vladimir Khorikov
- "`Domain model isolation <https://enterprisecraftsmanship.com/posts/domain-model-isolation/>`__" by Vladimir Khorikov
- "`Email uniqueness as an aggregate invariant <https://enterprisecraftsmanship.com/posts/email-uniqueness-as-aggregate-invariant/>`__" by Vladimir Khorikov
- "`How to know if your Domain model is properly isolated? <https://enterprisecraftsmanship.com/posts/how-to-know-if-your-domain-model-is-properly-isolated/>`__" by Vladimir Khorikov
- "`Domain model purity vs. domain model completeness <https://enterprisecraftsmanship.com/posts/domain-model-purity-completeness/>`__" by Vladimir Khorikov
- "`Domain model purity and lazy loading <https://enterprisecraftsmanship.com/posts/domain-model-purity-lazy-loading/>`__" by Vladimir Khorikov
- "`Domain model purity and the current time <https://enterprisecraftsmanship.com/posts/domain-model-purity-current-time/>`__" by Vladimir Khorikov
- "`Immutable architecture <https://enterprisecraftsmanship.com/posts/immutable-architecture/>`__" by Vladimir Khorikov
- "`Link to an aggregate: reference or Id? <https://enterprisecraftsmanship.com/posts/link-to-an-aggregate-reference-or-id/>`__" by Vladimir Khorikov

- "`How to create fully encapsulated Domain Models <https://udidahan.com/2008/02/29/how-to-create-fully-encapsulated-domain-models/>`__" by Udi Dahan

Примеры преобразования Anemic Domain Model в Domain Model:

- `Refactoring from Anemic Domain Model Towards a Rich One <https://github.com/vkhorikov/AnemicDomainModel>`__ by Vladimir Khorikov
- `Refactoring from anemic to rich Domain Model example <https://github.com/kgrzybek/refactoring-from-anemic-to-rich-domain-model-example>`__ by Kamil Grzybek

.. В определенной мере, затрагиваемая тема относится и к этой презентации \https://www.destroyallsoftware.com/talks/boundaries .

.. rubric:: Footnotes

.. [#fnadminapen] "The Anaemic Domain Model is no Anti-Pattern, it’s a SOLID design" \https://blog.inf.ed.ac.uk/sapm/2014/02/04/the-anaemic-domain-model-is-no-anti-pattern-its-a-solid-design/ (перевод на русский "Анемичная модель предметной области — не анти-шаблон, а архитектура по принципам SOLID" \https://habrahabr.ru/post/346016/ )
.. [#fnpoeaa] "Patterns of Enterprise Application Architecture" by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford

.. update:: Nov 16, 2019
