# Project 05 — Netflix Clone Hosting with Amazon S3

![Task 5 Architecture](infographic.png)

This project deploys a Netflix-style website on an Ubuntu EC2 instance using NGINX while storing and streaming video files directly from Amazon S3.

## Documentation

1. [Part 1 — Introduction, Architecture and Prerequisites](documentation/README_PART1.md)
2. [Part 2 — S3 Bucket, Video Upload, Policy and CORS](documentation/README_PART2.md)
3. [Part 3 — EC2, NGINX and Website Deployment](documentation/README_PART3.md)
4. [Part 4 — Video Integration, Testing and Domain Access](documentation/README_PART4.md)
5. [Part 5 — Verification, Cleanup, Troubleshooting and Interview Questions](documentation/README_PART5.md)

## Project Flow

```text
Create S3 bucket
→ Upload MP4 video files
→ Configure object access and CORS
→ Launch Ubuntu EC2
→ Install NGINX
→ Deploy Netflix clone website
→ Add S3 video URLs to website
→ Access site using EC2 Public IP or domain
→ Verify videos stream directly from S3
```

## Folder Structure

```text
Task5_Netflix_Clone_Hosting_with_Amazon_S3/
├── README.md
├── infographic.png
├── documentation/
├── scripts/
└── website/
```
