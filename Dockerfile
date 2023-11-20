FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py
COPY ./entrypoint.sh /code/entrypoint.sh

# Expose the specified port
ARG PORT
ENV PORT=${PORT}

ARG REGION
ENV REGION=${REGION}

RUN ["chmod", "+x", "./entrypoint.sh"]

# Set the entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]
