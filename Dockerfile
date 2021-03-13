FROM python:3.9.2-buster

COPY . /root/oci-emulator

RUN apt update

WORKDIR /root/oci-emulator

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/usr/local/bin/python", "oci_emulator.py"]
