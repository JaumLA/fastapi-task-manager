FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./taskmanagementapi /code/taskmanagementapi

CMD ["fastapi", "dev", "taskmanagementapi/main.py", "--host", "0.0.0.0", "--port", "8000"]
