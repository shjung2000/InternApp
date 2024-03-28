FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./apply_for_internship.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./apply_for_internship.py" ]


