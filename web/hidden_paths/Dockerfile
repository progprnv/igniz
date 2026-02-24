FROM python:3.11

WORKDIR /usr/src/app

COPY app ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

ENV FLAG="IGNIZ{s0urc3_c0d3_r3v34l3d_s3cr3ts}"

EXPOSE 8080
RUN useradd slashslash
CMD su slashslash -c "gunicorn -w 4 -b 0.0.0.0:8080 application:app"
