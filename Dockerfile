FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY setup.py .

RUN pip install .

COPY . .

CMD ["python", "./check_availability.py"]