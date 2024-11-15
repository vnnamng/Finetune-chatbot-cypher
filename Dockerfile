# Use Python 3.10.11-slim as the base image
FROM python:3.10.11-slim

# Set the working directory inside the container to /app
WORKDIR /app
RUN mkdir -p /app/lib && chmod -R 777 /app/lib

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create the html_files directory if it doesn't exist and set permissions
RUN mkdir -p /app/html_files && chmod -R 777 /app/html_files

# Create the html_files directory if it doesn't exist and set permissions
RUN mkdir -p /app/tmp && chmod -R 777 /app/tmp

# Copy the source code from the src directory into /app/src inside the container
COPY src ./src

# Copy the HTML files into the container
COPY src/network.html ./network.html
COPY src/tmp/pyvis_graph.html ./tmp/pyvis_graph.html

# Expose the port Streamlit will use (default is 8501)
EXPOSE 8501

# Create and switch to a non-root user for security purposes
RUN useradd app
USER app

# Run the Streamlit app 
CMD ["streamlit", "run", "src/Hello.py"]
