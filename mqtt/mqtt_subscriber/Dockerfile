FROM python:3.7.3-alpine3.9

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

#run pip install and get all upgrades...
RUN pip install --upgrade pip

#RUN adduser worker // use addgroup for alpine otherwise groupadd
RUN addgroup -S worker && adduser -S worker -G worker

#change user to worker
USER worker

#change to home directory of worker
WORKDIR /app

#install pipenv to local directory of user ...currently active "worker"
RUN pip install --user -U --no-warn-script-location pipenv  

#copy only requirement files over, for simplicity ..
#python files to folder /app/
COPY --chown=worker:worker ./src/requirements.txt .
COPY --chown=worker:worker ./src/start.py .

#data / configs to to folder /data/
COPY --chown=worker:worker ./data/logger.conf ./data/logger.conf
COPY --chown=worker:worker ./data/topics.json ./data/topics.json

#install with the user the requirements
RUN pip install --user -r /app/requirements.txt --no-warn-script-location

#add the workder home directory to the path variable, is required because of the command from above..which notifies 
#about this therefore "--no-warn-script-location pipenv " was added...
ENV PATH="/home/worker/app .local/bin:${PATH}"

#add a label 
LABEL maintainer="matthias.morath@gmail.com" \
      version="1.0.0"

#finally call python and start the script start.py
CMD [ "python", "./start.py" ]