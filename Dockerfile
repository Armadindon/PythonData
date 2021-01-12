FROM tiangolo/meinheld-gunicorn:python3.8

COPY . /app/

RUN pip install -r /app/requirements.txt
RUN cd /app && python install.py