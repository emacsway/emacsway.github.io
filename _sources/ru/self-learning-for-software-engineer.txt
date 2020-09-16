
Список литературы для самообучения разработчика программного обеспечения
========================================================================

.. post:: Oct 11, 2019
   :language: ru
   :tags:
   :category:  Architecture, DDD, Clean Architecture, Clean Code, Event-Driven, Microservices, CQRS, Event Sourcing, Extreme Programming, TDD, XP, Refactoring, programming
   :author: Ivan Zakrevsky
   :redirect: en/eda-reference-applications

Один из частых вопросов, который я наблюдаю регулярно, - это "посоветуйте список литературы в области разработки программного обеспечения".
В этом посте я изложу свое видение самообучения и приведу список тематической литературы, с учетом моего личного опыта.

.. contents:: Содержание


Предисловие
===========

Классическая ошибка новичков - жажда к знаниям, нетерпеливость.
Обычно это приводит к тому, что, в погоне за количеством, они надрываются (объем знаний, который предстоит освоить, действительно, огромный), осознают невыполнимость желаемого, впадают в депрессию, а затем и в состояние `психологической защиты <https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D1%89%D0%B8%D1%82%D0%BD%D1%8B%D0%B9_%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%B7%D0%BC>`__ (мол, "академичность" неуместна на практике), и прекращают развиваться.
Решается эта проблема очень просто - жажда должна быть не к знаниям, а к дисциплине.
А уж дисциплина обязательно приведет к обретению знаний.
Дисциплина - это, своего рода, производная знаний.
Она поддерживает постоянную скорость на пути освоения знаний.
Сперва нужно выработать привычку, а затем привычка будет работать на вас.
Как говорится, сохраняйте порядок, и порядок сохранит вас.

Достаточно читать по 5 страниц в день.
Тут главное - стабильность.
Пусть будет по чуть-чуть, но постоянно.
Дисциплина - мать победы, говорил А.В. Суворов.
Гнаться за количеством не нужно.

    "A little reading goes a long way toward professional advancement. If you read even one
    good programming book every two months, roughly 35 pages a week, you'll soon have
    a firm grasp on the industry and distinguish yourself from nearly everyone around you."

    \- "Code Complete" by Steve McConnell

..

    "We become authorities and experts in the practical and scientific spheres
    by so many separate acts and hours of work.
    If a person keeps faithfully busy each hour of the working day,
    he can count on waking up some morning to find himself one of the competent
    ones of his generation."

    \- William James, cited by Steve McConnell in "Code Complete"

И, желательно, чтобы читаемая книга совпадала с тематикой текущего проекта, чтобы через практику хорошо легла в память.
Я по этой причине часто изменял свой график чтения.
Обычно я читал в параллели 2-3 книги. Одну - планово, другие - по потребностям проекта.

Еще одной ошибкой является неудачный выбор литературы.
Сегодня штампуется много литературы, но далеко не каждая книга достойна внимания.
`Закон Парето <https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%BA%D0%BE%D0%BD_%D0%9F%D0%B0%D1%80%D0%B5%D1%82%D0%BE>`__ работает и здесь.

Хорошей вещью для систематизации собственных знаний является написание статей и участие в профессиональных дискуссиях.
Ничто так не систематизирует собственные знания, как попытка объяснить что-то другому человеку.
Вы, конечно, будете периодически ошибаться, но для кристализации знаний это лучше, чем ничего не делать.
К тому же, это хорошо развивает сдержанность в аргументации, что немаловажно.

На первых порах критически важно участвовать в Open Source проектах.
Можно завести свои собственные Open Source проекты.
Можно принимать участие в каких-то существующих проектах с авторитетными комьюнити, которые будут помогать избавляться от ошибок.
В любом случае, не надейтесь на то, что профессиональные проекты предоставят вам достаточную практику для закрепления знаний.
А Open Source проекты - очень даже предоставят.
Я даже считаю, что практика должна предшествовать теории, потому что трудно запомнить какое-то решение, если вам на практике не знакома решаемая проблема.
Потребность в теории должна назреть.
Когда я приступал к теории, то у меня был накоплен уже солидный багаж проблем, решение которых я искал.
Когда я впервые прочитал о мотивации паттерна Bridge, у меня в голове промелькнуло: "так вот, оказывается, как решается та самая проблема".
Когда я читал каталог Code Smells, я частенько вспоминал свой код.
В результате, решения навечно запечатлелись в памяти.

Очень правильно `сказал <https://sergeyteplyakov.blogspot.com/2017/02/reading-books-considered-harmful.html>`__ Сергей Тепляков: "Полноценное обучение – это не теория vs. практика. Это комбинация этих вещей, при этом процент одного и другого зависит от человека и изучаемой темы."

Ну и, главное, не впадать в фанатизм.
Засасывает.
Нужно себя уравновешивать другими интересами, семья, спорт, физкультура, шашлыки, друзья, путешествия...
Непредвзятый и свободный взгляд намного важнее изобилия знаний.
Путешествие должно быть на легке, как говорил Кент Бек.
По сути, знания нужны только для того, чтобы избавиться от всего лишнего.
Архитектура - это, на самом деле, наука об ограничениях (т.е. о том, как не надо делать).

Кандидатский минимум
====================

Учимся обучению
---------------

Это может показаться немного удивительным, но первая книга будет посвящена не техническим знаниям, а вопросам самоорганизации, управления временем, психологии, методикам работы под стрессом, оцеванию задач по разработке программного обеспечения, вопросам коммуникации и поведению в конфликтных ситуациях, и, самое главное, - науке быть правдивым.
Именно правдивость является важнейшим отличительным признаком настоящего профессионала.
И это не так просто, как может показаться на первый взгляд.
Есть разница между кодером и профессионалом.
И эта книга о том, как стать профессионалом.
Без знаний, изложенных в этой книге, вы просто не сможете изыскать время на самообучение, и список остальных книг вам может просто не понадобиться:

