FROM alpine:latest

WORKDIR /app/

ADD ./requirements.txt .

RUN apk add --no-cache ca-certificates && update-ca-certificates
RUN apk add --update --no-cache python3
RUN apk add --update --no-cache postgresql-dev
RUN apk add --no-cache --virtual=build-dependencies wget ca-certificates build-base python3-dev musl-dev
RUN wget --no-check-certificate "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python3

RUN echo "http://dl-3.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update

# Закоментил в связи с ошибкой возникаемой на данном этапе:
# Может быть связано с проблемами данной версии alpine.
# В будущем нужно будет убрать комментарий и проверить.
# Версия alpine на данный момент: 3.6, latest (versions/library-3.6/x86_64/Dockerfile).
#
#ERROR: unsatisfiable constraints:
#  /bin/sh (virtual):
#    provided by: busybox
#    required by:
#                 ca-certificates-20171114-r0[/bin/sh]
#                 alpine-baselayout-3.0.5-r2[/bin/sh]
#                 alpine-baselayout-3.0.5-r2[/bin/sh]
#                 ca-certificates-20171114-r0[/bin/sh]
#                 ca-certificates-20171114-r0[/bin/sh]
#The command '/bin/sh -c apk upgrade --update-cache --available' returned a non-zero code: 4
#
# RUN apk upgrade --update-cache --available

RUN apk add --update --no-cache libmagic jpeg-dev zlib-dev \
    freetds freetds-dev unixodbc unixodbc-dev libstdc++

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn meinheld
# RUN apk del build-dependencies

ADD . .

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=smm_tools.settings_prod
ENV DB_NAME=smm_tools
ENV DB_USER=smm_tools
ENV DB_PASSWORD=QwKu59GxwV9Iq1JC
ENV DB_HOST=postgres

