# Using latest version of Python
FROM python:3.13

# Setting up the Working Directory
WORKDIR /app/

# Copying and running the requirements
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Doing the setup of copy the source code to be run
COPY src/ ./

# Port which will be exposed
EXPOSE 3001

# Running the container (Using uvicorn to have a web server for my FastAPi object in main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