- "The Clean Coder" by Robert C. Martin


Изучаем основную используемую технологию
----------------------------------------

Следующая книга должна быть посвящена основной используемой технологии, т.е. синтаксическим возможностям языка программирования.
Для Python-разработчиков хорошим выбором была бы книга:

- "Learning Python" 5th edition by Mark Lutz

Для Golang интересно выглядят книги:

- "Hands-On Software Architecture with Golang. Design and architect highly scalable and robust applications using Go" by Jyotiswarup Raiturkar
- "The Go Programming Language" by Alan A.A. Donovan Google Inc., Brian W. Kernighan Princeton University

Для Erlang:

- "Programming Erlang: Software for a Concurrent World (Pragmatic Programmers)" 2nd edition by Joe Armstrong

Для frontend-разработчиков, работающих с Angular, имеет смысл обратить внимание на книгу:

- "ng-book2. The Complete Book on Angular 6" by Nate Murray, Felipe Coury, Ari Lerner, and Carlos Taborda


Азбука программирования
-----------------------

Подразумевается что вы уже хорошо знаете синтаксис основного языка программирования.
Но, знание букв еще не делает вас поэтом.
Следующие книги являются азбукой программирования.
Я привожу их в таком порядке, в каком я рекомендую их прочтение:

- "Design Patterns: Elements of Reusable Object-Oriented Software" by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides
- "Patterns of Enterprise Application Architecture" by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
- "Refactoring: Improving the Design of Existing Code" 1st edition by Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts
- "Clean Code: A Handbook of Agile Software Craftsmanship" by Robert C. Martin
- "Code Complete" 2nd edition by Steve McConnell
- "UML Distilled. A Brief Guide to the Standard Object Modeling Language" 3d edition by Martin Fowler
- "`KISS Principles <https://people.apache.org/~fhanik/kiss.html>`__"


Учимся быть эффективным
-----------------------

Знаний предыдущих пяти книг достаточно для того, чтобы вы стали работать в разы эффективней.
Но нужно не только знать, а еще и :doc:`уметь быть эффективным на практике <./tdd>`.
Никто не раскрывает этот вопрос лучше, чем Kent Beck:

- "Test-Driven Development By Example" by Kent Beck


Учимся делать команду эффективной
---------------------------------

Следующий барьер - умение сделать команду эффективной.
Вы не сможете быть эффективным в изоляции, поскольку ваша эффективность определяется качеством кодовой базы, а она разрабатывается всей командой.
Или вы сделаете команду эффективной, или ваша эффективность так и останется мечтательством.
Опять же, лучший наставник в этих вопросах - Kent Beck:

- "Extreme Programming Explained" 1st edition by Kent Beck

На данном этапе, этой книги достаточно.
Обратите внимание, я советую именно первое издание, так как оно лучше раскрывает смысл и назначение :doc:`Agile разработки <./easily-about-agile-way-to-rapid-development>`.


Изучаем операционную систему
----------------------------

Вот по операционным системам я мало что могу посоветовать, так как низкоуровневым программированием я практически не занимался.
Но вам обязательно нужно получить представление о том, как работают регистры процессора, память, и как управлять операционной системой.

Я в свое время читал эти книги (к сожалению, сегодня они устарели):

- "The Linux® Kernel Primer: A Top-Down Approach for x86 and PowerPC Architectures" by Claudia Salzberg Rodriguez, Gordon Fischer, Steven Smolski
- "Digital computers and microprocessors" by Aliyev / "Цифровая вычислительная техника и микропроцессоры" М.М.Алиев

А вот этот справочник у меня всегда под рукой:

- "Unix and Linux System Administration Handbook" 5th edition by Evi Nemeth, Garth Snyder, Trent R. Hein, Ben Whaley, Dan Mackin


Изучаем основы алгоритмов и структур данных
-------------------------------------------

Алгоритмы хоть и используются редко в прикладной разработке (если вы только не пишете поисковые системы, системные утилиты, языки программирования и операционные системы, системы маршрутизации, биржевые анализаторы и т.п.), но знать хотя бы базовые основы необходимо.
Существует книга, которая за двести с небольшим страниц может дать эти базовые основы в легкой и популярной форме:

- "Algorithms Unlocked" 3d edition by Thomas H. Cormen

Данная книга не акцентируется на математике, что, с одной стороны, облегчает освоение материала, но, с другой стороны, оставляет невосполненным важный аспект профессиональных знаний.
К счастью, существует книга, которая обеспечивает легкий вход в алгоритмы, включая их математический анализ:

- "Introduction to the Design and Analysis of Algorithms" 3d edition by A.Levitin

При чтении этой книги могут возникать вопросы справочного характера по математике, ответы на которые можно найти в приложении этой книги (Appendix A: Useful Formulas for the Analysis of Algorithms, Appendix B: Short Tutorial on Recurrence Relations), в математических справочниках (например, М.Я. Выгодского, А.А. Гусака) или в справочном разделе по математике "VIII Appendix: Mathematical Background" книги "Introduction to Algorithms" 3d edition by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein.


Изучаем математику
------------------

Существует монументальная книга, которую стоит упомянуть отдельно (обратите внимание на фамилии авторов, которые в представлении не нуждаются).
Чтобы не тормозить общий процесс обучения, ее лучше читать в параллельно-фоновом режиме.
К тому же математические знания следует всегда поддерживать в актуальном состоянии, и регулярно освежать их в голове в фоновом режиме.

