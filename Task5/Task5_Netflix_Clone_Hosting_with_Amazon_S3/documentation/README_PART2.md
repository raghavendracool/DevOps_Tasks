# Part 2 — S3 Bucket, Video Upload, Bucket Policy and CORS

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the S3 Bucket

Open:

```text
Amazon S3 → Create bucket
```

Configure:

```text
Bucket name: raghav-project-05-netflix-videos-<unique>
Region: ap-south-1
Object Ownership: Bucket owner enforced
```

## Step 2 — Create a Videos Folder

Inside the bucket, create:

```text
videos/
```

Upload your MP4 files:

```text
videos/movie1.mp4
videos/movie2.mp4
videos/movie3.mp4
```

AWS CLI alternative:

```bash
aws s3 cp movie1.mp4 s3://<BUCKET_NAME>/videos/
aws s3 cp movie2.mp4 s3://<BUCKET_NAME>/videos/
aws s3 cp movie3.mp4 s3://<BUCKET_NAME>/videos/
```

## Step 3 — Set Correct Content Type

MP4 objects should use:

```text
Content-Type: video/mp4
```

AWS CLI:

```bash
aws s3 cp movie1.mp4 \
  s3://<BUCKET_NAME>/videos/movie1.mp4 \
  --content-type video/mp4
```

## Step 4 — Configure Public Read for Training

For this beginner project, videos are publicly readable.

Disable the required Block Public Access settings for this bucket.

Add this Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadVideoObjects",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/videos/*"
    }
  ]
}
```

Replace `<BUCKET_NAME>`.

> Do not store private or confidential videos in a public bucket.

## Step 5 — Configure CORS

Open:

```text
S3 Bucket → Permissions → Cross-origin resource sharing
```

Add:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": [
      "Accept-Ranges",
      "Content-Length",
      "Content-Range",
      "Content-Type"
    ],
    "MaxAgeSeconds": 3000
  }
]
```

For production, replace `"*"` with your real domain.

## Step 6 — Copy Video Object URLs

Example:

```text
https://<BUCKET_NAME>.s3.ap-south-1.amazonaws.com/videos/movie1.mp4
```

Test in a browser.

## Step 7 — Verify Video Range Requests

Streaming works better when S3 responds to byte-range requests.

Test:

```bash
curl -I \
  -H "Range: bytes=0-1023" \
  https://<BUCKET_NAME>.s3.ap-south-1.amazonaws.com/videos/movie1.mp4
```

Expected response may include:

```text
HTTP/1.1 206 Partial Content
Accept-Ranges: bytes
Content-Type: video/mp4
```

## Production Security Option

Instead of public S3 objects, use:

- CloudFront
- Private S3 bucket
- Origin Access Control
- Signed URLs or signed cookies
- HTTPS
- AWS WAF

## Checklist

- [ ] S3 bucket created
- [ ] Videos uploaded
- [ ] `Content-Type` set to `video/mp4`
- [ ] Public access configured for lab
- [ ] Bucket Policy added
- [ ] CORS configured
- [ ] Video URLs copied
- [ ] Video URL opens successfully
