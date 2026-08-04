# Part 5 — Amazon S3 Static Website Hosting

[← Part 4](README_PART4.md) | [Next: Part 6 →](README_PART6.md)

## Objective

Host a separate static version of the website directly from an Amazon S3 bucket.

S3 Static Website Hosting supports client-side files such as:

- HTML
- CSS
- JavaScript
- Images

It does not execute PHP, Python, Java or server-side applications.

## Step 1 — Create a Globally Unique Bucket

Open:

```text
S3 Console → Create bucket
```

Example:

```text
Bucket name: raghav-project-04-static-site-2026-unique
AWS Region: ap-south-1
```

The bucket name must be globally unique.

## Step 2 — Upload Website Files

Upload the contents of the `website` directory:

```text
index.html
style.css
script.js
```

Do not upload only the parent folder unless the object paths match your HTML references.

AWS CLI alternative:

```bash
aws s3 sync ../website/ s3://<BUCKET_NAME>/ --delete
```

## Step 3 — Enable Static Website Hosting

Open:

```text
S3 Bucket → Properties → Static website hosting → Edit
```

Configure:

```text
Static website hosting: Enable
Hosting type: Host a static website
Index document: index.html
Error document: index.html
```

Save changes.

Record the website endpoint shown by S3.

## Step 4 — Configure Public Access for the Lab

Open:

```text
Permissions → Block public access → Edit
```

For this public training website, clear the required Block Public Access settings and acknowledge the warning.

> Never make a bucket public when it contains private, confidential or regulated data.

## Step 5 — Add the Bucket Policy

Replace `<BUCKET_NAME>`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForStaticWebsite",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/*"
    }
  ]
}
```

Open:

```text
Permissions → Bucket policy → Edit
```

Paste the policy and save.

## Step 6 — Open the Website Endpoint

The endpoint format varies by region. Copy it from the S3 console.

Example:

```text
http://<BUCKET_NAME>.s3-website.ap-south-1.amazonaws.com
```

Verify:

- HTML loads
- CSS is applied
- JavaScript works
- Browser Network tab shows HTTP 200 for required files
- No object returns 403 or 404

## Step 7 — Validate with AWS CLI

List objects:

```bash
aws s3 ls s3://<BUCKET_NAME>/ --recursive
```

Check configuration:

```bash
aws s3api get-bucket-website --bucket <BUCKET_NAME>
aws s3api get-public-access-block --bucket <BUCKET_NAME>
aws s3api get-bucket-policy --bucket <BUCKET_NAME>
```

## Step 8 — Update the Website

After editing local files:

```bash
aws s3 sync ../website/ s3://<BUCKET_NAME>/ --delete
```

Hard refresh:

```text
Ctrl + F5
```

## Important Limitation

The EC2 version dynamically displays instance information. S3 has no EC2 instance metadata, so the S3 website displays a static hosting message instead.

## Production Improvement

For a production static website, prefer:

```text
Users
  ↓
Amazon CloudFront
  ↓
Private S3 Bucket
```

Benefits:

- HTTPS
- Custom domain
- CDN caching
- Origin Access Control
- Private bucket
- AWS WAF integration

## Troubleshooting

### `403 Forbidden`

Check:

- Block Public Access configuration
- Bucket policy ARN
- Object exists
- Correct website endpoint is used
- Object ownership and policy permit read access

### `404 Not Found`

Check:

```text
index.html
```

The filename is case-sensitive.

### CSS or JavaScript Does Not Load

Use relative paths:

```html
<link rel="stylesheet" href="./style.css">
<script src="./script.js"></script>
```

Check browser Developer Tools → Network.

### REST Endpoint Downloads or Displays XML

Use the S3 **website endpoint**, not the normal S3 REST object URL.

## Part 5 Checklist

- [ ] Unique S3 bucket created
- [ ] Website files uploaded
- [ ] Static Website Hosting enabled
- [ ] Index document configured
- [ ] Public access configured for lab
- [ ] Bucket policy added
- [ ] Website endpoint copied
- [ ] HTML, CSS and JS verified
- [ ] No 403 or 404 errors
- [ ] Production CloudFront improvement understood

[Next: Part 6 — Verification, Cleanup and Troubleshooting →](README_PART6.md)