- "Concrete Mathematics: A Foundation for Computer Science" 2nd edition by Ronald L. Graham, Donald E. Knuth, Oren Patashnik

Эта книга дает прекрасную математическую базу для функционального программирования.
И хорошо заходит в сочетании с "The Art Of Computer Programming" Volume 1 3d edition by Donald Knuth, поскольку у них многие темы пересекаются и раскрываются с разных точек зрения, что дает полноту понимания.
Справочник математических нотаций в конце книги нередко оказывается полезным.

Книги по математике и алгоритмам - сложные книги, и я хотел бы поделиться одним советом, который я услышал еще в студенчестве.
Если что-то непонятно - прочитай три раза:

1. Первый раз просто прочитай, оставив попытки что-то понять, - нужно просто получить обзорность материала.
2. Второй раз прочитай уже пытаясь слегка вникать.
3. И третий раз прочитай уже вникая полностью.


Учимся архитектуре
------------------

Теперь можно приступить и к архитектуре:

- "Clean Architecture: A Craftsman's Guide to Software Structure and Design" by Robert C. Martin


Изучаем распределенные системы
------------------------------

- "NoSQL Distilled. A Brief Guide to the Emerging World of Polyglot Persistence." by Pramod J. Sadalage, Martin Fowler
- "Building Microservices. Designing Fine-Grained Systems" by Sam Newman
- "`A plain english introduction to CAP Theorem <http://ksat.me/a-plain-english-introduction-to-cap-theorem>`__" (`Russian <https://habr.com/ru/post/130577/>`__) by Kaushik Sathupadi
- "`Map Reduce: A really simple introduction <http://ksat.me/map-reduce-a-really-simple-introduction-kloudo>`__" by Kaushik Sathupadi
- "`Eventually Consistent - Revisited <https://www.allthingsdistributed.com/2008/12/eventually_consistent.html>`__" by Werner Vogels


Изучаем распределенные системы. Углубляем навыки.
-------------------------------------------------

Книг по этой теме предстоит прочитать слишком много.
Вряд-ли ваша работа будет ждать, пока вы прочитаете их все.
К счастью, сообщество .NET разработчиков подготовило краткий справочник, который заменит вам прочтение десятка книг:

- "`.NET Microservices: Architecture for Containerized .NET Applications <https://docs.microsoft.com/en-us/dotnet/standard/microservices-architecture/index>`__" edition v2.2.1 (`mirror <https://aka.ms/microservicesebook>`__) by Cesar de la Torre, Bill Wagner, Mike Rousos

К этой книге существует эталонное приложение, которое наглядно демонстрирует практическое применение изложенной в книге информации:

- https://github.com/dotnet-architecture/eShopOnContainers (CQRS, DDD, Microservices)

И можно сюда включить еще и книгу:

- "`CQRS Journey <https://docs.microsoft.com/en-US/previous-versions/msp-n-p/jj554200(v=pandp.10)>`__" by Dominic Betts, Julián Domínguez, Grigori Melnik, Fernando Simonazzi, Mani Subramanian

К ней также существует демонстрационное приложение:

- https://github.com/microsoftarchive/cqrs-journey (Event Sourcing, SAGA transactions)


Изучаем DDD
-----------

Начинать я рекомендовал бы с прекрасного краткого руководства:

- "`What Is Domain-Driven Design? <https://www.oreilly.com/library/view/what-is-domain-driven/9781492057802/>`__" by Vladik Khononov

Затем приступить к классике:

- "Domain-Driven Design" by Eric Evans
- "`Implementing Domain-Driven Design <https://kalele.io/books/>`__" by Vaughn Vernon

Существуют краткие изложения этих двух книг по DDD.

Краткие изложения "Domain-Driven Design" by Eric Evans:

- "`Domain-Driven Design Reference <https://domainlanguage.com/ddd/reference/>`__" by Eric Evans
- "`Domain-Driven Design Quickly <https://www.infoq.com/books/domain-driven-design-quickly/>`__"

Краткое изложение "Implementing Domain-Driven Design" by Vaughn Vernon:

- "`Domain-Driven Design Distilled <https://kalele.io/books/>`__" by V.Vernon

Статьи на частые вопросы по DDD:

- "`What is domain logic? <https://enterprisecraftsmanship.com/posts/what-is-domain-logic/>`__" by Vladimir Khorikov
- "`Domain services vs Application services <https://enterprisecraftsmanship.com/posts/domain-vs-application-services/>`__" by Vladimir Khorikov
- "`Domain model isolation <https://enterprisecraftsmanship.com/posts/domain-model-isolation/>`__" by Vladimir Khorikov
- "`Email uniqueness as an aggregate invariant <https://enterprisecraftsmanship.com/posts/email-uniqueness-as-aggregate-invariant/>`__" by Vladimir Khorikov
- "`How to know if your Domain model is properly isolated? <https://enterprisecraftsmanship.com/posts/how-to-know-if-your-domain-model-is-properly-isolated/>`__" by Vladimir Khorikov
- "`Domain model purity vs. domain model completeness <https://enterprisecraftsmanship.com/posts/domain-model-purity-completeness/>`__" by Vladimir Khorikov
- "`Immutable architecture <https://enterprisecraftsmanship.com/posts/immutable-architecture/>`__" by Vladimir Khorikov
- "`Link to an aggregate: reference or Id? <https://enterprisecraftsmanship.com/posts/link-to-an-aggregate-reference-or-id/>`__" by Vladimir Khorikov

