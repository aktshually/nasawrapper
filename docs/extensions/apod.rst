.. currentmodule:: nasawrapper.apod

APOD
====
One of the open APIs provided by NASA. A good example of what this API can do is the `Astronomy Picture of the Day website <https://apod.nasa.gov/apod/astropix.html>`_, wich gives you a new image/photograph of the universe every day. 
Also, each image has a brief explanation written by a professional astronomer, acording to the website.
I know, this is amazing.


SyncApod
----------------
.. autoclass:: SyncApod
    :members: get_apod, get_random, get_today_apod


AsyncApod
----------------
.. autoclass:: AsyncApod
    :members: get_apod, get_random, get_today_apod


ApodQueryBuilder
----------------
.. autoclass:: ApodQueryBuilder
    :members: set_date, set_start_date, set_end_date, set_count, set_thumbs