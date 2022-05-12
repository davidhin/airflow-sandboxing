# Airflow Sandboxing

Written for Airflow 2.3.0, for the purpose of learning.

## Getting Started

### Docker development

Airflow can be run locally or thorugh Docker. Here, I have set it up for both scenarios. To run through Docker, just run `docker-compose up`, and it will be accessible through localhost:8080.

### Local development

If running locally (for development, debugging, or testing purposes), we can initialize an appropriate conda environment with `mamba env create -f environment.yml --force` (mamba is optional, can use conda instead). Also, have to change the `AIRFLOW_HOME` env var in to the local directory. Then, run `airflow db init` to start the database. We also need to add the `plugins` folder to the pythonpath if we are using an interactive python session. In conda, we can to `conda develop plugins` (alternatively, can add it to pythonpath as shown in the `.env`) Now, it should be set up properly for local development and testing.

## Testing

WIP