- "`Bounded Contexts are NOT Microservices <https://vladikk.com/2018/01/21/bounded-contexts-vs-microservices/>`__" by Vladik Khononov
- "`Tackling Complexity in Microservices <https://vladikk.com/2018/02/28/microservices/>`__" by Vladik Khononov
- "`DDDDD: Bounded Contexts, Microservices, and Everything In Between <https://youtu.be/Z0RgR9xIQE4>`__" by Vladik Khononov

- "`Overselling Event Sourcing <https://zimarev.com/blog/event-sourcing/myth-busting/2020-07-09-overselling-event-sourcing/>`__" by Alexey Zimarev
- "`Event Sourcing and Microservices <https://zimarev.com/blog/event-sourcing/microservices/>`__" by Alexey Zimarev
- "`Projections in Event Sourcing <https://zimarev.com/blog/event-sourcing/projections/>`__" by Alexey Zimarev
- "`Event Sourcing and CQRS <https://zimarev.com/blog/event-sourcing/cqrs/>`__" by Alexey Zimarev
- "`Entities as event streams <https://zimarev.com/blog/event-sourcing/entities-as-streams/>`__" by Alexey Zimarev
- "`Event Sourcing basics <https://zimarev.com/blog/event-sourcing/introduction/>`__" by Alexey Zimarev

- "`What is Event Sourcing? <https://eventstore.com/blog/what-is-event-sourcing/>`__" by Alexey Zimarev
- "`Event Sourcing and CQRS <https://eventstore.com/blog/event-sourcing-and-cqrs/>`__" by Alexey Zimarev

- "`Effective Aggregate Design <https://dddcommunity.org/library/vernon_2011/>`__" by Vaughn Vernon
- "`CQRS, Task Based UIs, Event Sourcing agh! <http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/>`__" by Greg Young
- "`Clarified CQRS <http://udidahan.com/2009/12/09/clarified-cqrs/>`__" by Udi Dahan
- "`How to create fully encapsulated Domain Models <https://udidahan.com/2008/02/29/how-to-create-fully-encapsulated-domain-models/>`__" by Udi Dahan

- "`Designing a Domain Model to enforce No Duplicate Names <https://github.com/ardalis/DDD-NoDuplicates>`__ by Steve Smith

Статьи на частые вопросы по проектированию API:

- "`Designing APIs for microservices <https://docs.microsoft.com/en-us/azure/architecture/microservices/design/api-design>`__"
- "`Web API design <https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design>`__"
- "`Web API implementation <https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-implementation>`__"
- "`Microsoft REST API Guidelines <https://github.com/Microsoft/api-guidelines>`__"
- "`Google REST API Guidelines <https://google.aip.dev/general>`__"
- "`Web API Design- Crafting Interfaces that Developers Love <https://pages.apigee.com/rs/apigee/images/api-design-ebook-2012-03.pdf>`__"
- "`REST vs. GraphQL: A Critical Review <https://goodapi.co/blog/rest-vs-graphql>`__"
- "`5 reasons you shouldn’t be using GraphQL <https://blog.logrocket.com/5-reasons-you-shouldnt-be-using-graphql-61c7846e7ed3/?gi=f67074d77004>`__" (`перевод на Русский <https://medium.com/devschacht/esteban-herrera-5-reasons-you-shouldnt-use-graphql-bae94ab105bc>`__)

Собственно, этих знаний достаточно для того, чтобы стать зрелым специалистом.
Своего рода - кандидатский минимум.
Далее - порядок чтения может быть произвольным.
Читать весь список необязательно.


Дополнительная литература (на выбор)
====================================


Учимся делать команду эффективной. Углубляем навыки.
----------------------------------------------------

Теперь можно прочесть и второе издание XP.

- "Extreme Programming Explained" 2nd edition by Kent Beck
- "Planning Extreme Programming" by Kent Beck, Martin Fowler
- "More Effective Agile: A Roadmap for Software Leaders" by Steve McConnell
- "Clean Agile: Back to Basics" by Robert C. Martin
- "Agile! The Good, the Hype and the Ugly" by Bertrand Meyer
- "Scrum and XP from the Trenches: How We Do Scrum" 2nd edition by Henrik Kniberg
- "The Mythical Man-Month Essays on Software Engineering Anniversary Edition" by Frederick P. Brooks, Jr.
- "Succeeding with Agile: Software Development Using Scrum" by Mike Cohn
- "User Stories Applied: For Agile Software Development" by Mike Cohn


Развитие личностных профессиональных качеств
--------------------------------------------

- "The Pragmatic Programmer: From Journeyman to Master" 1st edition by David Thomas, Andrew Hunt
    - "The Pragmatic Programmer: your journey to mastery, 20th Anniversary Edition" 2nd edition by David Thomas, Andrew Hunt
- "A Mind for Numbers: How to Excel at Math and Science" by Barbara Ann Oakley


Базы данных
-----------

- "Mastering PostgreSQL In Application Development" by Dimitri Fontaine
- "The Art of PostgreSQL" 2nd edition by Dimitri Fontaine - is the new title of "Mastering PostgreSQL in Application Development"
- "SQL Antipatterns. Avoiding the Pitfalls of Database Programming." by Bill Karwin
- "Refactoring Databases. Evolutionary Database Design" by Scott J Ambler and Pramod J. Sadalage
- "An Introduction to Database Systems" by C.J. Date
- "PostgreSQL 10 High Performance" by Ibrar Ahmed, Gregory Smith, Enrico Pirozzi


Изучаем распределенные системы. Третий заход.
---------------------------------------------

