+++
date = '2026-01-04T02:50:21+05:30'
draft = false
title = 'This is how I run multiple application on my $5 vps instance'
+++




From past few months, I have been running multiple small webapps on a single VPS seamlessly. 

Each app gets its own subdomain, runs in its own Docker container, and is reverse-proxied via Nginx.  

This gives me Zero-Downtime App Deployment on a Single VPS using Nginx + Docker Compose

Nothing fancy.  
No Kubernetes.  
No PaaS.  
Just stuff that I understand end-to-end and won’t randomly surprise me.  

This post is basically my **personal checklist**.
Whenever I ship a new app, I follow these exact steps. If something breaks, I know exactly where to look.

---

### Step 1: SSH Into the Server

`ssh root@<vps_public_ip>`

---

### Step 2: Create a New Nginx Config for the Subdomain

Create one file per app at `/etc/nginx/sites-available/xyz.hostthis.tech`  
Say app name is `xyz`
Inside the file:

* Port 80 just redirects to HTTPS
* Port 443 handles SSL (Cloudflare)
* Nginx proxies traffic to localhost:8031
* 8031 is just an internal port exposed by Docker  

The file would look like:
```
server {
    listen 80;
    server_name xyz.hostthis.tech;
    return 301 https://xyz.hostthis.tech$request_uri;
}

server {
    listen 443 ssl http2;
    server_name xyz.hostthis.tech;

    include /etc/nginx/sites-available/templates/cloudflare-ssl.conf;

    location / {
        proxy_pass http://localhost:8031; # must match the docker exposed port
        include /etc/nginx/sites-available/templates/proxy.conf;
    }
}
```

The only thing I ever change here is the **port number**.

Once the file is ready, I enable it:
```
ln -s /etc/nginx/sites-available/xyz.hostthis.tech /etc/nginx/sites-enabled/
```
Then just test and reload Nginx:
```
nginx -t
systemctl restart nginx
```
At this point, the subdomain exists.
Even if the app isn’t running yet, Nginx is ready.

---

### Step 3: Deploy the App Using Docker Compose

Each app lives in its own folder.

So for this one:

* Clone the repo as `xyz_app` 
eg: `git clone <repo_url> xyz_app`
* It must have a valid Dockerfile

In my main docker-compose.yml, I add a new service.  

Edit your existing docker-compose.yml:  
```
services:
  xyz_app:
    build: ./xyz_app
    container_name: xyz_app
    restart: always
    ports:
      - "8031:8031"
    networks:
      - app_net

networks:
  app_net:
    driver: bridge
``` 
Important points:

* One container name per app
* One exposed port per app (8031 here)
* All apps live on the same Docker bridge network
* restart: always because My IT admin taught me
---

### Step 4: Build and Run Only This App

This is important.

I do NOT rebuild everything.

I only do:
```
docker compose build --no-cache xyz_app
docker compose up -d xyz_app
```
Other apps keep running.  
No downtime ; )

---

### Step 5: Debugging 

If something goes wrong, just check the logs

Logs:
```
docker logs xyz_app --tail=20
docker logs -f xyz_app
```
You can get Shell access: `docker exec -it xyz_app /bin/sh`

Restart: `docker restart xyz_app`

Stop (without deleting): `docker compose stop xyz_app`

For now that’s works for me 99% of the time.  

When time comes, I’ll upgrade.  
Until then, this setup has earned its place.  
(poetic huh)

Thanks for reading, you can ask ~doubts~ anything in the comments : ) 

---












