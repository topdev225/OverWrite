FROM python:3.6-alpine

# Sources
RUN mkdir -p /app

COPY ./requirements.txt /app/
WORKDIR /app

RUN apk add --update bash linux-headers musl-dev postgresql-dev postgresql-client gcc zlib-dev jpeg-dev

#RUN apk update
#RUN apk --no-cache add curl
## Install wkhtmltopdf
#RUN curl -L#o wk.tar.xz https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz \
#    && tar xf wk.tar.xz \
#    && cp wkhtmltox/bin/wkhtmltopdf /usr/bin \
#    && cp wkhtmltox/bin/wkhtmltoimage /usr/bin \
#    && rm wk.tar.xz \
#    && rm -r wkhtmltox

RUN pip install -U pip
RUN pip install numpy
RUN pip install -r requirements.txt
