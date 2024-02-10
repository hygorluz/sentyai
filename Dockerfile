FROM python:3.11-slim

ENV PATH="/home/service/.local/bin:${PATH}"

RUN groupadd -g 1001 service && \
    useradd -rm -d /home/service -s /bin/bash -g service -u 1001 service

RUN apt-get update && \
    apt-get install -y gcc make && \
    rm -rf /var/lib/apt/lists/*

USER service

WORKDIR /home/service/app

COPY --chown=service:service requirements.txt ./
RUN pip install --user --retries 5 --default-timeout=120 --prefer-binary --no-cache -r requirements.txt

COPY --chown=service:service . ./
RUN chmod +x ./*.sh

EXPOSE 8080

VOLUME [ "/home/service/app" ]

CMD ["gunicorn"  , "--bind", "0.0.0.0:8080","-k","uvicorn.workers.UvicornWorker","--timeout","180" , "service.application:create_application()"]
