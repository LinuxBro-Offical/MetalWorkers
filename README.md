# Metal Workers API

A FastAPI application serving the frontend, paired with a Django project for administrative functionality. Both applications share a single SQLite database (`metalworkers.db`).

## Getting Started

### 1. Prerequisites

- Python 3.8+ (ensure your `venv` is set up with a compatible version)
- `pip` for dependency management

### 2. Setup (Run these commands from `MetalWorkers/metalworkers-api`)

1.  **Activate Virtual Environment**: If you don't have one, create it (`python -m venv venv`) then activate it.

    ```bash
    source MetalWorkers/venv/bin/activate
    ```

2.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Django Migrations**: This will set up the shared database schema for both applications.

    ```bash
    python manage.py makemigrations api_admin
    python manage.py migrate
    ```

4.  **Collect Django Static Files**: Essential for the Django Admin interface to be styled correctly.

    ```bash
    python manage.py collectstatic --noinput
    ```

5.  **Create Django Superuser**: For accessing the Django Admin panel.

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your admin login.

### 3. Running Applications Locally

Open **two separate terminal windows** (ensure your virtual environment is activated in both).

#### Terminal Window 1: Run FastAPI Application

```bash
cd MetalWorkers/metalworkers-api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*   **Access FastAPI Frontend/APIs**: `http://localhost:8000/`
*   **Access FastAPI API Docs**: `http://localhost:8000/docs`

#### Terminal Window 2: Run Django Admin Panel

```bash
cd MetalWorkers/metalworkers-api
gunicorn admin_panel.wsgi:application --bind 0.0.0.0:8001
# Alternatively, for simpler local dev:
# python manage.py runserver 8001
```
*   **Access Django Admin Panel**: `http://localhost:8001/admin/`

### 4. Docker Container (Recommended for `reopen in containers`)

This project includes a Dockerfile that sets up the environment, runs Django migrations, collects static files, and uses Supervisor to run both the FastAPI and Django applications.

1.  **Build the Docker Image**:

    ```bash
    docker build -t metalworkers-api .
    ```

2.  **Run the Docker Container**:

    This will start both FastAPI (port 8000) and Django Admin (port 8001) processes within the container, managed by Supervisor. Ports will be mapped to your host.

    ```bash
    docker run --rm -it -p 8000:8000 -p 8001:8001 metalworkers-api
    ```
    *   **Access FastAPI Frontend/APIs**: `http://localhost:8000/`
    *   **Access FastAPI API Docs**: `http://localhost:8000/docs`
    *   **Access Django Admin Panel**: `http://localhost:8001/admin/`

3.  **Stopping the Container**:

    Press `Ctrl+C` in the terminal where the container is running, or if it's detached, use `docker stop <container_id_or_name>`.

### 5. Running Management Commands and One-Time Scripts in Docker

