# Agrocare-ML Project Setup Documentation

This documentation provides step-by-step instructions to set up the **Agrocare-ML** project on an Ubuntu server. It includes details about the required environment, dependencies, and deployment process.

---

## Prerequisites

- **Operating System**: Ubuntu 20.04 (LTS) x64
- **Python Version**: Python 3.8 (required for machine learning model compatibility)
  - Other Python versions may cause conflicts when loading trained machine learning models.
- **Git**: Ensure Git is installed to clone the repository.

---

## 1. Install Ubuntu Updates and Required Tools

Run the following commands to update the system and install essential tools:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git curl ufw python3.8-venv -y
```

Verify the Python version:

```bash
python --version
## or ##
python3 --version
```

---

## 2. Clone the Project Repository

Use Git to clone the project repository to your desired location:

```bash
git clone https://github.com/Agro-care/Agrocare-ML.git
cd Agrocare-ML
```

---

## 3. Setup Python Virtual Environment

Create a virtual environment using Python 3.8:

```bash
python3.8 -m venv venv
source venv/bin/activate
```

Verify that the virtual environment is active (you should see `(venv)` in your terminal prompt).

---

## 4. Install Project Dependencies

### Option 1: Install Using `requirements.txt`

Run the following command to install all required Python libraries:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Install Libraries Manually

If needed, you can manually install libraries. Common dependencies include:

// TODO incomplete for pytorch

```bash
pip install django gunicorn torch torchvision numpy pandas django-cors-headers deep-translator
```

---

## 5. Test Functionality Locally

Before deploying, test the functionality of the project locally:

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Open a browser and navigate to `http://127.0.0.1:8000` to verify the application.

---

## 6. Setup Gunicorn and Nginx for Production

### Step 1: Install Gunicorn

Install Gunicorn inside the virtual environment:

```bash
pip install gunicorn
```

Run Gunicorn to test the application:

```bash
gunicorn --bind 0.0.0.0:8000 AgrocareML.wsgi:application
```

Stop it using `Ctrl+C` once verified.

### Step 2: Create a Gunicorn Systemd Service

Create a systemd service to run Gunicorn as a background process:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve Agrocare-ML
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory={/path/to/Agrocare-ML}
ExecStart=/path/to/Agrocare-ML/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock AgrocareML.wsgi:application

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/Agrocare-ML` and `your_user` with the appropriate paths and username.

Enable and start the Gunicorn service:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Step 3: Install and Configure Nginx

Install Nginx:

```bash
sudo apt install nginx
```

Create a new Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/AgrocareML
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com server_domain_or_IP;

    location /static/ {
        root /path/to/Agrocare-ML/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Replace `your_domain.com` and `/path/to/Agrocare-ML` with your domain and correct project path.

Enable the site, configure UFW, and restart Nginx:

```bash
# Allow necessary ports and enable Nginx full profile in UFW
sudo ufw allow 8000/tcp
sudo ufw disallow 8000/tcp
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Enable the site and restart Nginx
sudo ln -s /etc/nginx/sites-available/AgrocareML /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

```bash
sudo ln -s /etc/nginx/sites-available/AgrocareML /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Setup SSL Using Certbot

Secure your site with SSL certificates using Certbot:

1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```
2. Obtain SSL Certificates:
   ```bash
   sudo certbot --nginx -d your_domain.com -d www.your_domain.com
   ```
3. Verify Auto-Renewal:
   ```bash
   sudo certbot renew --dry-run
   ```

Certbot will automatically configure Nginx to use SSL certificates.

---

## 8. Test the APIs

Verify that the APIs are working:

- Use tools like **Postman** or `curl` to send requests to the API endpoint.
- Example request:
  ```bash
  curl -X POST https://your_domain.com/api/crop-recommendation/predict/ \
  -H "Content-Type: application/json" \
  -d '{"Nitrogen": 90, "Phosphorous": 42, "Potassium": 43, "Temperature": 20, "Humidity": 82, "Ph": 6, "Rainfall": 202}'
  ```

Expected output:

```json
{
    "prediction": "Rice"
}
```

---

## 9. Firewall Configuration (Optional)

Enable and configure UFW (Uncomplicated Firewall):

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable 
```

---

## Summary

By following this documentation, you have:

- Cloned the Agrocare-ML repository.
- Set up the virtual environment and installed dependencies.
- Configured Gunicorn and Nginx for production.
- Secured your site with SSL using Certbot.
- Tested the functionality and APIs.

Your Django application should now be running successfully on `https://your_domain.com`. For further troubleshooting, check Nginx and Gunicorn logs:

```bash
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u gunicorn
```

