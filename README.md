## Nomic Challenge

This is my solution to the coding challenge for an interview at Nomic.
This repo contains a single Django application that implements queries on Plate data.
Please see the following sections for deploy and usage information.

### 1. Build and Deploy

This application is completely dockerized. You can build the necessary images by navigating
to the `deploy` folder and using `docker compose`:

```
cd deploy
docker compose build
```

Environmental variables, including `AWS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`, are provided with a `.env` file.
Please copy the template and fill in the necessary information before deploying with docker compose.

```
cp .env.template .env
vim .env              # Fill in AWS variables
docker compose up -d
```

The compose file includes instructions for the application container to 1, apply migrations, and 2, start the development server,
so hopefully things should just work. You can navigate to `http://localhost:8000/api/plates/` in a browser to see an empty list of plates.
In the next section, we will fill this in.

### 2. Database initialization and basic usage

I have provided an initialization script as a django management command. You can populate the database using:

```
docker compose run --rm app python3 manage.py initplates
```

Once populated, data for Bead Plates, Runs, and Plates should be in the database. The Django Rest Framework has a nice browser
interface for looking at these lists so please feel free to navigate to the following urls in the browser:

- Bead Plates: `http://localhost:8000/api/bead_plates/`
- Runs: `http://localhost:8000/api/runs/`
- Plates: `http://localhost:8000/api/plates/`

You can of course do something similary with the python `requests` library if you want to try stuff out in Jupyter:

```
import requests
from pprint import pprint

response = requests.get("http://localhost:8000/api/runs/")
pprint(
    response.json()
)
```

Each of the above endpoints returns a data package with the following schema:

```
{
    "count": int,
    "data": List[Dict]
}
```

You may toggle the return of data using the `return_data=false` query parameter on each url:

```
# In browser
http://localhost:8000/api/plates/?return_data=false

# In python
requests.get("http://localhost:8000/api/runs/", params={"return_data": "false"})
```

### 3. Performing plate queries

A major aspect of this assignment was performing more specific queries on plates.
This can be accomplished by passing query parameters to the '/api/plates/` endpoint.

For example, in order to get the plates between certain date ranges, you may pass the `run_date_gt` and `run_date_lt` params:

```
http://localhost:8000/api/plates/?run_date_lt=2023-11-01T00:00:00.00Z&run_date_gt=2023-09-01T00:00:00.00Z
```

If you want to find the plates with more than X occurences of beads bellow a Y threshold, use the `bead_count_threshold` and `occurence_threshold` params.
The following finds any plates with bead counts below 5 in the date range from the previous query:

```
http://localhost:8000/api/plates/?run_date_lt=2023-11-01T00:00:00.00Z&run_date_gt=2023-09-01T00:00:00.00Z&bead_count_threshold=5&occurence_threshold=0
```

You can generate a month by month count report by performing a get operation on the following URL.
Internally, this is implemented as a propper SQL query, so it should be rather performant.

```
http://localhost:8000/api/plates/report/
```

A special case of plate based queries arises for calimetrics. A basic query for a list of calimetrics can be performed with:

```
http://localhost:8000/api/plates/report/
```

You can add the `return_discrepency=true` query parameter to just look for metrics that differ by at least 2:

```
http://localhost:8000/api/calimetrics/?return_discrepency=true
```

### 4. Creating Analysis Results

If you want to wrap serveral plates together, you can create analysis results objects. I usually do these POST requests via python.
Currently, the POST request will take the database IDs as input. Let's wrap up plate 3 and 4 with the cali plate 2.

```
import requests

response = requests.post(
    "http://localhost:8000/api/analysis_results/",
    data = {
        "cali_plate": 2,
        "sample_plates": [3, 4]
    }
)
response.json()
```

You can then download this data using a get request:

```
response = requests.get("http://localhost:8000/api/analysis_results/1")
data = response.json()
```

The data object has the schema:

```
{
    "data": {
        "cali_plate": Dict[Dict]
        "sample_plates": Dict[Dict]
    }
} 
```

Each of `cali_plate` and `sample_plates` were exported directly from dataframes and thus can be put right back into one:

```
import pandas as pd

df = pd.DataFrame(data["data"]["cali_plate"])
```
