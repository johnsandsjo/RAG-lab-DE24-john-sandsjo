FROM python:3.13-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY /frontend /frontend
COPY api.py .
COPY function_app.py .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Define the command to run your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]