# Part 5 — Verification, Cleanup, Troubleshooting and Interview Questions

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Verification

### EC2

```bash
sudo systemctl status nginx --no-pager
sudo nginx -t
sudo ss -lntp | grep ':80'
curl -I http://localhost
```

### S3

```bash
aws s3 ls s3://<BUCKET_NAME>/videos/ --recursive
aws s3api get-bucket-cors --bucket <BUCKET_NAME>
aws s3api get-bucket-policy --bucket <BUCKET_NAME>
```

### Browser

Verify:

- Website loads through EC2 Public IP
- CSS and JavaScript load
- Movie cards display
- Video player opens
- Video streams from S3
- Seeking and playback work
- No CORS errors
- No 403 or 404 responses

## Common Troubleshooting

### Video Returns 403

Check:

- Bucket Policy
- Block Public Access
- Correct object URL
- Object exists
- Resource ARN includes `/videos/*`

### Video Returns 404

Check exact object key:

```bash
aws s3 ls s3://<BUCKET_NAME>/videos/
```

S3 object names are case-sensitive.

### CORS Error

Verify:

- CORS JSON is valid
- `GET` and `HEAD` are allowed
- Website origin is allowed
- Browser cache is cleared

### Video Downloads Instead of Playing

Set:

```text
Content-Type: video/mp4
```

Do not use:

```text
application/octet-stream
```

### Seeking Does Not Work

Check for:

```text
Accept-Ranges: bytes
206 Partial Content
```

### NGINX Site Not Loading

```bash
sudo nginx -t
sudo journalctl -u nginx --no-pager -n 100
sudo tail -100 /var/log/nginx/error.log
```

## Cleanup

Delete or release:

1. EC2 instance
2. Elastic IP, if created
3. Security Group
4. S3 objects
5. S3 bucket
6. Route 53 records
7. Unused key pair
8. CloudFront distribution, if created

Empty bucket:

```bash
aws s3 rm s3://<BUCKET_NAME>/ --recursive
```

Delete bucket:

```bash
aws s3api delete-bucket \
  --bucket <BUCKET_NAME> \
  --region ap-south-1
```

## 20 Interview Questions and Answers

### 1. Why store videos in S3 instead of EC2?

S3 provides scalable, durable and cost-effective object storage. It prevents large video files from consuming EC2 disk space.

### 2. What does NGINX do?

NGINX serves the static website files and handles browser requests for HTML, CSS and JavaScript.

### 3. Does video traffic pass through EC2?

No. The browser directly requests the video object from S3 using its URL.

### 4. Why is CORS required?

The website and S3 object use different origins. CORS allows the browser to request S3 videos from the EC2-hosted website.

### 5. What is a Bucket Policy?

A Bucket Policy is a resource-based IAM policy controlling access to an S3 bucket and its objects.

### 6. Why set `Content-Type: video/mp4`?

It tells the browser the object is an MP4 video so it can play it correctly.

### 7. What are byte-range requests?

They allow the browser to request only part of a video, enabling seeking and efficient streaming.

### 8. What response code is common for range requests?

`206 Partial Content`.

### 9. Is a public S3 bucket recommended for production?

No. A private bucket behind CloudFront with Origin Access Control and signed URLs is safer.

### 10. Why use an Elastic IP?

A normal EC2 Public IP can change after stop/start. An Elastic IP provides a stable address.

### 11. How can a domain point to EC2?

Create a DNS A record pointing to the EC2 Elastic IP.

### 12. How do you enable HTTPS?

Use NGINX with Let's Encrypt or place an ALB with ACM in front of EC2.

### 13. What happens if the website uses HTTPS but the video URL uses HTTP?

The browser blocks it as mixed content.

### 14. How do you confirm the video comes from S3?

Use Browser Developer Tools and inspect the Media request host.

### 15. What causes S3 403 errors?

Public access blocks, missing Bucket Policy, incorrect ARN, private object, or invalid URL.

### 16. What causes S3 404 errors?

Incorrect bucket name, object key, folder path or filename case.

### 17. How do you reduce video delivery latency?

Use Amazon CloudFront as a CDN in front of S3.

### 18. How do you protect paid video content?

Use CloudFront signed URLs or signed cookies, authentication and a private S3 bucket.

### 19. How can this project become highly available?

Place multiple EC2 instances behind an ALB and use an Auto Scaling Group.

### 20. How would you improve this architecture for production?

Use private S3, CloudFront, HTTPS, signed URLs, ALB, Auto Scaling, Route 53, WAF, logging, monitoring, CI/CD and infrastructure as code.
