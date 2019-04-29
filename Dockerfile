# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /clubReccomendationNU

# Copy the current directory contents into the container at /clubReccomendationNU
ADD . /clubReccomendationNU

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install the stopwords for the tfidf calculations
RUN python -m nltk.downloader stopwords

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "webInterface.py"]