FROM python:3.9-slim

RUN mkdir /kandula

COPY . /kandula/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python" , "run.py"]
