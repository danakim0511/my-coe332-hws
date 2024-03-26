FROM python:3.9

ENV FLASK_APP=gene_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

WORKDIR /app

# Install specific versions of required packages
RUN pip install Werkzeug==3.0.0 \
    Flask==3.0.2 \
    requests==2.26.0 \
    redis==4.0.2

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
