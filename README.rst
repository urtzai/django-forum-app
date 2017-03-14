Django-forum-app
================
|Travis| |Python27| |Python35| |PyPi|

.. |Travis| image:: https://api.travis-ci.org/urtzai/django-forum-app.svg?branch=master
.. _Travis: https://travis-ci.org/urtzai/django-forum-app

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. _Python27: https://badge.fury.io/py/django-forum-app

.. |Python35| image:: https://img.shields.io/badge/python-3.5-blue.svg
.. _Python35: https://badge.fury.io/py/django-forum-app

.. |PyPi| image:: https://badge.fury.io/py/django-forum-app.svg
.. _PyPi: https://badge.fury.io/py/django-forum-app

A very simple/minimalistic Django Forum app based on yoanisgil's `Django simple forum <https://github.com/yoanisgil/django-simple-forum>`_ project.


Dependencies
------------
- Django >= 1.8
- django-photologue >= 3.6
- django-tinymce >= 2.6.0

Installation
------------
Clone this repository and add it to your ``INSTALLED_APPS`` list:

.. code-block:: python

    INSTALLED_APPS = [
        'django_forum_app',
    ]

Then run migrations:

.. code-block::

    ./manage.py migrate django_forums_app

Finally, add this in ``urls.py``:

.. code-block:: django

    url(r'^forum/', include('django_forum_app.urls')),

Settings
--------
Ther are some option you could overrite to change the default behaviour of the forum:

``FORUM_SUBJECT``
    Subject for email notifications

    **Default:** ``FORUM``

``POSTS_PER_PAGE``
    Number of posts shown per page.

    **Default:** ``10``

``DJANGO_FORUM_APP_FILTER_PROFANE_WORDS``
    Attribute to filter profane words. Values should be *True*/*False*

    **Default:** ``True``

``TINYMCE_DEFAULT_CONFIG``
    Overriding this option you can change the tinymce editor behaviour.

    **Default:**

    .. code-block:: python

        TINYMCE_DEFAULT_CONFIG = {
            'language': 'en',
            'theme': 'modern',
            'height': 600,
            'plugins': [
                'advlist autolink lists link image charmap print preview anchor',
                'searchreplace visualblocks code fullscreen',
                'insertdatetime media table contextmenu paste',
            ],
            'toolbar': 'styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview',
            'menubar': False,
            'media_alt_source': False,
            'media_poster': False,
            'media_dimensions': False,
        }

Support
-------
Should you experience any issues do not hesistate to post an issue or contribute in this project pulling requests.

Travis CI status
----------------
We use Travis to check that the unit test suite is working against various combinations of Python, Django, etc...
`Click here for the full report <http://travis-ci.org/#!/urtzai/django-forum-app>`_.