When your application is running inside a Docker container, you need to execute management commands (like Django's `makemigrations`, `migrate`, `createsuperuser`) or your custom one-time scripts using `docker exec`. The container will already have `supervisord` running in the background, managing your applications.

First, you'll need the **Container ID** or **Container Name** of your running `metalworkers-api` container. You can find it by running:

```bash
docker ps
```

Once inside the container (or using `docker exec -it <container_id_or_name> bash`), you can run commands directly, or use `supervisorctl` to manage your running processes.

#### Examples:

*   **Access the interactive shell inside the running container**:

    ```bash
    docker exec -it <container_id_or_name> bash
    ```
    Once inside, you can run `python manage.py createsuperuser` directly.

*   **Run Django Migrations (if needed after a model change) directly**:

    ```bash
    docker exec -it <container_id_or_name> /usr/local/bin/python manage.py makemigrations api_admin
    docker exec -it <container_id_or_name> /usr/local/bin/python manage.py migrate
    ```

*   **Create Django Superuser directly**:

    ```bash
    docker exec -it <container_id_or_name> /usr/local/bin/python manage.py createsuperuser
    ```

*   **Run `add_default_services.py` script directly**:

    ```bash
    docker exec -it <container_id_or_name> /usr/local/bin/python one_time_scripts/add_default_services.py
    ```

*   **Run `export_newsletter_emails.py` script directly**:

    ```bash
    docker exec -it <container_id_or_name> /usr/local/bin/python one_time_scripts/export_newsletter_emails.py
    ```

*   **Check Supervisor status inside the container**:

    ```bash
    docker exec -it <container_id_or_name> supervisorctl status
    ```

### 6. Deployment to AWS EC2

This section provides a detailed guide to deploy your FastAPI and Django hybrid application to an AWS EC2 instance using Supervisor for process management and Nginx as a reverse proxy with SSL/TLS.

#### 1. AWS EC2 Instance Setup

*   **Launch an EC2 Instance**: Choose an Ubuntu Server (e.g., 22.04 LTS) instance type that suits your needs (e.g., `t2.micro` for testing). Ensure you create/select a Key Pair for SSH access.
*   **Configure Security Group**: During instance launch (or by modifying existing security groups), ensure inbound rules allow:
    *   **SSH**: Port `22` (Source `My IP` or `Anywhere` if you understand the risks).
    *   **HTTP**: Port `80` (Source `Anywhere`).
    *   **HTTPS**: Port `443` (Source `Anywhere`).
    *   (Initially, you might temporarily open port `8000` and `8001` from your IP for direct testing, but these will be proxied by Nginx later).
*   **Connect via SSH**: Once the instance is running, connect using your key pair:
    ```bash
    ssh -i /path/to/your-key.pem ubuntu@<your-ec2-public-ip-address>
    ```

#### 2. System Dependencies and Python Environment on EC2

1.  **Update System & Install Git**: Once logged into your EC2 instance:

    ```bash
    sudo apt update
    sudo apt upgrade -y
    sudo apt install git python3-venv python3-pip build-essential nginx supervisor certbot python3-certbot-nginx -y
    ```

2.  **Clone Your Repository**: Clone your project from your Git repository (e.g., GitHub, GitLab).

    ```bash
    git clone <your-repository-url> /home/ubuntu/Development/MetalWorkers/metalworkers-api
    # Example: git clone https://github.com/your-username/your-repo.git /home/ubuntu/Development/MetalWorkers/metalworkers-api
    ```
    *Adjust the target directory `/home/ubuntu/Development/MetalWorkers/metalworkers-api` if you prefer a different path.* Note this path, as it will be used in configurations.

3.  **Create and Activate Virtual Environment**: Create a Python virtual environment and activate it.

    ```bash
    cd /home/ubuntu/Development/MetalWorkers/metalworkers-api
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Python Dependencies**: Install all project-specific Python packages.

    ```bash
    pip install -r requirements.txt
    ```
    *Ensure `gunicorn` and `uvicorn[standard]` are listed in `requirements.txt` (they should be).* 

#### 3. Django Database & Admin Setup on EC2

*Run these commands from `/home/ubuntu/Development/MetalWorkers/metalworkers-api` on your EC2 instance.*

1.  **Make and Apply Django Migrations**: This creates the necessary database tables in `metalworkers.db`.

    ```bash
    python manage.py makemigrations api_admin
    python manage.py migrate
    ```

2.  **Collect Django Static Files**: This gathers all static assets required for the Django Admin interface.

    ```bash
    python manage.py collectstatic --noinput
    ```

3.  **Create Django Superuser**: Essential for logging into the Django Admin panel.

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set your administrator credentials.

#### 4. Supervisor Configuration on EC2

Supervisor will manage both your FastAPI and Django Gunicorn processes, keeping them running reliably.

1.  **Copy Supervisor Config File**: Copy the `metalworkers-api.conf` from your cloned repository to Supervisor's configuration directory. 

    ```bash
    sudo cp /home/ubuntu/Development/MetalWorkers/metalworkers-api/metalworkers-api.conf /etc/supervisor/conf.d/
    ```

2.  **Edit `metalworkers-api.conf` on EC2**: Open the copied file for editing.

    ```bash
    sudo nano /etc/supervisor/conf.d/metalworkers-api.conf
    ```
    *   **Adjust Paths**: Ensure `command` and `directory` paths are correct for your EC2 environment. The `deploy/metalworkers-api.conf` file should already be updated for Docker, which uses `/app`. **You need to revert the paths to reflect the EC2 host environment.** For example:
        *   `command=/home/ubuntu/Development/MetalWorkers/venv/bin/gunicorn ...`
        *   `directory=/home/ubuntu/Development/MetalWorkers/metalworkers-api`
    *   **Set `user`**: Change `user=ubuntu` (or the actual user for your EC2 instance).
    *   **Log Paths**: Change log paths from `/app/logs/...` to `/var/log/metalworkers-api/...`.

3.  **Create Log Directories on EC2**: Supervisor needs these directories for logs.

    ```bash
    sudo mkdir -p /var/log/metalworkers-api/
    sudo chown -R ubuntu:ubuntu /var/log/metalworkers-api/ # Adjust user/group if different
    ```

4.  **Update and Start Supervisor Processes**: Reload Supervisor's configuration and start your applications.

    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start metalworkers-api metalworkers-django-admin
    ```

5.  **Check Status**: Verify both processes are running.

    ```bash
    sudo supervisorctl status
    ```

#### 5. Nginx Reverse Proxy & SSL Configuration on EC2

Nginx will serve your application on standard web ports (80/443) and manage SSL, proxying requests to your FastAPI and Django applications running on ports 8000 and 8001.

1.  **Copy Nginx Configuration File**: Copy the `nginx.conf` from your project to Nginx's `sites-available` directory.

    ```bash
    sudo cp /home/ubuntu/Development/MetalWorkers/metalworkers-api/nginx.conf /etc/nginx/sites-available/your_domain.com
    ```
    *Replace `your_domain.com` with your actual domain name.* 

2.  **Edit `your_domain.com` Nginx Config on EC2**: Open the copied file for editing.

    ```bash
    sudo nano /etc/nginx/sites-available/your_domain.com
    ```
    *   **Replace Placeholders**: Update `server_name` to your actual domain(s) (e.g., `your_domain.com www.your_domain.com`).
    *   **Adjust Static/Django Static Aliases**: Change the `alias` paths for `/static/` and `/django_static/` to their absolute locations on your EC2 instance:
        *   `/home/ubuntu/Development/MetalWorkers/metalworkers-api/static/`
        *   `/home/ubuntu/Development/MetalWorkers/django_static/` (Note: Django collects to the workspace root, not `/metalworkers-api/django_static/`)

3.  **Enable Nginx Site & Remove Default**: Link your configuration and disable the default Nginx site.

    ```bash
    sudo ln -s /etc/nginx/sites-available/your_domain.com /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default
    ```

4.  **Test Nginx Configuration**: Check for syntax errors.

    ```bash
    sudo nginx -t
    ```

5.  **Restart Nginx**: Apply the new configuration.

    ```bash
    sudo systemctl restart nginx
    ```

#### 6. Configure DNS

*   **A Record**: At your domain registrar (or AWS Route 53), create/update `A` records for `your_domain.com` and `www.your_domain.com` to point to your EC2 instance's **Public IPv4 address**.
*   **Propagation**: Allow some time for DNS changes to propagate globally.

#### 7. Secure with SSL/TLS (HTTPS) using Certbot

1.  **Obtain and Install SSL Certificate**: Certbot will automate getting a free Let's Encrypt certificate and configuring Nginx for HTTPS.

    ```bash
    sudo certbot --nginx -d your_domain.com -d www.your_domain.com
    ```
    *   Follow the prompts (enter email, agree to terms, choose redirect option).

2.  **Verify Auto-Renewal**: Certbot sets up automatic renewal. Test it:

    ```bash
    sudo certbot renew --dry-run
    ```

#### 8. Final Check

*   Navigate to `https://metalworkers.com/` and `https://metalworkers.com/admin/` in your browser. Both should now be accessible and secure.

***

### Important Considerations for Production:

*   **Security**: Do not use `DEBUG = True` in Django's `settings.py` for production. Set `ALLOWED_HOSTS` to your actual domain names.
*   **Database**: For production, consider using a managed database service like AWS RDS (PostgreSQL, MySQL) instead of SQLite.
*   **Secret Keys**: Ensure `SECRET_KEY` in `admin_panel/settings.py` is loaded from environment variables and is strong.
*   **Logging**: Implement more robust logging configurations.
*   **Firewall**: AWS Security Groups act as your firewall. Ensure only necessary ports are open. 