FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "starter.py", "./" ]

RUN pipenv install --system --deploy

ENTRYPOINT [ "python", "batch.py" ]