FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y &&\
    apt-get install -y python3 \
		       python3-pip \
		       python3-matplotlib \
		       tzdata

RUN ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN pip3 install pytest==8.0.0

WORKDIR /code
COPY ml_data_analysis.py /code/ml_data_analysis.py
COPY great_circle_distance.py /code/great_circle_distance.py

RUN chmod +x /code/ml_data_analysis.py
ENV PATH=/code:$PATH

CMD ["python3", "/code/ml_data_analysis.py", "/data/Meteorite_Landings.json"]
