FROM python:3.9.2-buster

RUN apt update

COPY . /root/oci-emulator

WORKDIR /root/oci-emulator

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/usr/local/bin/python", "oci_emulator.py"]
