
Понимание Redux и Flux для ООП программистов
============================================

.. post:: Jan 03, 2018
   :language: ru
   :tags: OOP, Flux, Redux, JavaScript
   :category:
   :author: Ivan Zakrevsky

На тему Redux / Flux много много написано в интернете, но в основном все описания сводятся к тому, "как" они делают непонятно "что" и "зачем".
Я постараюсь изложить свое видение этого вопроса, возможно, оно окажется более понятным для ООП-программистов.

Отличие между прямым доступом к данным и использованием паттернов Redux / Flux такое же, как между использованием структур данных и объектов.
Если Вы хорошо понимаете объектно-ориентированное программирование, то предыдущего предложения Вам должно быть достаточно, чтобы все понять.

Краткую историю термина ООП Вы можете посмотреть в этом видеоролике "`David West OOP is Dead! Long Live OODD! <https://www.youtube.com/watch?v=RdE-d_EhzmA>`__".

Термин "Объектно-Ориентированное Программирование" был провозглашен Alan Kay, создателем Smalltalk Language.

    "Much is mentioned on WardsWiki of the definition of OO promulgated by Alan Kay, the inventor of Smalltalk Language.
    Many consider it the most authoritative of the DefinitionsForOo, on the grounds that HeInventedTheTerm.
    (Others disagree, that FlameWar belongs on other pages and not here)."

    http://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented

Вы наверняка много слышали о негативных последствиях прямого обращения к состоянию объекта.
Объект предоставляет свое поведение, и скрывает свое состояние. Структуры данных - наоборот.
Непосредственное обращение к состоянию объекта извне усложняет эволюционирование программы, а прямое изменение состояния объекта извне - сильно затрудняет отладку.
В таком случае становится сложно понять, кто и где использует или изменяет то или иное свойство объекта.
Это особенно хорошо это ощутимо в языках программирования, которые не поддерживают дескрипторы.

Существуют языки, ориентированные на сообщения (`Message Oriented Languages <http://wiki.c2.com/?MessageOrientedProgramming>`__), Objective-C, Ruby, Smalltalk...
Собственно, Smalltalk оказал огромное влияние на ООП, и даже, в определенной мере, выступил его прародителем.

    | As noted below, this is primarily a description of Smalltalk
    | 1. EverythingIsAnObject.
    | 2. Objects communicate by sending and receiving messages (in terms of objects).
    | 3. Objects have their own memory (in terms of objects).
    | 4. Every object is an instance of a class (which must be an object).
    | 5. The class holds the shared behavior for its instances (in the form of objects in a program list)
    | 6. To eval a program list, control is passed to the first object and the remainder is treated as its message.
    | http://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented

Обратите внимание на п.2 "Objects communicate by sending and receiving messages (in terms of objects).".
Начинаете улавливать сходство с Redux / Flux?

