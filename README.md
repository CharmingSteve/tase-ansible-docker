# Hello World Counter Application

A containerized application that displays a "Hello World" message and tracks page visits using Redis for persistent storage. Deployed via Ansible for automated infrastructure management.

## Architecture

This application consists of two main components:

1. **Web Server (Python/Flask)**
   - Serves a simple "Hello World" page
   - Tracks and displays visit counts
   - Built with Flask and Gunicorn
   - Uses multi-stage Docker build for optimized image size

2. **Database (Redis)**
   - Stores the visit counter
   - Persists data across container restarts
   - Lightweight and fast in-memory database

## Deployment

### Prerequisites

- Target machine with Docker and Docker Compose installed
- Ansible configured with the target in `/etc/ansible/hosts`

### Setup

1. Install required Ansible collection:
   ```bash
   ansible-galaxy collection install community.docker
   ```

2. Deploy the application:
   ```bash
   ansible-playbook deploy.yml
   ```

3. Access the application:
   ```
   http://[target-machine-ip]:8080
   ```

### Cleanup

To remove the deployment:
```bash
ansible-playbook cleanup.yml
```

## Technical Features

- **Multi-stage Docker Build**: Produces smaller, more secure containers
- **Stateful Counter**: Persists across container restarts via Redis volume
- **Idempotent Deployment**: Only updates when changes are detected
- **Production-ready Web Server**: Uses Gunicorn for better performance
- **Non-root Container**: Runs as unprivileged user for better security
- **Health Checks**: Monitors service health for both containers
- **Isolated Network**: Services communicate over a private Docker network

## Troubleshooting

### Web Server Issues

1. **Container not starting**:
   ```bash
   docker logs hello-counter-web-1
   ```
   - Look for Python import errors or Flask startup issues
   - Check if Gunicorn can bind to the specified port

2. **Worker timeouts**:
   - Increase Gunicorn timeout: Modify `--timeout` parameter in Dockerfile CMD
   - Reduce worker count: Use `--workers 1` for debugging
   - Check for blocking operations in Flask routes

3. **Import errors**:
   - Verify compatible package versions in Dockerfile
   - Ensure all dependencies are properly installed
   - Check for missing Python modules

4. **Permission issues**:
   - Verify the container is running as the correct user
   - Check file permissions in mounted volumes
   - Ensure Gunicorn has access to necessary directories

### Redis Issues

1. **Connection problems**:
   ```bash
   docker exec hello-counter-redis-1 redis-cli ping
   ```
   - Should return "PONG" if Redis is running correctly

2. **Data persistence**:
   - Verify volume is properly configured:
     ```bash
     docker volume inspect hello-counter_redis-data
     ```
   - Check Redis logs for any data loading/saving errors:
     ```bash
     docker logs hello-counter-redis-1
     ```

3. **Memory issues**:
   - Check Redis memory usage:
     ```bash
     docker exec hello-counter-redis-1 redis-cli info memory
     ```
   - Adjust memory settings if needed

4. **Network connectivity**:
   - Verify services are on the same network:
     ```bash
     docker network inspect hello-counter_app-network
     ```
   - Test connection from web container:
     ```bash
     docker exec hello-counter-web-1 curl -v telnet://redis:6379
     ```

## Container Health Status

Check container health status:
```bash
docker ps
```

Look for `(healthy)` or `(unhealthy)` in the STATUS column.

For detailed health check logs:
```bash
docker inspect --format='{{json .State.Health}}' hello-counter-web-1 | jq
```

## Performance Tuning

- Adjust Gunicorn workers: `--workers=2` (rule of thumb: 2 × CPU cores + 1)
- Optimize Redis: Consider enabling AOF for better persistence
- Scale web tier horizontally for higher loads

## Security Considerations

- All services run as non-root users
- No sensitive data stored in the application
- Containers have minimal installed packages
- Dependencies are pinned to specific versions

This application demonstrates containerization, service orchestration, and infrastructure as code principles in a simple but effective implementation.