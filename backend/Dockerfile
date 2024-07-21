#
FROM python:3.10

#
WORKDIR /code/backend

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app ./app

#
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--reload"]
