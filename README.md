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