- "Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions" by Gregor Hohpe, Bobby Woolf
- "Service Design Patterns: Fundamental Design Solutions for SOAP/WSDL and RESTful Web Services" by Robert Daigneau
- "Microsoft .NET: Architecting Applications for the Enterprise" 2nd edition by Dino Esposito, Andrea Saltarello
- "`Cloud Design Patterns <https://docs.microsoft.com/en-us/azure/architecture/patterns/>`__"
- "`Cloud Design Patterns. Prescriptive architecture guidance for cloud applications <https://docs.microsoft.com/en-us/previous-versions/msp-n-p/dn568099(v=pandp.10)>`__" by Alex Homer, John Sharp, Larry Brader, Masashi Narumoto, Trent Swanson. (`Code Samples <http://aka.ms/cloud-design-patterns-sample>`__)
- "`Build Microservices on Azure <https://docs.microsoft.com/en-us/azure/architecture/microservices>`__" by Microsoft Corporation and community
- "`Cloud Best Practices <https://docs.microsoft.com/en-us/azure/architecture/best-practices/>`__" by Microsoft Corporation and community
- "`Performance Antipatterns <https://docs.microsoft.com/en-us/azure/architecture/antipatterns>`__" by Microsoft Corporation and community
- "`Azure Application Architecture Guide <https://docs.microsoft.com/en-us/azure/architecture/guide/>`__" by Microsoft Corporation and community
- "`Azure Data Architecture Guide <https://docs.microsoft.com/en-us/azure/architecture/data-guide/>`__" by Microsoft Corporation and community
- "Release It! Design and Deploy Production-Ready Software" 2nd edition by Michael Nygard
- "`Microservices Patterns: With examples in Java <https://www.manning.com/books/microservice-patterns>`__" 1st edition by Chris Richardson (`more info <https://microservices.io/book>`__)
- "Monolith to Microservices Evolutionary Patterns to Transform Your Monolith" by Sam Newman
- "The Site Reliability Workbook. Practical Ways to Implement SRE." by Betsy Beyer, Niall Richard Murphy, David K. Rensin, Kent Kawahara & Stephen Thorne
- "Database Reliability Engineering. Designing and Operating Resilient Database Systems." by Laine Campbell and Charity Majors
- "Designing Data-Intensive Applications. The Big Ideas Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann
- "Database Internals: A Deep Dive into How Distributed Data Systems Work" by Alex Petrov
- "Distributed systems: principles and paradigms" 3d edition by Andrew S. Tanenbaum, Maarten Van Steen
- "Service-Oriented Architecture Analysis and Design for Services and Microservices" by Thomas Erl
- "REST in Practice: Hypermedia and Systems Architecture" by Savas Parastatidis, Jim Webber, Ian Robinson
- "RESTful Web APIs: Services for a Changing World" by Leonard Richardson, Sam Ruby, Mike Amundsen
- "Web API Design Crafting Interfaces that Developers Love" by Brian Mulloy
- "REST API Design Rulebook" by Mark Massé


Углубляем DDD
-------------

- "Reactive Messaging Patterns with the Actor Model: Applications and Integration in Scala and Akka" by Vaughn Vernon
- "Patterns, Principles, and Practices of Domain-Driven Design" by Scott Millett, Nick Tune
- "Hands-On Domain-Driven Design with .NET Core: Tackling complexity in the heart of software by putting DDD principles into practice" by Alexey Zimarev
- "Event Sourced Building Blocks for Domain-Driven Design with Python <https://leanpub.com/dddwithpython>`__ by John Bywater


Изучаем проектирование
----------------------

- "Agile Software Development. Principles, Patterns, and Practices." by Robert C. Martin, James W. Newkirk, Robert S. Koss
- "Analysis Patterns. Reusable Object Models" by Martin Fowler
- "Implementation Patterns" by Kent Beck
- "`Development of Further Patterns of Enterprise Application Architecture <https://martinfowler.com/eaaDev/>`__" by Martin Fowler
- "Domain Specific Languages" by Martin Fowler (with Rebecca Parsons)
- "Pattern Hatching: Design Patterns Applied" by John Vlissides
- "`Microsoft Application Architecture Guide <https://docs.microsoft.com/en-us/previous-versions/msp-n-p/ff650706(v=pandp.10)?redirectedfrom=MSDN>`__" 2nd edition (Patterns & Practices) by Microsoft Corporation (J.D. Meier, David Hill, Alex Homer, Jason Taylor, Prashant Bansode, Lonnie Wall, Rob Boucher Jr., Akshay Bogawat)
- "Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development" by Craig Larman
- "Object-Oriented Software Construction" 2nd edition by Bertrand Meyer
- "Working Effectively with Legacy Code" by Michael C. Feathers
- "Refactoring To Patterns" by Joshua Kerievsky
- "Structure and Interpretation of Computer Programs" (aka SICP) 2nd edition (MIT Electrical Engineering and Computer Science) by Harold Abelson, Gerald Jay Sussman, Julie Sussman
- "Object Oriented Software Engineering: A Use Case Driven Approach" by Ivar Jacobson


POSA
----

- "Pattern-Oriented Software Architecture: A System of Patterns, Volume 1" by Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, Michael Stal
- "Pattern-Oriented Software Architecture: Patterns for Concurrent and Networked Objects, Volume 2" by Douglas C. Schmidt, Michael Stal, Hans Rohnert, Frank Buschmann
- "Pattern-Oriented Software Architecture: Patterns for Resource Management, Volume 3" by Michael Kircher, Prashant Jain
- "Pattern-Oriented Software Architecture: A Pattern Language for Distributed Computing, Volume 4" by Frank Buschmann, Kevin Henney, Douglas C. Schmidt
- "Pattern-Oriented Software Architecture: On Patterns and Pattern Languages, Volume 5" by Frank Buschmann, Kevin Henney, Douglas C. Schmidt


