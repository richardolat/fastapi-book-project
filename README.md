# FastAPI App Deployment with Docker & Nginx Reverse Proxy

## Project Overview

This project deploys a **FastAPI** application using **Docker** for containerization and **Nginx** as a reverse proxy to handle incoming traffic. The project also includes a **CI/CD pipeline** powered by **GitHub Actions**, which automatically deploys changes to an **AWS EC2** instance when changes are made to the `main` branch or when a pull request is merged into it.

The application is deployed in a **Docker container** on an **Ubuntu EC2 instance**. The deployment process is automated through GitHub Actions, which ensures that every change pushed to the repository is reflected on the live server.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Project Setup](#project-setup)
3. [How to Run Locally](#how-to-run-locally)
4. [Missing Endpoint](#missing-endpoint)
5. [Deployment Process](#deployment-process)
6. [GitHub Actions CI/CD Workflow](#github-actions-cicd-workflow)
7. [License](#license)

---

## Technologies Used

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **Docker**: A platform for automating the deployment of applications inside lightweight containers.
- **Nginx**: A web server used to serve the FastAPI application behind a reverse proxy.
- **GitHub Actions**: A CI/CD tool used for automating deployment to an EC2 instance on AWS.
- **Ubuntu EC2 Instance**: Amazon Web Services (AWS) EC2 instance running Ubuntu to host the FastAPI application.
- **Python**: The programming language used to build the FastAPI application.

---

## Project Setup

### 1. **Clone the Repository**

To get started with the project, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/fastapi-deployment.git
cd fastapi-deployment
```


### 2. Install Dependencies
The project relies on certain Python dependencies. Install them by running:

```bash
pip install -r requirements.txt
requirements.txt includes the necessary libraries such as fastapi, uvicorn, etc.
```

### 3. Docker Setup
To build and run the application with Docker, make sure Docker is installed on your machine. You can find installation instructions on Docker's website.

### Build the Docker Image
```bash
Run the following command to build the Docker image for the application:
docker build -t fastapi-app .
Run the Docker Container
Once the image is built, you can run it with:
docker run -d --name fastapi-container -p 8000:8000 fastapi-app
This will start the FastAPI app inside a Docker container and map port 8000 inside the container to port 8000 on your local machine.
```

### How to Run Locally
### To run the FastAPI app locally, simply use Uvicorn, which is a lightning-fast ASGI server for Python. This is ideal for FastAPI applications.

### 1. Install Uvicorn
If you don’t have Uvicorn installed, install it using:

```bash
pip install uvicorn
```
### 2. Run the Application
Start the app with:
```bash
uvicorn main:app --reload
This will start the FastAPI app locally, and you can access it by navigating to http://127.0.0.1:8000 in your browser.
```

### Missing Endpoint
The following GET endpoint allows you to fetch a specific book by its ID from the in-memory database.

Code for the Missing Endpoint:
```python
@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int) -> Book:
    book = db.books.get(book_id)
    if book:
        return book
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": f"Book with ID {book_id} not found"},
    )
This endpoint is added to the existing books.py file, and it checks the InMemoryDB for a specific book based on the book_id.
```

## Deployment Process
### 1. Set Up EC2 Instance
## Deploy the application to an Ubuntu EC2 instance by following these steps:

### Launch an Ubuntu EC2 instance in AWS.

### Ensure the EC2 instance has a public IP address and is accessible via SSH.

## Install Docker and Nginx on the EC2 instance.

### Install Docker:

```bash
sudo apt update
sudo apt install -y docker.io
Install Nginx:
```

```bash
sudo apt install -y nginx
```

### 2. Set Up Nginx Reverse Proxy
The application uses Nginx as a reverse proxy. Below is the Nginx configuration for the reverse proxy setup:

```bash
server {
    listen 80;
    server_name your-domain.com;  # Change to your domain or public IP

    location / {
        proxy_pass http://127.0.0.1:8000;  # FastAPI container's port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Once the file is created, enable the Nginx site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 3. Run the FastAPI Docker Container on EC2
## SSH into your EC2 instance and navigate to your project directory. Then, build and run the Docker container as shown in the previous steps.

### GitHub Actions CI/CD Workflow

### Workflow Overview
### This project uses GitHub Actions to automate the deployment of changes to the EC2 instance. The workflow is triggered when changes are pushed to the main branch or when a pull request is merged into main.

### The following steps are performed in the CI/CD pipeline:

### Checkout the repository.
### Set up SSH to securely access the EC2 instance using a private key stored in GitHub Secrets.
### Rebuild the Docker image on the EC2 instance.
### Restart the Docker container to reflect changes.
### Restart Nginx to apply any changes to the reverse proxy.
### GitHub Actions Workflow
### The .github/workflows/deploy.yml file looks like this:

```yaml
---
name: Deploy FastAPI App to EC2

on:
  push:
    branches:
      - main
  pull_request:
    types: [closed]  # Trigger when a PR is merged into main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      # Checkout code from GitHub repository
      - name: Checkout repository
        uses: actions/checkout@v2

      # Set up SSH for EC2
      - name: Set up SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.EC2_SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.EC2_PUBLIC_IP }} >> ~/.ssh/known_hosts

      # Deploy FastAPI app to EC2
      - name: Deploy FastAPI app to EC2
        run: |
          ssh -o StrictHostKeyChecking=no ubuntu@${{ secrets.EC2_PUBLIC_IP }} << 'EOF'
            cd /home/ubuntu/fastapi-book-project
            git pull origin main
            docker build -t fastapi-app .
            docker stop fastapi-container || true
            docker rm fastapi-container || true
            docker run -d --name fastapi-container -p 8000:8000 fastapi-app
            sudo systemctl restart nginx
          EOF
``` 

### Secrets Required
### Ensure the following secrets are added to your GitHub repository:

### EC2_SSH_PRIVATE_KEY: The private SSH key for your EC2 instance.
### EC2_PUBLIC_IP: The public IP address of your EC2 instance (e.g., 54.152.65.119).
### Adding the Secrets
### Go to your GitHub repository.
### Navigate to Settings > Secrets > New repository secret.
### Add the secrets with the appropriate names:
### EC2_SSH_PRIVATE_KEY: The private key file (without line breaks).
### EC2_PUBLIC_IP: The public IP of your EC2 instance.
## License
### This project is licensed under the MIT License. See the LICENSE file for more details.