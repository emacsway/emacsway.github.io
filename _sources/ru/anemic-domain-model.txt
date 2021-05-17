
Про Anemic Domain Model
=======================

.. post:: Jan 04, 2018
   :language: ru
   :tags: ORM, DataMapper, DB, SQL, Model, DDD, Repository
   :category:
   :author: Ivan Zakrevsky


Время от времени в кругу моих знакомых регулярно поднимается вопрос о том, что Anemic Domain Model - никакой вовсе и не антипаттерн, и в качестве аргументов приводятся ссылки на статью "The Anaemic Domain Model is no Anti-Pattern, it’s a SOLID design" [#fnadminapen]_.
После очередного упоминания этой статьи я решил об этом написать.

Список перечисленной внизу статьи литературы содержит книгу Martin, Robert C. "Agile software development: principles, patterns, and practices." Prentice Hall PTR, 2003. Эта книга дает, на мой взгляд, лучшее представление о том, что делают методы объекта: `они Внедряют Зависимости (Dependency Injection) <https://youtu.be/TMuno5RZNeE?t=33m30s>`__, что делает возможным полиморфизм.

Я не думаю, что исключение внедрения зависимостей (Dependency Injection) на уровне объекта будет сильно способствовать пятому принципу "D" в SOLID (поскольку `DI является механизмом реализации DIP <https://sergeyteplyakov.blogspot.com/2014/11/di-vs-dip-vs-ioc.html>`__), а лишение объекта полиморфизма (особенно в условиях отсутствия `Множественной Диспетчеризации <https://en.wikipedia.org/wiki/Multiple_dispatch>`__) будет способствовать третьему принципу "L" в SOLID.
В таком случае внедрять зависимости и обеспечивать полиморфизм придется вручную, фактически превращая программу из объектно-ориентированной в процедурную.

    📝 The fact that the boundaries are not visible during the deployment of a monolith does not mean that they are not present and meaningful.
    Even when statically linked into a single executable, the ability to independently develop and marshal the various components for final assembly is immensely valuable.

    Such architectures almost always depend on some kind of **dynamic polymorphism to manage their internal dependencies**.
    **This is one of the reasons that object-oriented development has become such an important paradigm in recent decades.**
    Without OO, or an equivalent form of polymorphism, architects must fall back on the dangerous practice of using pointers to functions to achieve the appropriate decoupling.
    Most architects find prolific use of pointers to functions to be too risky, so they are forced to abandon any kind of component partitioning.

    \- "Clean Architecture: A Craftsman’s Guide to Software Structure and Design" by Robert C. Martin

Нужно заметить, что на этом месте многие начинают говорить о превосходствах функционального программирования, зачастую не проводя различий между функциональным программированием и процедурным.
Превосходства функционального программирования хорошо осветил Роберт Мартин в статьях "`OO vs FP <http://blog.cleancoder.com/uncle-bob/2014/11/24/FPvsOO.html>`__" (2014) и "`FP vs. OO <https://blog.cleancoder.com/uncle-bob/2018/04/13/FPvsOO.html>`__" (2018).

Все дело в том, что в функциональном программировании обеспечивается ссылочная прозрачность, т.е. накладывается ограничение на изменяемость данных.
А между тем, основной недостаток утраты инкапсуляции в Anaemic Domain Model заключается именно в утрате контроля за изменением состояния и обеспечением инвариантов.

    📝 "OO makes code understandable by encapsulating moving parts. FP makes code understandable by minimizing moving parts."
    -- `Michael Feathers <https://twitter.com/mfeathers/status/29581296216>`__

Обе парадигмы, и функциональная, и объектно-ориентированная, решают вопрос управления существенной сложностью (Essential Complexity) программы, но разными способами.

    📝 "Brooks argues that software development is made difficult because of two different classes of problems—the essential and the accidental. In referring to these two terms, Brooks draws on a philosophical tradition going back to Aristotle. In philosophy, the essential properties are the properties that a thing must have in order to be that thing. A car must have an engine, wheels, and doors to be a car. If it doesn't have any of those essential properties, it isn't really a car.

    Accidental properties are the properties a thing just happens to have, properties that don't really bear on whether the thing is what it is. A car could have a V8, a turbocharged 4-cylinder, or some other kind of engine and be a car regardless of that detail. A car could have two doors or four; it could have skinny wheels or mag wheels. All those details are accidental properties. You could also think of accidental properties as incidental, discretionary, optional, and happenstance.

    <...>

    As Dijkstra pointed out, modern software is inherently complex, and no matter how hard you try, you'll eventually bump into some level of complexity that's inherent in the real-world problem itself. This suggests a two-prong approach to managing complexity:

    - **Minimize the amount of essential complexity that anyone's brain has to deal with at any one time.**
    - Keep accidental complexity from needlessly proliferating."

    <...>

    Abstraction is the ability to engage with a concept while safely ignoring some of its details—handling different details at different levels. Any time you work with an aggregate, you're working with an abstraction. If you refer to an object as a "house" rather than a combination of glass, wood, and nails, you're making an abstraction. If you refer to a collection of houses as a "town," you're making another abstraction.

    <...>

    From a complexity point of view, the principal benefit of abstraction is that it allows you to ignore irrelevant details. Most real-world objects are already abstractions of some kind. As just mentioned, a house is an abstraction of windows, doors, siding, wiring, plumbing, insulation, and a particular way of organizing them. A door is in turn an abstraction of a particular arrangement of a rectangular piece of material with hinges and a doorknob. And the doorknob is an abstraction of a particular formation of brass, nickel, iron, or steel.

    <...>

    Encapsulation picks up where abstraction leaves off. Abstraction says, "You're allowed to look at an object at a high level of detail." Encapsulation says, "Furthermore, you aren't allowed to look at an object at any other level of detail."

    -- "Software Estimation: Demystifying the Black Art (Developer Best Practices)" by Steve McConnell

..

    📝 "Following Aristotle, I divide them [difficulties] into essence - the difficulties inherent in the nature of the software - and accidents - those difficulties that today attend its production but that are not inherent.

    <...>

    The complexity of software is in essential property, not an accidental one.
    Hence descriptions of a software entity that **abstract away its complexity often abstract away its essence**.
    Mathematics and the physical sciences made great strides for three centuries by constructing simplified models of complex phenomena, deriving properties from the models, and verifying those properties experimentally.
    This worked because the complexities ignored in the models were not the essential properties of the phenomena.
    It does not work when the complexities are the essence."

    -- "No Silver Bullet - Essence and Accident in Software Engineering" by Frederick P. Brooks, Jr.

Нужно отличать Anemic Domain Model в объектно-ориентированной парадигме от Data Type в функциональной парадигме.
Вот `здесь <https://youtu.be/dnUFEg68ESM?t=3085>`_, например, сам Eric Evans говорит о том, что в своей книге "Domain-Driven Design" он не рассматривал глубоко функциональную парадигму, потому что в 2003 она не имела такого применения как сегодня.
А сегодня, в контексте Event Sourcing, она имеет уже совсем другое значение.

    📝 You know, functional is a big thing.
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
Не уверен, что это как-то могло бы поднять авторитет статьи, которая с такой легкостью берется опровергать статью "`Anemic Domain Model <https://www.martinfowler.com/bliki/AnemicDomainModel.html>`__" by Martin Fowler.
Зато я нередко наблюдал подобный приём с целью привлечения внимания к ресурсу, используя общественную резонансность скандальных утверждений.

Я не наблюдаю в статье четкого понимания автором различий между:

#. Логикой уровня приложения
#. Бизнес-логикой (причем, следует отличать предметно-ориентированную бизнес-логику от бизнес-логики, зависящей от приложения)
#. Обязанностью доступа к данным (что не является бизнес-логикой), иногда именуемой слоем данных

В примере статьи рассматривается вместо бизнес-логики - обязанность доступа к данным (да еще и в виде Active Record).
К сожалению, в списке литературы статьи нет другой книги Robert C. Martin - "Clean Code", в которой рассказывается, как для разделения служебной логики и бизнес-логики вот уже более 10 лет используется :ref:`Cross-Cutting Concerns <domain-model-relationship-implementing-aop-ru>`.

Выглядит так, что единственный мотив не наделять доменную модель вообще никакими обязанностями - это способность автора всунуть в доменную модель обязанности слоя доступа к данным.
К тому же Service Layer относится к Application Logic, т.е. имеет политику более низкого уровня, нежели Domain Logic.
А :ref:`у Domain Service есть ограниченный список причин для своего существования <domain-service-ru>`.

В статье приводится неверная трактовка Single Responsibility Principle (SRP), которая подразумевает "делать одну вещь".

В своей книге Clean Architecture, Robert C. Martin именно по этой причине сожалеет, что выбрал такое название (SRP):

    📝 "Of all the SOLID principles, the **Single Responsibility Principle (SRP) might be the least well understood**. That’s likely because it has a particularly **inappropriate name**.
    It is too easy for programmers **to hear the name and then assume that it means that every module should do just one thing**.

    Make no mistake, there is a principle like that. A function should do one, and only one, thing. We use that principle when we are refactoring large functions into smaller functions; we use it at the lowest levels. **But it is not one of the SOLID principles—it is not the SRP.**

    Historically, the SRP has been described this way:

    **A module should have one, and only one, reason to change.**

    Software systems are changed to satisfy users and stakeholders; those users and stakeholders are the “reason to change” that the principle is talking about. Indeed, we can rephrase the principle to say this:

    A module should be responsible to one, and only one, user or stakeholder.

    Unfortunately, the words “user” and “stakeholder” aren’t really the right words to use here. There will likely be more than one user or stakeholder who wants the system changed in the same way. Instead, we’re really referring to a group—one or more people who require that change. We’ll refer to that group as an actor.

    Thus the final version of the SRP is:

    A module should be responsible to one, and only one, actor.

    Now, what do we mean by the word “module”? The simplest definition is just a source file. Most of the time that definition works fine. Some languages and development environments, though, don’t use source files to contain their code. In those cases a module is just a cohesive set of functions and data structures.

    That word “cohesive” implies the SRP. Cohesion is the force that binds together the code responsible to a single actor.

    Perhaps the best way to understand this principle is by looking at the symptoms of violating it..."

    -- "Clean Architecture: A Craftsman’s Guide to Software Structure and Design" by Robert C. Martin

В книге "Agile Software Development. Principles, Patterns, and Practices." by Robert C. Martin, James W. Newkirk, Robert S. Koss, в оригинальной статье "`Principles Of OOD <http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod>`__" by Robert C. Martin, и в комментирующей статье "`The Single Responsibility Principle <http://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html>`__" by Robert C. Martin, SRP выводится из понятий `Coupling and Cohesion <https://wiki.c2.com/?CouplingAndCohesion>`__ of Constantine's Law.
В то время, как в обсуждаемой статье Cohesion совершенно не учитывается.

Вся эта неразбериха завуалирована введением избыточного понятия Rich Domain Model, что вводит читателя в заблуждение относительно присутствия некой дифференцированности в реализации Domain Model.
Никаких Rich Domain Model нет.
Есть Domain Model (объект моделирующий поведение объекта реального мира (предметной области)), а есть Anemic Domain Model (т.е. структура данных, выраженная объектами без поведения).

В целом, основной мотив сторонников Anemic Domain Model сводится к тому, что, они встречают сложность в разделении реализации служебной Логики Доступа к Данным и Бизнес-Логики Доменной Модели.
Поэтому, они предлагают вынести всю Бизнес-Логику из Доменной Модели к служебной логике в Сервисы.
Ну... хорошо... а в Сервисах не нужно разделять логику разного уровня политики?
Получаются те же яйца, только в процедурном стиле.
От перестановки мест слагаемых проблема не решается.

Единственное упрощение, которое можно достигнуть ценой утраты инкапсуляции доменной модели, - это отсутствие потребности в инверсии зависимостей, поскольку сервис уровня приложения, как сервис более низкого уровня политики, может быть осведомлен об интерфейса доменного сервиса, обладающего более высоким уровнем политики.
В то время, как доменная модель (в случае применения Lazy Loading) - не может.
Но инкапсуляция позволяет управлять Essential Complexity, что имеет гораздо более важное значение, чем Accidental Complexity.

Главный императив разработки ПО заключается в управлении сложностью.
Написание несопровождаемого Spaghetti-code не требует существенных умственных усилий.

    📝 "хочу сказать, что сделать простое иногда во много раз сложнее, чем сложное."

    -- М.Т. Калашников в интервью журналисту газеты «Metro Москва», 2009 год.

..

    📝 "Усложнять - просто, упрощать - сложно".

    -- "Закон Мейера"

Трудности нужно решать, а не замыкаться от них (см. `Психологическая Защита <https://ru.m.wikipedia.org/wiki/%D0%97%D0%B0%D1%89%D0%B8%D1%82%D0%BD%D1%8B%D0%B9_%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%B7%D0%BC>`__).

Мне это напоминает случай, когда Мартину Фаулеру сказали, что гибкое проектирование невозможно, потому что схему базы данных сложно изменить, а значит, ее нужно проектировать заблаговременно.
Мартин Фаулер `ответил <https://youtu.be/VjKYO6DP3fo?t=16m11s>`__, что если схему базы сложно изменить, значит мы должны подумать о том, как можно сделать процесс миграций проще.
Так появился механизм миграций базы данных, который сделал возможной Agile-разработку.

Все что не относится к логике предметной области, - это новая обязанность, которая должна быть вынесена за пределы Domain Model, или, по крайней мере, не рассматриваться как бизнес-логика, если Domain Model реализована в виде паттерна Active Record (как в той статье).

Очень часто можно наблюдать разбухшие модели, которые выполняют очень много несвойственных ее предметной области обязанностей, в т.ч. и уровня приложения (управление транзакциями, проверка привилегий и т.п.).
Domain Model должна моделировать только поведение объекта предметной области (реального мира).
Если Domain Model имеет несколько десятков методов, которые не выражают поведение объекта реального мира, не имеют общего применения, а используются только одним клиентом, то мы должны их разместить либо непосредственно внутри клиента, либо в классе, который обслуживает клиента (для обслуживания клиентов уровня приложения существует Sevice Layer, для обслуживания клиентов уровня предметной области и выравнивания интерфейсов существует паттерн Wrapper).
Более подробно эта тема уже рассматривалась в статье ":doc:`service-layer`".

Еще одной частой причиной порождения Anemic Domain Model является недостаточное использование `Domain Event <https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation>`__, либо некорректная его реализация.

Domain Model может быть представлена в виде агрегата, т.е. композиции связанных объектов, что характерно для DDD и NoSQL.
Domain Model может иметь методы, изменяющие ее состояние, но она не должна заботиться о его сохранении в базу данных.
Предположим, что по мере роста информированности в процессе разработки проекта, вы пришли к выводу, что NoSQL-хранилище подходит лучше, чем RDBMS, и решили заменить реализацию класса ответственного за сохранение объекта.
С точки зрения архитектуры, база данных - это IO-устройство, от которого приложение стремится быть независимым.
NoSQL хранилища построены вокруг идеи агрегата, что позволяет, в определенной мере, избавиться от реляционных связей и упростить масштабирование.
Границами транзакции NoSQL-хранилища являются границы агрегата.
Если детали реализации сохранения агрегата скрыты за интерфейсом ответственного за это объекта (обычно это Repository + DataMapper), то такой рефакторинг минимизирует изменение самой Доменной Модели.
В противном случае, программа не имеет независимости от IO-устройства, что нарушает Single Responsibility Principle (что проявляется в виде Code Smell "Shotgun Surgery").

Иногда случается, что Бизнес-Логика Доменной Модели нуждается в доступе к экземпляру связанной Доменной Модели, или даже в доступе к корню другого Агрегата.
Недостаточное понимание способов разделения политики разных уровней (Бизнес-Логики и Логики Доступа к Данным) часто приводит к оправданию Anemic Domain Model.
Между тем, существует целый :ref:`ряд способов решения этой проблемы <domain-model-relationship-ru>`.

Эта тема уже затрагивалась в статьях:

- ":doc:`javascript-and-repository-pattern`"
- ":doc:`service-layer`"
- ":doc:`storm-orm`"

Существует превосходная статья по этому вопросу:

- "`Domain model purity and lazy loading <https://enterprisecraftsmanship.com/posts/domain-model-purity-lazy-loading/>`__" by Vladimir Khorikov

Ключевой признак плохой архитектуры - это ее зависимость от деталей реализации.
Архитектура должна определять реализацию, а не подстраиваться под нее.

Да, бывают случаи, когда целесообразней использовать структуры данных вместо объектов.
Хорошо эту тему раскрывает Robert C. Martin в главе "Chapter 6: Objects and Data Structures :: Data/Object Anti-Symmetry" книги "Clean Code: A Handbook of Agile Software Craftsmanship".
Мне попадалась ещё статья на эту тему: "`Что такое expression problem, или о дуализме функционального и объектно-ориентированного программирования <https://ru.hexlet.io/blog/posts/expression-problem>`__" / Дмитрий Дементий.
Но эта тема не имеет никакого отношения к предмету обсуждаемой статьи, которая посвящена тому, как писать процедурные программы в Объектно-Ориентированных языках.

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
- "`In Defense of Lazy Loading <https://enterprisecraftsmanship.com/posts/defense-lazy-loading>`__" by Vladimir Khorikov
- "`Domain model purity and the current time <https://enterprisecraftsmanship.com/posts/domain-model-purity-current-time/>`__" by Vladimir Khorikov
- "`Immutable architecture <https://enterprisecraftsmanship.com/posts/immutable-architecture/>`__" by Vladimir Khorikov
- "`Link to an aggregate: reference or Id? <https://enterprisecraftsmanship.com/posts/link-to-an-aggregate-reference-or-id/>`__" by Vladimir Khorikov

- "`How to create fully encapsulated Domain Models <https://udidahan.com/2008/02/29/how-to-create-fully-encapsulated-domain-models/>`__" by Udi Dahan

Примеры преобразования Anemic Domain Model в Domain Model:

- `Refactoring from Anemic Domain Model Towards a Rich One <https://github.com/vkhorikov/AnemicDomainModel>`__ by Vladimir Khorikov
- `Refactoring from anemic to rich Domain Model example <https://github.com/kgrzybek/refactoring-from-anemic-to-rich-domain-model-example>`__ by Kamil Grzybek

Видео:

- `Доклад Vladimir Khorikov про Anemic Domain Model <https://youtu.be/UlEmtTJUwtA?t=6075>`__

.. В определенной мере, затрагиваемая тема относится и к этой презентации \https://www.destroyallsoftware.com/talks/boundaries .

.. rubric:: Footnotes

.. [#fnadminapen] "The Anaemic Domain Model is no Anti-Pattern, it’s a SOLID design" \https://blog.inf.ed.ac.uk/sapm/2014/02/04/the-anaemic-domain-model-is-no-anti-pattern-its-a-solid-design/ (перевод на русский "Анемичная модель предметной области — не анти-шаблон, а архитектура по принципам SOLID" \https://habrahabr.ru/post/346016/ )
.. [#fnpoeaa] "Patterns of Enterprise Application Architecture" by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford

.. update:: May 17, 2021
