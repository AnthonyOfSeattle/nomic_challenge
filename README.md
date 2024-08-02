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

You may toggle the return of data using the `return_data=false` query parameter:

```
# In browser
http://localhost:8000/api/plates/?return_data=false

# In python
requests.get("http://localhost:8000/api/runs/", params={"return_data": "false"})
```
