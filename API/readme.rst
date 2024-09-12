1. With terminal navigate to the root of this repository
--------------------------------------------------------

2. Build docker image
---------------------
.. code-block::

    docker build -t suggestion-api-test-2 .

3. Run container
----------------
.. code-block::

    docker run --name suggestion-api-test-2-container -p 8000:8000 suggestion-api-test-2

4. Output will contain
----------------------
INFO:     Uvicorn running on http://0.0.0.0:8000

Use this url in chrome to see the model frontend;
use http://0.0.0.0:8000/docs for testing the model in the web interface.

5. Query model
--------------
    
 #. Via web interface (chrome):
        http://0.0.0.0:8000/docs -> test model