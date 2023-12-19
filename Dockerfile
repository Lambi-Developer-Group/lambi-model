# syntax=docker=dockerfile:1

FROM python:3.9.2

# Specified to Workdir
WORKDIR /lambi 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Set to your PORT
EXPOSE 8080

COPY . .

# CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD [ "export", "PORT=8080"]
CMD [ "gunicorn", "-b", ":8080", "main:app"]