Алгоритмы. Второй заход.
------------------------

- "Introduction to Algorithms" 3d edition by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
- "Algorithms and Data Structures" (Oberon version: August 2004) by N.Wirth

Donald E. Knuth:

- "The Art of Computer Programming, Volume 1: Fundamental Algorithms" 3d edition by Donald Knuth
- "The Art of Computer Programming, Volume 1, Fascicle 1: MMIX; A RISC Computer for the New Millennium" 1st edition by Donald Knuth
- "The Art of Computer Programming, Volume 2, Seminumerical Algorithms" 3rd edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 3, Sorting and Searching" 2nd edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4, Fascicle 0: Introduction to Combinatorial Algorithms and Boolean Functions" 1st edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4, Fascicle 1: Bitwise Tricks & Techniques; Binary Decision Diagrams" 1st edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4, Fascicle 2: Generating All Tuples and Permutations" 1st edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4, Fascicle 3: Generating All Combinations and Partitions Paperback" 1st edition by Donald E. Knuth
- "Art of Computer Programming, Volume 4, Fascicle 4: Generating All Trees; History of Combinatorial Generation 1st edition by Donald E. Knuth
- "The Art of Computer Programming" Volume 4, Fascicle 5: Mathematical Preliminaries Redux; Introduction to Backtracking; Dancing Links" 1st edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4, Fascicle 6: Satisfiability" 1st edition by Donald E. Knuth
- "The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1" 1st edition by Donald E. Knuth

Хорошая подборка книг по алгоритмам: http://e-maxx.ru/bookz/


Тестирование
------------

- "xUnit Test Patterns. Refactoring Test Code." by Gerard Meszaros
- "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman, Nat Pryce
- "Agile Testing: A Practical Guide for Testers and Agile Teams" by Lisa Crispin, Janet Gregory
- "More Agile Testing: Learning Journeys for the Whole Team" by Lisa Crispin, Janet Gregory
- "ATDD by Example: A Practical Guide to Acceptance Test-Driven Development" by Markus Gärtner
- "Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation" by Jez Humble, David Farley
- "Continuous Integration: Improving Software Quality and Reducing Risk" by Paul M. Duvall, Steve Matyas, Andrew Glover


Компиляторы
-----------

- "Compiler Construction" by N.Wirth
- "Compilers: Principles, Techniques, and Tools" 2nd edition by Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman


Изучаем архитектуру
-------------------

- "Software Architecture in Practice" 3d edition by Len Bass, Paul Clements, Rick Kazman
- "Object-Oriented Analysis and Design with Applications" 3rd edition by Grady Booch, Robert A. Maksimchuk, Michael W. Engle, Bobbi J. Young Ph.D., Jim Conallen, Kelli A. Houston


Изучаем оценивание задач
------------------------

- "Software Estimation: Demystifying the Black Art (Developer Best Practices)" by Steve McConnell (я встречал в интернете `краткий конспект <http://igorshevchenko.ru/blog/entries/software-estimation>`__)
- "Agile Estimating and Planning" by Mike Cohn


Функциональное программирование
-------------------------------

- `"Software architecture: object-oriented vs functional <http://se.ethz.ch/~meyer/publications/functional/meyer_functional_oo.pdf>`__" by Bertrand Meyer
- "`Category Theory for Programmers <https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/>`__" by Bartosz Milewski (`unofficial PDF and LaTeX source <https://github.com/hmemcpy/milewski-ctfp-pdf>`__)
- "`Domain Modeling Made Functional. Tackle Software Complexity with Domain-Driven Design and F# <https://fsharpforfunandprofit.com/books/>`__" by Scott Wlaschin
- "`F# for Fun and Profit <https://fsharpforfunandprofit.com/>`__" by Scott Wlaschin
- "Functional Programming for the Object-Oriented Programmer" by Brian Marick
- "Functional Thinking" by Neal Ford
- "`Haskell <https://en.wikibooks.org/wiki/Haskell>`__"
- "`The Science of Functional Programming. A Tutorial, with Examples in Scala. <https://github.com/winitzki/sofp/blob/master/sofp-src/sofp.pdf>`__" by Sergei Winitzki, Ph.D.
- "Microservices with Clojure. Develop event-driven, scalable, and reactive microservices with real-time monitoring" by Anuj Kumar


Справочники
-----------

- "Computing Handbook. Computer Science and Software Engineering." 3d edition by Allen Tucker, Teofilo Gonzalez, Jorge Diaz-Herrera


Справочная информация
=====================


Body of Knowledge
-----------------

- "`Guide to the Systems Engineering Body of Knowledge (SEBoK) <https://www.sebokwiki.org/wiki/Download_SEBoK_PDF>`__"
- "`The Information Technology Architecture Body of Knowledge (ITABoK) <https://itabok.iasaglobal.org/>`__"
- "`The Enterprise Architecture Body of Knowledge (EABoK) <https://www.mitre.org/publications/technical-papers/guide-to-the-evolving-enterprise-architecture-body-of-knowledge>`__"
- "`A Guide to the Business Architecture Body of Knowledge(R) (BIZBOK(R) Guide) <https://www.businessarchitectureguild.org/page/BIZBOK>`__"
- "`A Guide to the Business Analysis Body of Knowledge (BABoK) <https://www.iiba.org/standards-and-resources/babok/>`__"
- "`The Project Management Body of Knowledge <https://www.pmi.org/pmbok-guide-standards/foundational/pmbok>`__"
- "`Учебник 4CIO. Настольная книга ИТ-Директора <https://book4cio.ru/>`__"
- "`Учебник 4CDTO. Настольная книга руководителя цифровой трансформации <https://4cio.ru/pages/570>`__"


