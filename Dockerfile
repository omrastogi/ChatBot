FROM python:3.8.3
# RUN python3 -m pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
#EXPOSE 5000
#EXPOSE 80ls

#CMD ["python3", "app.py"]
CMD ["python3", "-m","flask", "run","--host=0.0.0.0"]