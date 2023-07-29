# Base Image
FROM python:3.10-slim-bullseye

# Installing necessary packages
RUN pip install modal-client
RUN pip install oloren

COPY .modal.toml /root/.modal.toml
# Copying application code to the Docker image
COPY app.py /app.py
COPY detectron2modal.py /detectron2modal.py

# Default command for the container
CMD ["python", "app.py"]