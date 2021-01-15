FROM python:3.8

COPY . /app/

WORKDIR /app
RUN pip install -r requirements.txt
RUN python install.py

RUN chmod +x ./start_server.sh

ENTRYPOINT ["./start_server.sh"]