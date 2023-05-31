FROM tensorflow/tensorflow

WORKDIR /home

RUN apt-get update && apt-get install -y python3-pip graphviz

RUN pip install --upgrade pip

COPY requirements.txt /home/requirements.txt

RUN pip3 install -r requirements.txt
