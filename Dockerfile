FROM python:3.6

RUN groupadd -r gunicorn && useradd -r -g gunicorn gunicorn
WORKDIR /Segmentator
COPY . /Segmentator/
COPY install_packages.sh /Segmentator/
RUN ./install_packages.sh
EXPOSE 5000
USER gunicorn

#CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "--preload"]
CMD ["python3", "run.py"]
