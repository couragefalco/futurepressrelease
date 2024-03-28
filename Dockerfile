# Use the official Python base image
FROM python:3.10.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt ./ 

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container at /app
COPY . .

# Streamlit runs on port 8501, so expose that port
EXPOSE 8501

# Command to run the app. Use the streamlit run command to run your script
CMD ["streamlit", "run", "main.py"]
