# Part 4 — S3 Video Integration, Streaming Test and Domain Access

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Update `config.js`

The website uses:

```javascript
window.VIDEO_CONFIG = {
  bucketBaseUrl: "https://<BUCKET_NAME>.s3.ap-south-1.amazonaws.com/videos",
  videos: [
    {
      title: "AWS DevOps Documentary",
      file: "movie1.mp4",
      poster: "https://images.unsplash.com/photo-1451187580459-43490279c0fa"
    },
    {
      title: "Cloud Engineering",
      file: "movie2.mp4",
      poster: "https://images.unsplash.com/photo-1518770660439-4636190af475"
    },
    {
      title: "Linux Administration",
      file: "movie3.mp4",
      poster: "https://images.unsplash.com/photo-1629654297299-c8506221ca97"
    }
  ]
};
```

Replace `<BUCKET_NAME>`.

Deploy the updated file:

```bash
scp -i project-key.pem website/config.js \
  ubuntu@<EC2_PUBLIC_IP>:/home/ubuntu/config.js

ssh -i project-key.pem ubuntu@<EC2_PUBLIC_IP>

sudo cp /home/ubuntu/config.js \
  /var/www/netflix-clone/config.js

sudo chown www-data:www-data \
  /var/www/netflix-clone/config.js
```

## Step 2 — Verify Streaming

Open:

```text
http://<EC2_PUBLIC_IP>
```

Click a movie.

Verify:

- Video modal opens
- Video plays
- Seek bar works
- Pause and resume work
- Browser receives video from S3

## Step 3 — Verify in Browser Developer Tools

Open:

```text
F12 → Network → Media
```

Expected request host:

```text
<BUCKET_NAME>.s3.ap-south-1.amazonaws.com
```

This proves EC2 serves the website while S3 serves the video.

## Step 4 — Test from Command Line

```bash
curl -I \
  https://<BUCKET_NAME>.s3.ap-south-1.amazonaws.com/videos/movie1.mp4
```

Expected:

```text
200 OK
Content-Type: video/mp4
Accept-Ranges: bytes
```

## Step 5 — Optional Domain Configuration

Create a Route 53 record:

```text
Record type: A
Name: netflix.example.com
Value: EC2 Elastic IP
TTL: 300
```

Because a normal EC2 Public IP can change after stop/start, allocate and associate an Elastic IP first.

## Step 6 — Optional HTTPS

Recommended production options:

- NGINX with Let's Encrypt certificate
- Application Load Balancer with ACM certificate
- CloudFront in front of S3 and EC2-based origin
- Route 53 DNS

## Important Browser Issue

A website served over HTTPS cannot load video over HTTP.

Use HTTPS for both:

```text
Website: HTTPS
S3 video URL: HTTPS
```

## Streaming Validation Checklist

- [ ] `config.js` contains correct bucket URL
- [ ] Video names match S3 object keys exactly
- [ ] Video `Content-Type` is correct
- [ ] CORS permits GET and HEAD
- [ ] Video plays
- [ ] Seeking works
- [ ] Network tab shows S3 host
- [ ] No mixed-content errors
- [ ] Public IP or domain works
