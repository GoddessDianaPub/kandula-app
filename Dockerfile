FROM python:3.9-slim

RUN mkdir /kandula
WORKDIR /kandula
COPY . /kandula/

RUN pip install --upgrade pip
#Run pip install psycopg2
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python" , "run.py"]
