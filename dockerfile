# Step 1: Use an official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the requirements file first to install dependencies
COPY requirements.txt /app/

# Step 4: Install dependencies with retries and using a faster mirror
RUN pip install --no-cache-dir --retries 5 --timeout=180 -r requirements.txt -i https://pypi.org/simple

# Step 5: Copy the rest of the application files into the container
COPY . /app/

# Step 6: Expose the port that FastAPI will run on (default is 8000)
EXPOSE 8000

# Step 7: Set the entry point to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

