FROM python:3.9-slim

RUN mkdir /kandula

COPY . /kandula/

CMD ["python" , "run.py"]
