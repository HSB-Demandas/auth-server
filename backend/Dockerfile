FROM python:3.12.4-slim-bullseye AS base

# Celery does not work with root unless you force it
ENV C_FORCE_ROOT true

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

LABEL app.project.image.name="dashboard-platform-base"

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
        apt-utils \
        build-essential \
        nano \
        curl \
        netcat \
        inetutils-ping \
        libpcre3 \
        libtiff5-dev \
        zlib1g-dev \
        libpcre3 \
        libpcre3-dev \
        libjpeg62 \
        libjpeg62-turbo-dev \
        libfreetype6-dev \
        libwebp-dev \
        liblcms2-dev \
        libxml2-dev \
        libxslt-dev \
        python-dev \
        postgresql-client \
        gettext \
        dos2unix \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-mark hold python2 python2-minimal python2.7 python2.7-minimal libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# -----------------------------------------------------------------------------
FROM base AS builder

RUN set -ex \
    && pip3 install -I -U pip setuptools poetry==1.8

WORKDIR /code/app

COPY ./pyproject.toml /code/.
COPY ./poetry.lock /code/.

# Prepare dependencies
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN cd /tmp && poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN set -ex \
    && pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt \
    && rm -rf /root/.cache/pip/*

# -----------------------------------------------------------------------------
FROM builder AS development

LABEL app.project.image.name="dashboard-platform-dev"

RUN set -ex \
    && RUN_DEPS=" \
        graphviz \
        graphviz-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# -----------------------------------------------------------------------------
FROM builder AS release

RUN set -ex \
    && pip3 install -U gunicorn==20.1.0 \
    && rm -rf /root/.cache/pip/*

ENV PORT=8000

#ARG USERNAME=docker
#ARG UID=123
#ARG GID=4567
#
#RUN addgroup --gid ${GID} ${USERNAME}
#RUN useradd -ms /bin/bash ${UID} --uid ${UID} --home /home/${USERNAME}
#RUN usermod -a -G ${GID} ${UID}
#RUN chown -R ${UID}:${GID} /code
#
#USER ${UID}
# Copy and prepare entrypoint script with explicit handling for ECS compatibility
COPY conf/docker/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    sed -i 's/\r$//' /entrypoint.sh && \
    cat /entrypoint.sh

COPY . /code/app/

CMD exec gunicorn --bind 0.0.0.0:$PORT --log-file=- --workers 5 --threads 8 --log-level INFO project.wsgi:application
ENTRYPOINT ["/entrypoint.sh"]
# -----------------------------------------------------------------------------
FROM release AS staging

LABEL app.project.image.name="dashboard-platform-staging"

# -----------------------------------------------------------------------------
FROM release AS production

ENV DEBUG=false

LABEL app.project.image.name="dashboard-platform-production"