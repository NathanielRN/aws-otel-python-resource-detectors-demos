FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV HOME=/

ENV OTEL_RESOURCE_ATTRIBUTES='service.name=ecs-sample-app'

EXPOSE 5000

CMD python application.py
