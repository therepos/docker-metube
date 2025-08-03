FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN pip install mutagen watchdog

COPY postprocess.py /postprocess.py
COPY cover.png /cover.png

CMD ["python", "/postprocess.py"]
