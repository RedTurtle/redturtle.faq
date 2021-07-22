.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/redturtle.faq.svg
    :target: https://pypi.python.org/pypi/redturtle.faq/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/redturtle.faq.svg
    :target: https://pypi.python.org/pypi/redturtle.faq
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/redturtle.faq.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/redturtle.faq.svg
    :target: https://pypi.python.org/pypi/redturtle.faq/
    :alt: License


=============
RedTurtle Faq
=============

Add two new content-types to manage Faqs:

- FaqFolder
- Faq

This product is intended to be a Volto extension, so it only provides the content-types (no custom views or styles).

Faq content-type has **blocks** enabled.


Expandable component
--------------------

FaqFolders have an additional expandable component (@faq-structure) that will return the complete structure of the current context with sub-FaqFolders and Faqs::

    > curl -i http://localhost:8080/Plone/example-folder/@faq-structure -H 'Accept: application/json'


You can also filter faqs querying with **SearchableText** index::

    > curl -i http://localhost:8080/Plone/example-folder/@faq-structure?SearchableText=foo -H 'Accept: application/json'


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install redturtle.faq by adding it to your buildout::

    [buildout]

    ...

    eggs =
        redturtle.faq


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.faq/issues
- Source Code: https://github.com/RedTurtle/redturtle.faq


License
-------

The project is licensed under the GPLv2.
