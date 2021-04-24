#slim is an official python runtime (base image)
FROM python:3.9.1-slim

#Installing operating system requirements
#RUN apt-get update && apt install build-essential libssl-dev libffi-dev python3-dev

WORKDIR /CLIENT

COPY . ./

#RUN pip install --trusted-host pypi.python.org -r requirements.txt

#runs setup.py #install itself
RUN pip install .
 
RUN chmod +x ./run_client.sh

ENTRYPOINT ["sh","./run_client.sh"]
