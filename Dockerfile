FROM python:3.9-slim #as build

RUN mkdir /kandula
WORKDIR /kandula
COPY . /kandula/

RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run vulnerability scan on build image
#FROM build AS vulnscan
#COPY --from=aquasec/trivy /usr/local/bin/trivy /usr/local/bin/trivy
#RUN trivy rootfs --no-progress /

CMD ["python", "run.py"]
