FROM python:3.9

ENV FLASK_APP=gene_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

WORKDIR /app

# Install specific version of Werkzeug
RUN pip install Werkzeug==2.0.2

# Install Flask
RUN pip install Flask==3.0.2

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
