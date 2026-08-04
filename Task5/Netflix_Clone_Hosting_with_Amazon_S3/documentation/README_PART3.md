# Part 3 — EC2, NGINX and Netflix Clone Deployment

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Launch Ubuntu EC2

Configure:

```text
Name: project-05-netflix-web
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Storage: 10 GiB gp3
Auto-assign Public IP: Enabled
```

Attach the Security Group:

```text
HTTP 80 from 0.0.0.0/0
SSH 22 from My IP
```

## Step 2 — Connect to EC2

```bash
chmod 400 project-key.pem
ssh -i project-key.pem ubuntu@<EC2_PUBLIC_IP>
```

## Step 3 — Install NGINX

```bash
sudo apt update -y
sudo apt install nginx git curl -y
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx --no-pager
```

Test:

```bash
curl -I http://localhost
```

Expected:

```text
HTTP/1.1 200 OK
```

## Step 4 — Deploy the Supplied Website

The package includes:

```text
website/
├── index.html
├── style.css
├── script.js
└── config.js
```

Copy the folder to EC2 using SCP:

```bash
scp -i project-key.pem -r website \
  ubuntu@<EC2_PUBLIC_IP>:/home/ubuntu/
```

On EC2:

```bash
sudo mkdir -p /var/www/netflix-clone
sudo cp -R /home/ubuntu/website/. /var/www/netflix-clone/
sudo chown -R www-data:www-data /var/www/netflix-clone
sudo find /var/www/netflix-clone -type d -exec chmod 755 {} \;
sudo find /var/www/netflix-clone -type f -exec chmod 644 {} \;
```

## Step 5 — Configure NGINX

Create:

```bash
sudo nano /etc/nginx/sites-available/netflix-clone
```

Add:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name _;

    root /var/www/netflix-clone;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(css|js|png|jpg|jpeg|gif|svg|ico)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/netflix-clone \
  /etc/nginx/sites-enabled/netflix-clone

sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## Step 6 — Test Website

Open:

```text
http://<EC2_PUBLIC_IP>
```

Expected:

- Netflix clone page loads
- Styles and JavaScript work
- Movie cards display
- Video buttons are visible

## User Data Alternative

The package includes:

```text
scripts/user-data.sh
```

Update the repository URL and S3 bucket name before pasting it into EC2 User Data.

## Troubleshooting

### NGINX 403

Check:

```bash
namei -l /var/www/netflix-clone/index.html
sudo chown -R www-data:www-data /var/www/netflix-clone
```

### NGINX 404

Check:

```bash
ls -la /var/www/netflix-clone
sudo nginx -T
```

### Website Does Not Open

Check:

```bash
sudo ss -lntp | grep ':80'
sudo systemctl status nginx --no-pager
```

Also verify Security Group port 80.

## Checklist

- [ ] Ubuntu EC2 running
- [ ] Public IP assigned
- [ ] NGINX installed
- [ ] NGINX enabled
- [ ] Website copied
- [ ] NGINX server block configured
- [ ] Configuration test passed
- [ ] Website opens through Public IP
