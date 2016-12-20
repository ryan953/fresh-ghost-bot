FROM python:2.7
ADD requirements.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt
ADD . /fresh-ghost-bot
WORKDIR /fresh-ghost-bot
EXPOSE 5000
CMD ["make", "test"]
