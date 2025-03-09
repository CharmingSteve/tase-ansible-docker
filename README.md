# Hello World Counter Application

A simple containerized application that displays a "Hello World" message and counts page visits.

## Components

- **Web Server**: Python Flask application serving a Hello World page with visit counter
- **Database**: Redis instance storing the visit counter
- **Deployment**: Ansible playbook for automated deployment

## Architecture

- The web server displays a simple Hello World page
- Each page visit increments a counter stored in Redis
- The current count is displayed on the page
- Docker Compose manages both services
- Ansible automates the deployment

## Technical Features

- **Multi-stage Docker Build**: Produces smaller, more secure containers
- **Stateful Counter**: Persists across container restarts
- **Idempotent Deployment**: Only updates when changes are detected
- **Production-ready Web Server**: Uses Gunicorn instead of Flask's development server
- **Non-root Container**: Runs as unprivileged user for better security

## Deployment

### Prerequisites

- Target machine with Docker and Docker Compose installed
- Ansible configured with the target in `/etc/ansible/hosts`

### Deploy

```bash
ansible-playbook deploy.yml
```

## Container Optimization

This project uses multi-stage Docker builds to create smaller, more efficient containers:

1. **Builder Stage**: Installs dependencies in an isolated environment
2. **Runtime Stage**: Contains only the necessary application code and dependencies
3. **Security**: Runs as a non-root user
4. **Performance**: Uses Gunicorn for better performance in production

The resulting container is significantly smaller than a traditional build, making it faster to deploy and more resource-efficient on the Raspberry Pi.