Существует письмо Alan Kay, которое я считаю нужным процитировать полностью:

    Alan Kay On Messaging
    From: Alan Kay <alank@wdi.disney.com>
    Date: 1998-10-10 07:39:40 +0200
    To: squeak@cs.uiuc.edu
    Subject: Re: prototypes vs classes was: Re: Sun's HotSpot

    Folks --

    Just a gentle reminder that I took some pains at the last OOPSLA to try to
    remind everyone that Smalltalk is not only NOT its syntax or the class
    library, it is not even about classes. I'm sorry that I long ago coined the
    term "objects" for this topic because it gets many people to focus on the
    lesser idea.

    The big idea is "messaging" - that is what the kernal of Smalltalk/Squeak
    is all about (and it's something that was never quite completed in our
    Xerox PARC phase). The Japanese have a small word - ma - for "that which
    is in between" - perhaps the nearest English equivalent is "interstitial".
    The key in making great and growable systems is much more to design how its
    modules communicate rather than what their internal properties and
    behaviors should be. Think of the internet - to live, it (a) has to allow
    many different kinds of ideas and realizations that are beyond any single
    standard and (b) to allow varying degrees of safe interoperability between
    these ideas.

    If you focus on just messaging - and realize that a good metasystem can
    late bind the various 2nd level architectures used in objects - then much
    of the language-, UI-, and OS based discussions on this thread are really
    quite moot. This was why I complained at the last OOPSLA that - whereas at
    PARC we changed Smalltalk constantly, treating it always as a work in
    progress - when ST hit the larger world, it was pretty much taken as
    "something just to be learned", as though it were Pascal or Algol.
    Smalltalk-80 never really was mutated into the next better versions of OOP.
    Given the current low state of programming in general, I think this is a
    real mistake.

    I think I recall also pointing out that it is vitally important not just to
    have a complete metasystem, but to have fences that help guard the crossing
    of metaboundaries. One of the simplest of these was one of the motivations
    for my original excursions in the late sixties: the realization that
    assignments are a metalevel change from functions, and therefore should not
    be dealt with at the same level - this was one of the motivations to
    encapsulate these kinds of state changes, and not let them be done willy
    nilly. I would say that a system that allowed other metathings to be done
    in the ordinary course of programming (like changing what inheritance
    means, or what is an instance) is a bad design. (I believe that systems
    should allow these things, but the design should be such that there are
    clear fences that have to be crossed when serious extensions are made.)

    I would suggest that more progress could be made if the smart and talented
    Squeak list would think more about what the next step in metaprogramming
    should be - how can we get great power, parsimony, AND security of meaning?

    Cheers to all,

    Alan

    | - http://lists.squeakfoundation.org/pipermail/squeak-dev/1998-October/017019.html
    | - http://wiki.c2.com/?AlanKayOnMessaging

