
.. emacsway post example, created by `ablog start` on Oct 09, 2015.

.. post:: Oct 09, 2015
   :language: ru
   :tags: Emacs, Dependency Injection, Autocomplete, Python
   :author: Ivan Zakrevsky


Emacs autocomplete and Dependency injection (DI)
================================================

В пассивных классах, которым `зависимости внедряет <http://www.martinfowler.com/articles/injection.html>`__ программа, возникают трудности с автокомплитом в `emacs <https://www.gnu.org/software/emacs/>`__ с `elpy-mode <https://github.com/jorgenschaefer/elpy>`__.

Вариантов решения здесь несколько.

#. Устанавливать зависимости через конструктор класса, учитывая, что бэкенд `jedi <https://github.com/davidhalter/jedi>`__ учитывает `типы аргументов функций и возвращаемых значений <http://jedi.jedidjah.ch/en/latest/docs/features.html#type-hinting>`__, указанных в строках документирования.
#. Устанавливать зависимость через метод установки (setter). Причем, не обязательно, чтобы этот метод использовался, достаточно просто объявить его в классе и прописать в строке документирования тип аргумента.
#. Получать зависимость через метод доступа (getter). В отличии от первых двух вариантов, работать будет декларация типов возвращаемых значений, а не аргументов.
#. Использовать `Service Locator <http://www.martinfowler.com/articles/injection.html>`__ или паттерн `Plugin <http://martinfowler.com/eaaCatalog/plugin.html>`__, которые инициируют запрос и делегируют его исполнение резольверу зависимостей.

В случае с `rope <https://github.com/python-rope/rope>`__ вместо декларации типов аргументов в строках документирования можно использовать `Dynamic Object Analysis <https://github.com/python-rope/rope/blob/master/docs/overview.rst#dynamic-object-analysis>`__.

Но мы пойдем самым сложным путем, и заставим emacs решать эту проблему.

Итак.

\1. Стартуем интерпретатор ``M-x run-python`` (предварительно настраиваем elpy на использование ipython чтобы автокомплит работал и в шеле тоже)::

    (when (executable-find "ipython") (elpy-use-ipython))

\2. посылаем в интерпретатор файл с которым работаем: ``M-x python-shell-send-file``.

\3. определяем в интерпретаторе переменную, которая нужна. В моем случае нужна ``self.dao.engine``. Делаем в шелле что-то типа
``self = StatsFactory().make_api()``
у которого по счастливому стечению обстоятельств есть атрибут .dao.engine, который мне и нужен.

В итоге в интерпретаторе будет объявлена переменная ``self.dao.engine``.

\4. Поскольку `elpy заглушает вызов completion-at-point <https://github.com/jorgenschaefer/elpy/blob/3e7e08d14998063ce254cd1934786e7e212b99e3/elpy.el#L3101>`__ в выпадающем окне company-mode, вызываем вручную ``M-x completion-at-point`` или ``M-x python-shell-completion-complete-or-indent``.

Чтобы не вызывать вручную, биндим их на любую удобную комбинацию клавиш, например "``C-c TAB``".

\5. Таким образом можно автокомплитить любые недостающие переменные, - просто объявляем их в интерпретаторе, и они будут подсказываться в буфере редактирования файла.

P.S.: это старейшая возможность питон-мода, которая лего забывается из-за наличия jedi и rope)) `IDLE <https://docs.python.org/3/library/idle.html>`__ работает по аналогичному принципу.

P.P.S.: ropemacs-mode должен быть выключен, если он установлен. Можно не выключать, а просто снять ``'ropemacs-completion-at-point`` с ``'ropemacs-mode-hook``:

.. code-block:: elisp

    (add-hook 'ropemacs-mode-hook (lambda ()
      (if ropemacs-mode
          (remove-hook 'completion-at-point-functions 'ropemacs-completion-at-point t))
    ))


.. update:: Jan 03, 2016

   Добавил в `forked rope <https://github.com/emacsway/rope/tree/type-hinting>`__ поддержку `подсказок типов <https://github.com/emacsway/rope/blob/type-hinting/docs/overview.rst#type-hinting>`__  в строках документирования для параметров функций, возвращаемого значения и атрибутов класса.


.. update:: Jan 05, 2016

   Добавил в `forked rope <https://github.com/emacsway/rope/tree/type-hinting>`__ поддержку `подсказок типов <https://github.com/emacsway/rope/blob/type-hinting/docs/overview.rst#type-hinting>`__ на основании комментирования типов согласно `PEP 0484 <https://www.python.org/dev/peps/pep-0484/#type-comments>`__ для присваиваний.


.. update:: Feb 16, 2016

   Форк принят в мастер (`bd89775 <https://github.com/python-rope/rope/commit/d2496d25a1301dfc17e2173683e45d44c013c290>`__).

.. update:: Nov 29, 2016

   Реализация Type Hinting существенно `переработана <https://github.com/python-rope/rope/tree/master/rope/base/oi/type_hinting>`__.
