#slim is an official python runtime
FROM python:3.9.1-slim

#Installing operating system requirements
#RUN apt-get update && apt install build-essential libssl-dev libffi-dev python3-dev

WORKDIR /SERVER

COPY . ./

#RUN pip install --trusted-host pypi.python.org -r requirements.txt

#runs setup.py // installs itself
RUN pip install .
 
RUN chmod +x ./run_server.sh

ENTRYPOINT ["sh","./run_server.sh"]

