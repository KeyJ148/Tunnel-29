FROM python:3

EXPOSE 8080
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install libcairo2 libcairo2-dev

COPY *.py ./

CMD [ "python", "-u", "./tunnel29.py" ]