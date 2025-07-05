# Latest python Docker container
FROM python:latest

# Set a workin directory in the container for code and libraries
WORKDIR /code

# Copy all code and configurations into the container
ADD ./lib/*.py ./lib/
ADD ./main.py ./main.py
ADD ./requirements.txt ./requirements.txt

# Install dependencies (Python pip modules)
RUN pip install -r requirements.txt

# Run main.py on container startup
CMD [ "python", "./main.py" ]
