# Task 8 — Interview Guide

## 1. Explain the architecture.

The Flask application runs on EC2 behind NGINX and Gunicorn. Files are stored in a private S3 bucket under user-specific prefixes. EC2 accesses S3 through an IAM role.

## 2. Why use S3 instead of EC2 storage?

S3 is durable, scalable and independent of the EC2 lifecycle.

## 3. Why use an IAM role?

It avoids storing long-term AWS access keys on the server.

## 4. How is user isolation implemented?

Every S3 key begins with `users/<username>/`, and the application validates the logged-in username before every operation.

## 5. Is prefix isolation alone enough for production?

No. Add stronger authorization, audit logging, Cognito or an identity provider, and possibly user-scoped presigned URLs.

## 6. How are passwords protected?

They are stored using Werkzeug password hashing rather than plaintext.

## 7. Why keep the S3 bucket private?

Files are personal and should never be directly public.

## 8. How do downloads work?

The sample fetches the object through Flask and returns it as an attachment.

## 9. How would you improve large-file downloads?

Generate short-lived presigned URLs so the browser downloads directly from S3.

## 10. How would you improve uploads?

Use multipart uploads or presigned POST/PUT uploads directly to S3.

## 11. Why enable versioning?

It helps recover overwritten or deleted objects.

## 12. How do you prevent malicious uploads?

Restrict extensions, validate MIME types, limit size, scan files and block executable content.

## 13. How do you make the application highly available?

Use an ALB, Auto Scaling Group, multiple EC2 instances and shared session/database storage.

## 14. Why is SQLite not ideal for multiple EC2 instances?

It is local to one server and cannot safely act as a shared production database.

## 15. Which authentication service is better for production?

Amazon Cognito or an enterprise identity provider.

## 16. How would you monitor it?

CloudWatch logs and metrics, S3 access logs, CloudTrail, NGINX logs and application alarms.

## 17. How do you encrypt files?

Use SSE-S3 or SSE-KMS at rest and HTTPS in transit.

## 18. How do you control costs?

Use lifecycle policies, Intelligent-Tiering, direct S3 transfers and remove unused EC2 resources.

## 19. How do you support folders?

Folders are represented by S3 key prefixes.

## 20. How would you share a file securely?

Create a short-lived presigned URL with explicit authorization.
