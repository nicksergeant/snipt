FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    python \
    python-dev \
    python-setuptools \
    git-core \
    mercurial \
    libxml2-dev \
    libxslt-dev \
    libpq-dev
RUN easy_install pip
COPY . /app/snipt
RUN pip install -r /app/snipt/requirements.txt
RUN pip install --index-url https://code.stripe.com --upgrade stripe
ADD .docker/run.sh /docker-run
RUN mkdir -p /tmp/app
WORKDIR /app/snipt
EXPOSE 8000
CMD ["/docker-run"]
