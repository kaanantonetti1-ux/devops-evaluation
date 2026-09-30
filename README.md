# DevOps Evaluation

This project was created for the DevOps evaluation.

The goal of the project is to build a complete pipeline from the application code to a Docker image, then deploy this image automatically after the CI pipeline succeeds.

The application is a small Flask API using Redis. It also exposes Prometheus metrics.

## Project structure

```text
devops-evaluation/
│
├── .github/
│   ├── actions/
│   │   └── setup-python/
│   │       └── action.yml
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── prometheus/
│   └── alerts.yml
│
├── tests/
│   └── test_app.py
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
├── .gitignore
├── .gitattributes
├── .yamllint.yml
└── README.md