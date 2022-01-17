FROM python:3.9.9-slim-bullseye
COPY . /mumble/.
WORKDIR /mumble
RUN apt-get update && apt-get install -y libssl-dev python3-pip python3.9-dev libbz2-dev build-essential && pip3 install -r requirements.txt
EXPOSE 21803
CMD ["hypercorn","mumble-fastapi:app", "--bind", "0.0.0.0:21803"]