ГОСТы
-----

- "`База ГОСТов allgosts.ru - 35. ИНФОРМАЦИОННЫЕ ТЕХНОЛОГИИ. МАШИНЫ КОНТОРСКИЕ <https://allgosts.ru/35/>`__"
- "`StandartGOST.ru - бесплатные ГОСТы и магазин документов. Информационные технологии. Машины конторские <https://standartgost.ru/0/753-informatsionnye_tehnologii_mashiny_kontorskie>`__"


Online-каталоги
---------------

- `Catalog of Refactorings <http://www.refactoring.com/catalog/>`__
- `Code Smell <http://c2.com/cgi/wiki?CodeSmell>`__
- `Anti Patterns Catalog <http://c2.com/cgi/wiki?AntiPatternsCatalog>`__
- `Catalog of Patterns of Enterprise Application Architecture <https://martinfowler.com/eaaCatalog/>`__
- `List of DSL Patterns <https://www.martinfowler.com/dslCatalog/>`__
- `Enterprise Integration Patterns <http://www.enterpriseintegrationpatterns.com/>`__
- `Service Design Patterns <http://servicedesignpatterns.com>`__
- `SOAPatterns.org <http://soapatterns.org/>`__
- `CloudPatterns.org <http://www.cloudpatterns.org/>`__
- `BigDataPatterns.org <http://www.bigdatapatterns.org/>`__
- `Microservices Patterns <https://microservices.io/patterns/>`__
- `Microservices Patterns (book) <https://www.manning.com/books/microservice-patterns>`__
- `Microservices Patterns from Sam Newman <https://samnewman.io/patterns/>`__
- `About DDD on the site of Ward Cunningham <http://ddd.fed.wiki.org/>`__
- `Refactoring Databases <http://www.databaserefactoring.com/>`__
- `XUnit Test Patterns <http://xunitpatterns.com/>`__
- `Cloud Design Patterns | Microsoft Docs <https://docs.microsoft.com/en-us/azure/architecture/patterns/>`__
- `Refactoring Databases <https://databaserefactoring.com/>`__
- `Catalog of Database Refactorings <http://www.agiledata.org/essays/databaseRefactoringCatalog.html>`__
- `Extreme Programming Rules <http://www.extremeprogramming.org/rules.html>`__
- `Consistency Models - a clickable map <https://jepsen.io/consistency>`__
- `Subway Map to Agile Practices - a clickable map <https://www.agilealliance.org/agile101/subway-map-to-agile-practices/>`__
- `The Arcitura Education Patterns, Mechanisms and Metrics Master Catalog <https://patterns.arcitura.com/>`__


Code Smell catalogs
-------------------

- Chapter 17: "Smells and Heuristics" of the book "Clean Code: A Handbook of Agile Software Craftsmanship" by Robert C. Martin
- Chapter 3. "Bad Smells in Code" of the book "Refactoring: Improving the Design of Existing Code" by Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts
- `Code Smell <http://c2.com/cgi/wiki?CodeSmell>`__ catalog on the site of Ward Cunningham
- "Refactoring To Patterns" by Joshua Kerievsky


Другие подборки литературы
--------------------------

- `Awesome lists <https://github.com/sindresorhus/awesome>`__
- `Awesome Domain-Driven Design <https://github.com/heynickc/awesome-ddd>`__
- `Awesome Microservices <https://github.com/mfornos/awesome-microservices>`__
- `Solution Architecture links, articles, books, video lessons, etc. <https://github.com/unlight/solution-architecture>`__
- `Awesome Algorithms <https://github.com/tayllan/awesome-algorithms>`__
- `Awesome Algorithms Education <https://github.com/gaerae/awesome-algorithms-education>`__
- `List of awesome university courses for learning Computer Science <https://github.com/prakhar1989/awesome-courses>`__
- `MAXimal :: bookz - электронные версии различных книг по алгоритмам <http://e-maxx.ru/bookz/>`__
- `Programming and design learning resources by Kamil Grzybek <http://www.kamilgrzybek.com/programming-and-design-resources/>`__
- `Список книг от Сергея Теплякова <https://sergeyteplyakov.blogspot.com/2013/08/blog-post.html>`__
- `Reading List by Mathias Verraes <https://verraes.net/2015/12/reading-list/>`__
- `Книги по направлению Архитектура и проектирование ПО от эксперта luxoft <https://www.luxoft-training.ru/about/experts/answers/302/30945/>`__


Почтовые рассылки и сообщества
------------------------------

- `Domain Driven Design Community <http://dddcommunity.org/>`__
- `Domain Driven Design Weekly <http://dddweekly.com/>`__
- `Microservice Weekly <https://microserviceweekly.com/>`__


.. _reference-applications-ru:

Эталонные демонстрационные приложения
=====================================

- `eShopOnContainers <https://github.com/dotnet-architecture/eShopOnContainers>`__ (CQRS, DDD, Microservices)
- `Microsoft patterns & pratices CQRS Journey sample application <https://github.com/microsoftarchive/cqrs-journey>`__ (CQRS, DDD, Event Sourcing, SAGA transactions)

..

    "A perfect example of this [you can see] if you go look at the CQRS and Event Sourcing by Microsoft Patterns and Practices, which is heavily focused on doing this inside of Azure using their toolkits."

    \- Greg Young, "`A Decade of DDD, CQRS, Event Sourcing <https://youtu.be/LDW0QWie21s?t=1092>`__" at 18:15

