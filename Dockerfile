FROM python:3.9-slim

RUN mkdir /kandula
WORKDIR /kandula
COPY . /kandula/

RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python" , "run.py"]
