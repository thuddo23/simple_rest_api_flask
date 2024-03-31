FROM python:3.12
LABEL authors="thuandd"
EXPOSE 5000
WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install flask
CMD ["flask", "run", "--host", "0.0.0.0"]