- `Full Modular Monolith application with Domain-Driven Design approach <https://github.com/kgrzybek/modular-monolith-with-ddd>`__ by Kamil Grzybek
- `Sample .NET Core REST API CQRS implementation with raw SQL and DDD using Clean Architecture <https://github.com/kgrzybek/sample-dotnet-core-cqrs-api>`__ by Kamil Grzybek
- `Refactoring from anemic to rich Domain Model example <https://github.com/kgrzybek/refactoring-from-anemic-to-rich-domain-model-example>`__ by Kamil Grzybek
- `Sample Bounded Contexts for C#.NET from the book "Implementing Domain-Driven Design" <https://github.com/VaughnVernon/IDDD_Samples_NET>`__ by Vaughn Vernon
- `Sample Bounded Contexts from the book "Implementing Domain-Driven Design" <https://github.com/VaughnVernon/IDDD_Samples>`__ by Vaughn Vernon
- Implementation of samples from the book "Domain-Driven Design" by Eric Evans in `Java <https://github.com/citerus/dddsample-core>`__, `C# <https://github.com/SzymonPobiega/DDDSample.Net>`__, `Ruby <https://github.com/paulrayner/ddd_sample_app_ruby>`__, `Golang <https://github.com/marcusolsson/goddd>`__ (`yet another Golang <https://github.com/go-kit/kit/tree/master/examples/shipping>`__). See also `the article <https://www.citerus.se/go-ddd>`__.
- `Simple CQRS example <https://github.com/gregoryyoung/m-r>`__ by Greg Young (приложение так же реализует Event Sourcing)
- `Greg Young's Simple CQRS in F# <https://github.com/thinkbeforecoding/m-r>`__ by Jérémie Chassaing
- `Complete serverless application to show how to apply DDD, Clean Architecture, and CQRS by practical refactoring of a Go project <https://github.com/ThreeDotsLabs/wild-workouts-go-ddd-example>`__ (`more info <https://threedots.tech/post/serverless-cloud-run-firebase-modern-go-application/>`__) by Robert Laszczak
- `Clean Monolith Shop <https://github.com/ThreeDotsLabs/monolith-microservice-shop>`__ by Robert Laszczak - Source code for `Why using Microservices or Monolith can be just a detail? <https://threedots.tech/post/microservices-or-monolith-its-detail/>`__ article
- `go-iddd - showcase project for implementing DDD in Go <https://github.com/AntonStoeckl/go-iddd>`__ by Anton Stöckl (see more info `here <https://medium.com/@TonyBologni/implementing-domain-driven-design-and-hexagonal-architecture-with-go-1-292938c0a4d4>`__ and `here <https://medium.com/@TonyBologni/implementing-domain-driven-design-and-hexagonal-architecture-with-go-2-efd432505554>`__).
- `Demo taxi system, using eventsourcing library <https://github.com/johnbywater/es-example-taxi-demo>`__ by John Bywater
- `FTGO example application. Example code for the book Microservice patterns <https://github.com/microservices-patterns/ftgo-application>`__ by Chris Richardson
- `Sample code for the book Principles, Practices and Patterns of Domain-Driven Design <https://github.com/elbandit/PPPDDD>`__ by Scott Millett, Nick Tune
- `Hands-On Domain-Driven Design with .NET Core, published by Packt <https://github.com/PacktPublishing/Hands-On-Domain-Driven-Design-with-.NET-Core>`__ by Alexey Zimarev
- `Extended code samples related to the book "Domain Modeling Made Functional" <https://github.com/swlaschin/DomainModelingMadeFunctional>`__ by Scott Wlaschin
- `Railway-Oriented-Programming-Example <https://github.com/swlaschin/Railway-Oriented-Programming-Example>`__ by Scott Wlaschin
- `DDD with Actors <https://github.com/VaughnVernon/DDDwithActors>`__ by Vaughn Vernon
- `The examples for the book "Reactive Messaging Patterns with the Actor Model" <https://github.com/VaughnVernon/ReactiveMessagingPatterns_ActorModel>`__ by Vaughn Vernon
- `A Stock Trader system to demonstrate reactive systems development <https://github.com/VaughnVernon/reactive-stock-trader>`__ (`source <https://github.com/RedElastic/reactive-stock-trader>`__ by RedElastic)

- `Refactoring from Anemic Domain Model Towards a Rich One <https://github.com/vkhorikov/AnemicDomainModel>`__ by Vladimir Khorikov
- `DDD in Practice <https://github.com/vkhorikov/DddInAction>`__ by Vladimir Khorikov
- `DDD and EF Core <https://github.com/vkhorikov/DddAndEFCore>`__ by Vladimir Khorikov
- `CQRS in Practice <https://github.com/vkhorikov/CqrsInPractice>`__ by Vladimir Khorikov
- `Applying Functional Principles in C# <https://github.com/vkhorikov/FuntionalPrinciplesCsharp>`__ by Vladimir Khorikov
- `Specification Pattern in C# <https://github.com/vkhorikov/SpecPattern>`__ by Vladimir Khorikov
- `Specification pattern implementation in C# <https://github.com/vkhorikov/SpecificationPattern>`__ by Vladimir Khorikov

Others:

- `DDD Sample Projects <https://github.com/heynickc/awesome-ddd#sample-projects>`__

..
    - "Rapid Development: Taming Wild Software Schedules" by Steve McConnell
    - "The Definitive Guide to MongoDB" by David Hows, Peter Membrey, Eelco Plugge, Tim Hawkins
    - "High Performance MySQL" by Baron Schwartz, Peter Zaitsev, and Vadim Tkachenko
    - "PostgreSQL: Up and Running" by Regina Obe and Leo Hsu

.. update:: Aug 05, 2020

