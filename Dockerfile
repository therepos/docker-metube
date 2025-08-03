FROM python:3.11-slim

RUN pip install mutagen watchdog

COPY postprocess.py /postprocess.py

CMD ["python", "/postprocess.py"]
