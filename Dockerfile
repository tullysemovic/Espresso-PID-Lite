FROM python:3.8
COPY . /server
WORKDIR /server
RUN pip install -r server/requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["server/run.py"]