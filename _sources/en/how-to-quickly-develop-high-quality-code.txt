
How to quickly develop high-quality code. Team work.
====================================================

.. post:: Jul 10, 2017
   :language: en
   :tags:
   :category:
   :author: Ivan Zakrevsky

This article is about how to write high-quality code quickly.

.. contents:: Contents

Myths
=====

There are several myths:


The first myth. Horizontal stratification of team.
--------------------------------------------------

There is an opinion that a team should be broken by three layers: junior, middle and senior.

The truth is that it's enough to have at least one weak developer in the team to lose a lot of time for the whole team.

    There are two ways of constructing a software design: one way is to make it so simple that there are obviously no deficiencies, and the other is to make it so complicated that there are no obvious deficiencies. (C. A. R. Hoare)

Do you know the Primary Technical Imperative of software development?

    Managing complexity is the most important technical topic in software development. In my view, it's so important that Software's Primary Technical Imperative has to be managing complexity.
    («Code Complete» [#fncodec]_)

During code construction developer reads code for 91% of the time, and only for 9% of the time he types text from keyboard.

    You might ask: How much is code really read? Doesn’t most of the effort go into
    writing it?

    Have you ever played back an edit session? In the 80s and 90s we had editors like Emacs
    that kept track of every keystroke. You could work for an hour and then play back your whole
    edit session like a high-speed movie. When I did this, the results were fascinating.

    The vast majority of the playback was scrolling and navigating to other modules!

    - Bob enters the module.
    - He scrolls down to the function needing change.
    - He pauses, considering his options.
    - Oh, he’s scrolling up to the top of the module to check the initialization of a variable.
    - Now he scrolls back down and begins to type.
    - Ooops, he’s erasing what he typed!
    - He types it again.
    - He erases it again!
    - He types half of something else but then erases that!
    - He scrolls down to another function that calls the function he’s changing to see how it is called.
    - He scrolls back up and types the same code he just erased.
    - He pauses.
    - He erases that code again!
    - He pops up another window and looks at a subclass. Is that function overridden?

    . . .

    You get the drift. Indeed, the ratio of time spent reading vs. writing is well over 10:1.
    We are constantly reading old code as part of the effort to write new code.

    Because this ratio is so high, we want the reading of code to be easy, even if it makes
    the writing harder. Of course there’s no way to write code without reading it, so making it
    easy to read actually makes it easier to write.

    There is no escape from this logic. You cannot write code if you cannot read the sur-
    rounding code. The code you are trying to write today will be hard or easy to write
    depending on how hard or easy the surrounding code is to read. So if you want to go fast,
    if you want to get done quickly, if you want your code to be easy to write, make it easy to
    read.
    («Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_)

..

    "Dijkstra pointed out that no one's skull is really big enough to contain a modern
    computer program (Dijkstra 1972), which means that we as software developers
    shouldn't try to cram whole programs into our skulls at once; we should try to organize
    our programs in such a way that we can safely focus on one part of it at a time. The goal
    is to minimize the amount of a program you have to think about at any one time. You
    might think of this as mental juggling—the more mental balls the program requires you
    to keep in the air at once, the more likely you'll drop one of the balls, leading to a design
    or coding error.

    At the software-architecture level, the complexity of a problem is reduced by dividing
    the system into subsystems. Humans have an easier time comprehending several simple
    pieces of information than one complicated piece. The goal of all software-design
    techniques is to break a complicated problem into simple pieces. The more independent
    the subsystems are, the more you make it safe to focus on one bit of complexity at a
    time. Carefully defined objects separate concerns so that you can focus on one thing at a
    time. Packages provide the same benefit at a higher level of aggregation.

    Keeping routines short helps reduce your mental workload. Writing programs in terms
    of the problem domain, rather than in terms of low-level implementation details, and
    working at the highest level of abstraction reduce the load on your brain.

    The bottom line is that programmers who compensate for inherent human limitations
    write code that's easier for themselves and others to understand and that has fewer
    errors."
    («Code Complete» [#fncodec]_)

..

    Software's Primary Technical Imperative is managing complexity. This is greatly
    aided by a design focus on simplicity.
    Simplicity is achieved in two general ways: minimizing the amount of essential
    complexity that anyone's brain has to deal with at any one time, and keeping
    accidental complexity from proliferating needlessly.
    («Code Complete» [#fncodec]_)

..

    The number
    "7±2" has been found to be a number of discrete items a person can remember while
    performing other tasks (Miller 1956). If a class contains more than about seven data
    members, consider whether the class should be decomposed into multiple smaller
    classes (Riel 1996).
    («Code Complete» [#fncodec]_)

..

    Collective ownership increases your feeling of personal power on a project. On an XP
    project you are never stuck with someone else's stupidity. You see something in the
    way, you get it out of the way. If you choose to live with something for the moment
    80because it is expedient, that is your business. But you're never stuck. So you never
    get the sense that, "I could get my work done, if only I didn't have to deal with these
    other idiots." One less frustration. One step closer to clear thinking.

    Collective ownership also tends to spread knowledge of the system around the team.
    It is unlikely that there will ever be a part of the system that only two people know
    (it has to be at least a pair, which is already better than the usual situation where
    one smart programmer holds everyone else hostage). This further reduces project
    risk.
    (Kent Beck [#fnxp]_)

Thus, when one developer writes an unreadable code for 9% of his time, this code slows down the development velocity of the whole team by 91%.
The code is written once, but is read incommensurably many times in the development process.

The emphasis on "fast writing" code actually leads to a reduction in the development velocity in geometric progression. And the emphasis on "readability" of code leads to an increase in the development velocity, also in an geometric progression.

If code is not readable, has a bad code navigation, a bad decomposition, a lot of code smells, hight coupling, low cohesion, violates SRP, OC principles, has poor test coverage, doesn't uses type hinting and doesn't allow to use automated refactoring, then this code slows rate of development for 91% of time of the whole team.

Thus, each developer in the team MUST be a senior developer.
The best way to achieve it is the XP by Kent Beck.

Experience sharing is the rule №1 for the high-skilled team.
If your team still has a junior developer after two months, your team needs a better manager.

    Pair programming is also not a tutoring session. Sometimes pairs contain one
    partner with much more experience than the other partner. When this is true, the
    first few sessions will look a lot like tutoring. The junior partner will ask lots of
    questions, and type very little. Very quickly, though, the junior partner will start
    catching stupid little mistakes, like unbalanced parentheses. The senior partner will
    notice the help. After a few more weeks, the junior partner will start picking up the
    larger patterns that the senior partner is using, and notice deviations from those
    patterns.

    In a couple of months, typically, the gap between the partners is not nearly so
    noticeable as it was at first. The junior partner is typing more regularly. The pair
    notices that each of them has strengths and weaknesses. Productivity, quality, and
    satisfaction rise.
    (Kent Beck [#fnxp]_)

..

    So, why does pair programming work for XP? Well, the first value is communication,
    and there are few forms of communication more intense than face-to-face. So, pair
    programming works for XP because it encourages communication. I like to think of
    the analogy of a pool of water. When an important new bit of information is learned
    by someone on the team, it is like putting a drop of dye in the water. Because of the
    pairs switching around all the time, the information rapidly diffuses throughout the
    team just as the dye spreads throughout the pool. Unlike the dye, however, the
    information becomes richer and more intense as it spreads and is enriched by the
    experience and insight of everyone on the team.

    In my experience, pair programming is more productive than dividing the work
    between two programmers and then integrating the results. Pair programming is
    often a sticking point for folks wanting to adopt XP. All I can say is that you should
    get good at it, then try an iteration where you pair for all production code and
    another where you program everything solo. Then you can make your own decision.
    (Kent Beck [#fnxp]_)

..

    It's hard to collaborate. Our whole education system is tuned to individual
    achievement. If you work with someone on a project, the teacher calls it cheating
    and punishes you. The reward systems in most companies, with individual
    evaluations and raises (often cast as a zero sum game), also encourages individual thinking.
    You will likely have to learn new people skills, interacting as closely with your team as you will in XP.
    (Kent Beck [#fnxp]_)


The second myth. Quality code is not suitable for hot deadline.
---------------------------------------------------------------

Team doesn't have time to write high-quality code, because they have a hot deadline.

In reality you have the hot deadline because you have the unpredictable codebase which requires a lot of your time.
You spend a lot of time to try to understand messy mishmash of a code.
Sometimes you are able to understand the code only with debugger.
Your code has a poor test coverage, therefore you spend a lot of time for bugfixes.
Sometimes you are not able to implement a some feature due to poor design, but you also can't to refactor the code because of the poor test coverage.
Your code has a lot of duplicates which are the cause of a lot of bugs.

    The General Principle of Software Quality is
    that improving quality reduces development costs.

    Understanding this principle depends on understanding a key observation: the best way
    to improve productivity and quality is to reduce the time spent reworking code, whether
    the rework arises from changes in requirements, changes in design, or debugging. The
    industry-average productivity for a software product is about 10 to 50 of lines of
    delivered code per person per day (including all noncoding overhead). It takes only a
    matter of minutes to type in 10 to 50 lines of code, so how is the rest of the day spent?
    Part of the reason for these seemingly low productivity figures is that industry average
    numbers like these factor nonprogrammer time into the lines-of-code-per-day figure.
    Tester time, project manager time, and administrative support time are all included.
    Noncoding activities, such as requirements development and architecture work, are also
    typically factored into those lines-of-code-per-day figures. But none of that is what
    takes up so much time.

    The single biggest activity on most projects is debugging and correcting code that
    doesn't work properly. Debugging and associated refactoring and other rework consume
    about 50 percent of the time on a traditional, naive software-development cycle. (See
    Section 3.1, "Importance of Prerequisites," for more details.) Reducing debugging by
    preventing errors improves productivity. Therefore, the most obvious method of
    shortening a development schedule is to improve the quality of the product and decrease
    the amount of time spent debugging and reworking the software.
    This analysis is confirmed by field data. In a review of 50
    development projects involving over 400 work-years of effort and
    almost 3 million lines of code, a study at NASA's Software
    Engineering Laboratory found that increased quality assurance was
    associated with decreased error rate but did not increase overalldevelopment cost (Card 1987).

    A study at IBM produced similar findings:

    Software projects with the lowest levels of defects had the shortest development
    schedules and the highest development productivity.... software defect removal is
    actually the most expensive and time-consuming form of work for software (Jones
    2000).

    The same effect holds true at the small end of the scale. In a 1985
    study, 166 professional programmers wrote programs from the
    same specification. The resulting programs averaged 220 lines of
    code and a little under five hours to write. The fascinating result
    was that programmers who took the median time to complete their
    programs produced programs with the greatest number of errors.
    The programmers who took more or less than the median time
    produced programs with significantly fewer errors (DeMarco and
    Lister 1985).

    The two slowest groups took about five times as long to achieve roughly the same
    defect rate as the fastest group. It's not necessarily the case that writing software without
    defects takes more time than writing software with defects. As the graph shows, it can
    take less.
    («Code Complete» [#fncodec]_)

..

    Watts Humphrey reports that teams using the Team Software Process
    (TSP) have achieved defect levels of about 0.06 defects per 1000 lines of code.
    TSP focuses on training developers not to create defects in the first place (Weber
    2003).

    The results of the TSP and cleanroom projects confirm another version of the General
    Principle of Software Quality: it's cheaper to build high-quality software than it is to
    build and fix low-quality software. Productivity for a fully checked-out, 80,000-line
    cleanroom project was 740 lines of code per work-month. The industry average rate for
    fully checked-out code is closer to 250–300 lines per work-month, including all
    noncoding overhead (Cusumano et al 2003). The cost savings and productivity come
    from the fact that virtually no time is devoted to debugging on TSP or cleanroom
    projects. No time spent on debugging? That is truly a worthy goal!
    («Code Complete» [#fncodec]_)

..

    Quality is another strange variable. Often, by insisting on better quality you can get
    projects done sooner, or you can get more done in a given amount of time. This
    happened to me when I started writing unit tests...
    As soon as I had my tests, I had so much more
    confidence in my code that I wrote faster, without stress. I could clean up my
    system more easily, which made further development easier. I've also seen this
    happen with teams. As soon as they start testing, or as soon as they agree on coding
    standards, they start going faster.

    There is a strange relationship between internal and external quality. External quality
    is quality as measured by the customer. Internal quality is quality as measured by
    the programmers. Temporarily sacrificing internal quality to reduce time to market in
    hopes that external quality won't suffer too much is a tempting short-term play. And
    you can often get away with making a mess for a matter of weeks or months.
    Eventually, though, internal quality problems will catch up with you and make your
    software prohibitively expensive to maintain, or unable to reach a competitive level
    of external quality.
    (Kent Beck [#fnxp]_)

..

    Why can't you just listen, write a test case, make it run, listen, write a test case,
    make it run indefinitely? Because we know it doesn't work that way. You can do that
    for a while. In a forgiving language you may even be able to do that for a long while.
    Eventually, though, you get stuck. The only way to make the next test case run is to
    break another. Or the only way to make the test case run is far more trouble than it
    is worth. Entropy claims another victim.

    The only way to avoid this is to design. Designing is creating a structure that
    organizes the logic in the system. Good design organizes the logic so that a change
    45 in one part of the system doesn't always require a change in another part of the system.
    Good design ensures that every piece of logic in the system has one and only one home.
    Good design puts the logic near the data it operates allows the extension of the system with changes in only one place.
    (Kent Beck [#fnxp]_)

..

    ... the activity of design is not an option. It must be given serious thought for software development to be effective.
    (Kent Beck [#fnxp]_)

There is only one way to develop a software quickly: to do it in the right way for the first time.


The third myth. Pair programming reduces the velocity of development.
---------------------------------------------------------------------

There is an opinion that pair programming reduces the velocity of development.

    Studies at the Software Engineering
    Institute have found that developers insert an average of 1 to 3
    defects per hour into their designs and 5 to 8 defects per hour into
    code (Humphrey 1997), so attacking these blind spots is a key to
    effective construction.
    («Code Complete» [#fncodec]_)

..

    The primary purpose of collaborative construction is to improve
    software quality. As noted in Chapter 20, "The Software-Quality
    Landscape," software testing has limited effectiveness when used
    alone—the average defect-detection rate is only about 30 percent
    for unit testing, 35 percent for integration testing, and 35 percent
    for low-volume beta testing. In contrast, the average
    effectivenesses of design and code inspections are 55 and 60
    percent (Jones 1996). The secondary benefit of collaborative
    construction is that it decreases development time, which in turn
    lowers development costs.
    
    Early reports on pair programming suggest that it can achieve a
    code-quality level similar to formal inspections (Shull et al 2002).
    The cost of full-up pair programming is probably higher than the
    cost of solo development—on the order of 10–25 percent higher—
    but the reduction in development time appears to be on the order of
    45 percent, which in some cases may be a decisive advantage over
    solo development (Boehm and Turner 2004), although not over
    inspections which have produced similar results.
    («Code Complete» [#fncodec]_)

..

    A number of these cases illustrate the General Principle of Software Quality, which
    holds that reducing the number of defects in the software also improves development
    time.

    Various studies have shown that in addition to being more effective
    at catching errors than testing, collaborative practices find different
    kinds of errors than testing does (Myers 1978; Basili, Selby, and
    Hutchens 1986). As Karl Wiegers points out, "A human reviewer
    can spot unclear error messages, inadequate comments, hard-coded
    variable values, and repeated code patterns that should be
    consolidated. Testing won't" (Wiegers 2002). A secondary effect is
    that when people know their work will be reviewed, they scrutinize
    it more carefully. Thus, even when testing is done effectively,
    reviews or other kinds of collaboration are needed as part of a
    comprehensive quality program.
    («Code Complete» [#fncodec]_)

..

    Informal review procedures were passed on from person to person in the general culture
    of computing for many years before they were acknowledged in print. The need for
    reviewing was so obvious to the best programmers that they rarely mentioned it in print,
    while the worst programmers believed they were so good that their work did not need
    reviewing. (Daniel Freedman and Gerald Weinberg)

..

    In addition to feedback about how well they follow standards, programmers need
    feedback about more subjective aspects of programming: formatting, comments,
    variable names, local and global variable use, design approaches, the-way-we-do-
    things-around-here, and so on. Programmers who are still wet behind the ears need
    guidance from those who are more knowledgeable, and more knowledgeable
    programmers who tend to be busy need to be encouraged to spend time sharing what
    they know. Reviews create a venue for more experienced and less experienced
    programmers to communicate about technical issues. As such, reviews are an
    opportunity for cultivating quality improvements in the future as much as in the present.

    One team that used formal inspections reported that inspections quickly brought all the
    developers up to the level of the best developers (Tackett and Van Doren 1999).
    («Code Complete» [#fncodec]_)

..

    Collective Ownership Applies to All Forms of Collaborative Construction

    With collective ownership, all code is owned by the group rather than by individuals
    and can be accessed and modified by various members of the group. This produces
    several valuable benefits:

    - Better code quality arises from multiple sets of eyes seeing the code and multiple programmers working on the code.
    - The impact of someone leaving the project is lessened because multiple people are familiar with each section of code.
    - Defect-correction cycles are shorter overall because any of several programmers can potentially be assigned to fix bugs on an as-available basis.

    Some methodologies, such as Extreme Programming, recommend formally pairing
    programmers and rotating their work assignments over time. At my company, we've
    found that programmers don't need to pair up formally to achieve good code coverage.
    Over time we achieve cross-coverage through a combination of formal and informal
    technical reviews, pair programming when needed, and rotation of defectcorrection
    assignments.
    («Code Complete» [#fncodec]_)

..

    Pair programming produces numerous benefits:

    - It holds up better under stress than solo development. Pairs encourage each other to keep code quality high even when there's pressure to write quick and dirty code.
    - It improves code quality. The readability and understandability of the code tends to rise to the level of the best programmer on the team.
    - It shortens schedules. Pairs tend to write code faster and with fewer errors. The project team spends less time at the end of the project correcting defects.
    - It produces all the other general benefits of collaborative construction, including disseminating corporate culture, mentoring junior programmers, and fostering collective ownership.

    («Code Complete» [#fncodec]_)

..

    Pair programming typically costs about the same as inspections and produces
    similar quality code. Pair programming is especially valuable when schedule
    reduction is desired. Some developers prefer working in pairs to working solo.
    («Code Complete» [#fncodec]_)

..

    In my experience, pair programming is more productive than dividing the work
    between two programmers and then integrating the results.
    (Kent Beck [#fnxp]_)

The main conclusion is that you can't say about affect of pair programming to velocity of development until you begin to track the time of your team for bugfixes, refactoring and debugging.

Please do not confuse "Inspection" [#fncodec]_ (or "Code Reading" [#fncodec]_) and usual Code Review on github.
Inspection is the kind of Collaborative Development Practice, while usual Code Review usually involves only 2 persons (reviewer and author).
Code Review is weak for experience sharing.
Also, usual Code Review does not require any preparation.

    90 percent of the defects were
    found in preparation for the review meeting, and only about 10
    percent were found during the review itself (Votta 1991, Glass
    1999).
    («Code Complete» [#fncodec]_)

There was one real example of my practice.
We had a ticket for 3 days of development had been assigned to the new developer.
It was a talented developer, but he had a lack of knowledges for the project.

- The new developer solved the ticket during 6 days, because he needed a time to understand the program.
- Then I spent 1-2 days for a few of Code Reviews with fixes.
- Eventually I understood that I spent a lot of time and I approved the incomplete pull request with a lot of design mistakes. Also product team insisted on merge the pull request even with bugs.
- After it, when I was developing my own ticket and I saw that this mistakes interfere to my implementation, I did the refactoring of the mistakes and spent about a day for refactoring.

Thus, we both spent 6 + 2 * 2 + 1 = 11 days.
If we used "Continued Review" of XP we would spent 3 * 2 = 6 days + growing the skills of the new developer.
Next time he would be able to solve the issue independently.


The fourth myth. Theory and practice are two different things.
--------------------------------------------------------------

There is an opinion that theory and practice are two different things.

In reality the theory is the research of the practice.
Do you want to solder own processor, or write own assembler to create own website?
You use the collective knowledges instead of it.
The life of a human is to short to reproduce the evolutional way of the IT-industry in isolation.
Code development is too complicated science today.
Several outstanding developers have dedicated their lives to collecting and systematizing collective knowledges.
They wrote books with the collectives knowledge for you.
Martin Fowler, Kent Beck, Robert Marting, Steve McConnel, Eric Evans, Mark Lutz, Erich Gamma, Niklaus Wirth, Donald Knuth, Christopher Date and others.
If a developer thinks he is able to obtain the experience himself, isolated from the collective knowledges, he looks like an odd man who wants to solder own processor for his web-site...))

There is 5 fundamental books which must be read by each professional:

1. «Design Patterns: Elements of Reusable Object-Oriented Software» Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides
#. «Patterns of Enterprise Application Architecture» Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford
#. «Refactoring: Improving the Design of Existing Code» Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts
#. «Clean Code: A Handbook of Agile Software Craftsmanship» Robert C. Martin
#. «Code Complete» Steve McConnell

I recommend to read the books in the given order.


The fifth myth. Quality code is perfectionism and excess of complicated design patterns.
----------------------------------------------------------------------------------------

Some people thinks that quality always has a lot of complicated design patterns and, therefore, it is too difficult.
Let me open, for example, motivation of the pattern Mediator.

    "Mediator promotes loose **coupling** by keeping objects from referring to each other explicitly,
    and it lets you vary their interaction independently."
    («Design Patterns: Elements of Reusable Object-Oriented Software» [#fndp]_)

The key word in the quote is the word "Coupling_".
The `low coupling and high cohesion <Coupling_>`__ is the most important criteria of code quality.
Low coupling reduces the complexity of the code.
It's simplification, not the complication.
It allows to limit the attention necessary to understand this responsibility of the code.
Thus, patterns is not complexity.

The quality code is always simple!

    "On the surface, being an XP programmer looks a lot like being a programmer within
    other software development disciplines. You spend your time working with programs,
    making them bigger, simpler, faster. Beneath the surface, however, the focus is
    quite different. Your job isn't over when the computer understands what to do. Your
    first value is communication with other people. If the program runs, but there is
    some vital component of communication left to be done, you aren't done. You write
    tests that demonstrate some vital aspect of the software. You break the program
    into more smaller pieces, or merge pieces that are too small into larger, more
    coherent pieces. You find a system of names that more accurately reflects your
    intent.

    This may sound like a high-minded pursuit of perfection. It is anything but. You try
    to develop the most valuable software for the customer, but not to develop anything
    that isn't valuable. If you can reduce the size of the problem enough, then you can
    afford to be careful with the work you do on what remains. Then, you are careful by
    habit."
    (Kent Beck [#fnxp]_)

..

    "Of course, you can
    do a better job if you have more tools in your toolbox than if you have fewer, but it
    is much more important to have a handful of tools that you know when not to use,
    than to know everything about everything and risk using too much solution."
    (Kent Beck [#fnxp]_)

..

    "It doesn't take a Ph.D. in computer science to contribute to an XP project (in fact, the Ph.D.'s sometimes have the most trouble)."
    (Kent Beck [#fnxp]_)

..

    "It's hard to do simple things. It seems crazy, but sometimes it is easier to do 
    something more complicated than to do something simple. This is particularly true 
    when you have been successful doing the complicated thing in the past. Learning to 
    see the world in the simplest possible terms is a skill and a challenge. The challenge 
    is that you may have to change your value system. Instead of being impressed when 
    someone (like you, for instance) gets something complicated to work, you have to 
    learn to be dissatisfied with complexity, not to rest until you can't imagine anything 
    simpler working."
    (Kent Beck [#fnxp]_)

..

    "I like my code to be elegant and efficient.
    The logic should be straightforward to make it hard for bugs to hide,
    the dependencies minimal to ease maintenance, error handling complete according to an articulated strategy,
    and performance close to optimal so as not to tempt people to make the code messy with unprincipled optimizations.
    Clean code does one thing well."
    (Bjarne Stroustrup, inventor of C++ and author of The C++ Programming Language.)

..

    "The design goal for Eventlet’s API is simplicity and readability.
    You should be able to read its code and understand what it’s doing.
    Fewer lines of code are preferred over excessively clever implementations."
    (`Eventlet’s docs <http://eventlet.net/doc/basic_usage.html>`__)

..

    "Simplicity and elegance are unpopular because they require hard work and discipline to achieve and education to be appreciated."
    (Edsger W. Dijkstra)

..

    "Simplicity is prerequisite for reliability."
    (Edsger W. Dijkstra)

..

    "Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it. And to make matters worse: complexity sells better."
    (Edsger W. Dijkstra, 1984 `On the nature of Computing Science <http://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD896.html>`__ (EWD896))

..

    "A little time spent refactoring can make the code better communicate its purpose. Programming in this mode is all about saying exactly what you mean."
    ("Refactoring: Improving the Design of Existing Code", Martin Fowler)


Advices
=======

Use catalog of refactorings
---------------------------

Don't spend a lot of time for explanations at code review.
You can simple use link to certain method of refactoring by using `Catalog of Refactorings`_.
Pay attention, each method of refactoring has the page number of the book «Refactoring: Improving the Design of Existing Code» [#fnrefactoring]_ by Martin Fowler, where any developer can find the comprehensive information for the method with examples.

..

    Change is the only constant. (Kent Beck [#fnxp]_)


Use catalogs of code smells
---------------------------

Do you want to avoid a war of opinions and save a lot of team's time?
Ground your arguments on knowledge, instead of opinion, when you do code review.
Use catalogs of Code Smells.
There is a few of most frequently used catalogs:

- Chapter 17: «Smells and Heuristics» of the book «Clean Code: A Handbook of Agile Software Craftsmanship» [#fnccode]_ Robert C. Martin
- Chapter 3. «Bad Smells in Code» of the book «Refactoring: Improving the Design of Existing Code» [#fnrefactoring]_ by Martin Fowler
- `Code Smell`_
- «Refactoring To Patterns» [#fnrtp]_

Use Designing Through Refactoring
---------------------------------

More info on approach of "Designing Through Refactoring" you can find in the chapter «Refactoring and Design» of the book «Refactoring: Improving the Design of Existing Code» [#fnrefactoring]_ by Martin Fowler.
This approach is unbelievable effective when you use Type Hinting declaration (more info `here <https://github.com/python-rope/rope/blob/master/docs/overview.rst#type-hinting>`__, `here <http://jedi.readthedocs.io/en/latest/docs/features.html#type-hinting>`__ and `here <https://www.jetbrains.com/help/pycharm/type-hinting-in-pycharm.html>`__) with a tool for automated refactoring (`rope <https://github.com/python-rope/rope>`_, `refactoring tool of PyCharm <https://www.jetbrains.com/help/pycharm/refactoring-source-code.html>`_).


Track and analyze the inefficient time spent
--------------------------------------------

There are several tools to track your time, for example:

- `rescuetime <https://www.rescuetime.com/>`_
- `timescreen <https://bitbucket.org/emacsway/timescreen>`_

I personally use `timescreen`_.

Track and analyze the inefficient time spent, and you will see how to save a lot of time.

=============================================================  ===============================================================================
Ineffective waste of time                                      The solution
=============================================================  ===============================================================================
You are forced to see and understand an implementation.        You don't have *to see* the implementation.
                                                               You don't have *to understand* the program, you have *to read* the program.
                                                               You have to read the *interface*, not the *implementation*.
                                                               If the interface is not clear, ask the author to improve it.
                                                               The declaration of public interfaces is important,
                                                               it's a great way to reduce the complexity of the program.
                                                               Code is written once, but it is read many times.
                                                               Make reading the code easy, save the time.

You are forced to understand the program using the debugger.   This violates the Primary Technical Imperative of
                                                               software development "Managing complexity".
                                                               Don't ask the author to improve the code quality, because he can't to do it.
                                                               Introduce a Collaborative Development Practice to share experience:
                                                               XP, Pair Programming, Formal Inspection, Code Reading (don't confuse it
                                                               with usual Code Review).
                                                               Ask some experienced developer to refactor the complicated part of code,
                                                               and share the solution with the author to improve his skills.
                                                               Remember the quotes:

                                                                   "The competent programmer is fully aware of the strictly limited size
                                                                   of his own skull; therefore, he approaches the programming task
                                                                   in full humility"
                                                                   (Dijkstra 1972).

                                                               ..

                                                                   "Be Humble, don’t think of yourself as a super genius,
                                                                   this is your first mistake.
                                                                   By being humble, you will eventually achieve super genius status =),
                                                                   and even if you don’t, who cares!
                                                                   your code is stupid simple,
                                                                   so you don’t have to be a genius to work with it."
                                                                   (`KISS principle <https://people.apache.org/~fhanik/kiss.html>`__)

You are forced to debug and to fix bugs.                       Introduce `Test-Driven Development`_ (TDD), improve the quality of code
                                                               and the corporate culture of code construction.
                                                               The time of debugging and bug fixing is one of the important
                                                               measurement parameters.
                                                               The main goal of TDD is saving the time.
                                                               Also TDD improves the code quality, because it is easier to write well
                                                               decomposed classes with low coupling and clear responsibility
                                                               than to be thinking how to test a tangled mishmash.

A lot of discussions in the team. A war of opinions.           A lot of discussions means the lack of the knowledges.
                                                               Where there is knowledge, there is not a lot of discussions,
                                                               and everyone knows what and how to do it.
                                                               Introduce using of a catalog of code smells, the catalog of refactorings,
                                                               the approach of "Designing Through Refactoring".
                                                               Introduce reading technical literature into corporate culture.

You can't implement a new feature without refactoring.         This is normal if you use the approach of "Designing Through Refactoring".
                                                               But if the cause is a lack of design skills,
                                                               you have to improve the skills of the team.
                                                               Introduce a Collaborative Development Practice to share experience.

=============================================================  ===============================================================================


Create motivation
-----------------

Many times I saw how talented developers lost motivation due to management mistakes and left the company.
Once I saw how the tight-knit collective with high self-motivation was destroyed for a couple of weeks after the change of the management.

    "Quality means doing it right when no one is looking." (Henry Ford)

..

    There is a human effect from quality. Everybody wants to do a good job, and they
    work much better if they feel they are doing good work. If you deliberately
    downgrade quality, your team might go faster at first, but soon the demoralization of
    producing crap will overwhelm any gains you temporarily made from not testing, or
    not reviewing, or not sticking to standards.
    (Kent Beck [#fnxp]_)

..

    This points to a deeper value, one that lies below the surface of the other four —
    respect. If members of a team don't care about each other and what they are doing,
    XP is doomed.
    (Kent Beck [#fnxp]_)

..

    If members of a team don't care about the project, nothing can
    save it. Given some minimal passion, XP provides some positive feedback. This is not
    manipulative; it's just enjoying being part of something that works, instead of part of
    something that doesn't work.
    (Kent Beck [#fnxp]_)


Be fair and honest
------------------

It worth to read chapter "33.4. Intellectual Honesty" of «Code Complete» [#fncodec]_.

    "Any fool can defend his or her mistakes—and most fools do." (Dale Carnegie)


Be courageous
-------------

It worth to read chapter "Chapter 7. Four Values: Courage" of «Extreme Programming Explained» [#fnxp]_.

..

    "programmers will have to wrestle with the messy real world." (Steve McConnel)


Keep improving yourself
-----------------------

One company asks the question to new candidates:

    "What have you learned in the last year and what would you like to learn next?"

Ask this question to yourself and everyone in the team.

    "Specific features of the technical environment change every 5 to 10 years.
    If you aren't curious enough to keep up with the changes,
    you might find yourself down at the old-programmers' home playing cards with T-Bone
    Rex and the Brontosaurus sisters."
    («Code Complete», Steve McConnell [#fncodec]_)

..

    "We become authorities and experts in the practical and scientific spheres
    by so many separate acts and hours of work.
    If a person keeps faithfully busy each hour of the working day,
    he can count on waking up some morning to find himself one of the competent
    ones of his generation."
    (William James [#fncodec]_)


Use Extreme Progrgramming (XP)
------------------------------

    "XP is a lightweight, efficient, low-risk, flexible, predictable, scientific, and fun way to develop software."
    (Kent Beck [#fnxp]_)

"`Extreme Programming Explained`_" by Kent Beck is one of the most valuable books I've ever read.


Further reading
===============

* "`Extreme Programming Explained`_" by Kent Beck
* "Planning Extreme Programming" by Kent Beck, Martin Fowler
* "Rapid Development: Taming Wild Software Schedules" by Steve McConnell
* "The Clean Coder" by Robert C. Martin
* "Code Complete" by Steve McConnell


.. rubric:: Footnotes

.. [#fnccode] «`Clean Code: A Handbook of Agile Software Craftsmanship`_» by `Robert C. Martin`_
.. [#fncodec] «`Code Complete`_» Steve McConnell
.. [#fnrefactoring] «`Refactoring: Improving the Design of Existing Code`_» by `Martin Fowler`_, Kent Beck, John Brant, William Opdyke, Don Roberts
.. [#fnrtp] «`Refactoring To Patterns`_» by Joshua Kerievsky
.. [#fnxp] «`Extreme Programming Explained`_» by Kent Beck
.. [#fndp] «Design Patterns: Elements of Reusable Object-Oriented Software» by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides


.. update:: 06 Nov, 2017


.. _Clean Code\: A Handbook of Agile Software Craftsmanship: http://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884
.. _Robert C. Martin: http://informit.com/martinseries
.. _Code Complete: http://www.informit.com/store/code-complete-9780735619678
.. _Steve McConnell: http://www.informit.com/authors/bio/754ffba3-b7b2-45ef-be37-3d9995e8e409
.. _Refactoring\: Improving the Design of Existing Code: https://martinfowler.com/books/refactoring.html
.. _Martin Fowler: https://martinfowler.com/aboutMe.html
.. _Refactoring To Patterns: http://martinfowler.com/books/r2p.html
.. _Extreme Programming Explained: http://www.informit.com/store/extreme-programming-explained-embrace-change-9780321278654
.. _Catalog of Refactorings: http://www.refactoring.com/catalog/
.. _Coupling: http://wiki.c2.com/?CouplingAndCohesion
.. _Cohesion: http://wiki.c2.com/?CouplingAndCohesion
.. _Code Smell: http://c2.com/cgi/wiki?CodeSmell
.. _Test-Driven Development: https://martinfowler.com/bliki/TestDrivenDevelopment.html
