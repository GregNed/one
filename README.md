Run locally: pip install -r requirements.txt && fastapi dev main.py

To get all the points with a specified radius from a specific POI: 
http://localhost:8000/within/?poi_name=Rothschild%20Boulevard&radius=300

To get all the points: http://localhost:8000/all/


To explore the data, run pip install jupyterlab && jupyter lab .