И еще одно известное письмо:

    | E-Mail of 2003-07-23
    | Dr. Alan Kay was so kind as to answer my questions about the term “object-oriented programming”.
    | Clarification of "object-oriented" [E-Mail]

    | Date: Wed, 23 Jul 2003 09:33:31 -0800
    | To: Stefan Ram [removed for privacy]
    | From: Alan Kay [removed for privacy]
    | Subject: Re: Clarification of "object-oriented"
    | [some header lines removed for privacy]
    | Content-Type: text/plain; charset="us-ascii" ; format="flowed"
    | Content-Length: 4965
    | Lines: 117

    | Hi Stefan --

    | Sorry for the delay but I was on vacation.

    | At 6:27 PM +0200 7/17/03, Stefan Ram wrote:
    | >   Dear Dr. Kay,
    | >
    | >   I would like to have some authoritative word on the term
    | >   "object-oriented programming" for my tutorial page on the
    | >   subject. The only two sources I consider to be "authoritative"
    | >   are the International Standards Organization, which defines
    | >   "object-oriented" in "ISO/IEC 2382-15", and you, because,
    | >   as they say, you have coined that term.

    | I'm pretty sure I did.

    | > Unfortunately, it is difficult to find a web page or source
    | > with your definition or description of that term. There are
    | > several reports about what you might have said in this regard
    | > (like "inheritance, polymorphism and encapsulation"), but
    | > these are not first-hand sources. I am also aware that later
    | > you put more emphasis on "messaging" - but I still would like
    | > to know about "object oriented".

    | > For the records, my tutorial page, and further distribution
    | > and publication could you please explain:

    | >   When and where was the term "object-oriented" used first?


    | At Utah sometime after Nov 66 when, influenced by Sketchpad, Simula, 
    | the design for the ARPAnet, the Burroughs B5000, and my background in 
    | Biology and Mathematics, I thought of an architecture for 
    | programming. It was probably in 1967 when someone asked me what I was 
    | doing, and I said: "It's object-oriented programming".

    | The original conception of it had the following parts.

    |   - I thought of objects being like biological cells and/or individual 
    | computers on a network, only able to communicate with messages (so 
    | messaging came at the very beginning -- it took a while to see how to 
    | do messaging in a programming language efficiently enough to be 
    | useful).


    |   - I wanted to get rid of data. The B5000 almost did this via its 
    | almost unbelievable HW architecture. I realized that the 
    | cell/whole-computer metaphor would get rid of data, and that "<-" 
    | would be just another message token (it took me quite a while to 
    | think this out because I really thought of all these symbols as names 
    | for functions and procedures.


    |   - My math background made me realize that each object could have 
    | several algebras associated with it, and there could be families of 
    | these, and that these would be very very useful. The term 
    | "polymorphism" was imposed much later (I think by Peter Wegner) and 
    | it isn't quite valid, since it really comes from the nomenclature of 
    | functions, and I wanted quite a bit more than functions. I made up a 
    | term "genericity" for dealing with generic behaviors in a 
    | quasi-algebraic form.


    |   - I didn't like the way Simula I or Simula 67 did inheritance 
    | (though I thought Nygaard and Dahl were just tremendous thinkers and 
    | designers). So I decided to leave out inheritance as a built-in 
    | feature until I understood it better.


    | My original experiments with this architecture were done using a 
    | model I adapted from van Wijngaarten's and Wirth's "Generalization of 
    | Algol" and Wirth's Euler. Both of these were rather LISP-like but 
    | with a more conventional readable syntax. I didn't understand the 
    | monster LISP idea of tangible metalanguage then, but got kind of 
    | close with ideas about extensible languages draw from various 
    | sources, including Irons' IMP.


    | The second phase of this was to finally understand LISP and then 
    | using this understanding to make much nicer and smaller and more 
    | powerful and more late bound understructures. Dave Fisher's thesis 
    | was done in "McCarthy" style and his ideas about extensible control 
    | structures were very helpful. Another big influence at this time was 
    | Carl Hewitt's PLANNER (which has never gotten the recognition it 
    | deserves, given how well and how earlier it was able to anticipate 
    | Prolog).


    | The original Smalltalk at Xerox PARC came out of the above. The 
    | subsequent Smalltalk's are complained about in the end of the History 
    | chapter: they backslid towards Simula and did not replace the 
    | extension mechanisms with safer ones that were anywhere near as 
    | useful.

    | >   What does "object-oriented [programming]" mean to you?
    | >   (No tutorial-like introduction is needed, just a short
    | >   explanation [like "programming with inheritance,
    | >   polymorphism and encapsulation"] in terms of other concepts
    | >   for a reader familiar with them, if possible. Also, it is
    | >   not neccessary to explain "object", because I already have
    | >   sources with your explanation of "object" from
    | >   "Early History of Smalltalk".)


    | (I'm not against types, but I don't know of any type systems that 
    | aren't a complete pain, so I still like dynamic typing.)


    | OOP to me means only messaging, local retention and protection and 
    | hiding of state-process, and extreme late-binding of all things. It 
    | can be done in Smalltalk and in LISP. There are possibly other 
    | systems in which this is possible, but I'm not aware of them.

    Cheers,

    Alan

    | >   Thank you,
    | >   Stefan Ram

    | - http://www.purl.org/stefan_ram/pub/doc_kay_oop_en


Последний абзац настолько важен, что я повторю: **"OOP to me means only messaging, local retention and protection and hiding of state-process, and extreme late-binding of all things."** (Alan Kay)

Так же стоит отдельно повторить этот абзац:

    "I thought of objects being like biological cells and/or individual computers on a network, only able to communicate with messages (so messaging came at the very beginning -- it took a while to see how to do messaging in a programming language efficiently enough to be useful)." (Alan Kay)

Мы должны скрывать состояние не потому что это усложняет отладку, а потому что в этом заключается сама идея ООП!

Вы поймете Redux / Flux намного лучше, если начнете с прочтения этой статьи: "`Event Sourcing <https://martinfowler.com/eaaDev/EventSourcing.html>`__".

Event Sourcing, Flux и Redux делают то же самое, что и "`Encapsulate Field <https://www.refactoring.com/catalog/encapsulateField.html>`__".
Они скрывают состояние и предоставляют поведение!

Вызов метода объекта - это передача ему сообщения в виде аргуметов метода.
Сигнатура метода - это протокол общения.
Никто не может изменять состояние объекта кроме него самого.
Мы можем попросить объект изменить состояние, но мы не можем изменить его непосредственно.
Таким образом, объект обретает полный контроль над своим состоянием.

.. update:: Jan 03, 2018
