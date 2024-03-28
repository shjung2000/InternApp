FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./student_history.py ./amqp_setup.py ./
CMD [ "python", "./student_history.py" ]


