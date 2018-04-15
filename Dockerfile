FROM python:3

RUN mkdir /home/vega/
WORKDIR /home/vega/

COPY . .

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
