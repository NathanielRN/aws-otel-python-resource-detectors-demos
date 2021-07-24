FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV HOME=/

ENV OTEL_RESOURCE_ATTRIBUTES='service.name=eks-sample-resource-detectors-app'

CMD python application.py
