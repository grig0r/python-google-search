python-google-search
======
Simple google search client library. Google version of [python-duckduckgo-search](https://github.com/grig0r/python-duckduckgo-search)

Dependencies
----
- beautifulsoup4 (https://www.crummy.com/software/BeautifulSoup/)
- requests (https://github.com/kennethreitz/requests)

Installation
----

.. code-block:: bash

  python setup.py install

one-liner

.. code-block:: bash

  git clone https://github.com/grig0r/python-google-search && cd python-google-search/ && python setup.py install

Usage
----

.. code-block:: pycon

  >>> import gclient

create search instance

.. code-block:: pycon

  >>> search = gclient.Search('perl language')

get list of result objects

.. code-block:: pycon

  >>> results = search.results(20)
  >>> results
  [<Result: The Perl Programming Language - www.perl.org (https://www.perl.org/)>,
   <Result: Perl – Wikipedia, wolna encyklopedia (https://pl.wikipedia.org/wiki/Perl)>,
   <Result: Perl - Wikipedia (https://en.wikipedia.org/wiki/Perl)>,
  [...]

get attributes from result object

.. code-block:: pycon

  >>> first_result = results[0]
  >>> first_result.title
  'The Perl Programming Language - www.perl.org'
  >>> first_result.url
  'https://www.perl.org/'
  >>> first_result.description
  'The Perl Programming Language at Perl.org. Links and other helpful resources for new and experienced Perl programmers.'
