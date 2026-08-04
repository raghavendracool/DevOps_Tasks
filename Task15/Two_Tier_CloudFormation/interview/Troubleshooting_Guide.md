# Task 15 — Troubleshooting Guide

## Stack Failure Path

```text
Stack status failed?
  ↓
Describe stack events
  ↓
Find first CREATE_FAILED resource
  ↓
Check reason and dependent resources
  ↓
Correct template or parameter
  ↓
Validate and redeploy
```

## Application Failure Path

```text
ALB DNS resolves?
  ↓
Listener exists?
  ↓
Target registered?
  ↓
Target healthy?
  ↓
Web SG allows ALB SG?
  ↓
NGINX running?
  ↓
User Data completed?
```

## Useful Commands

```bash
sudo cloud-init status --long
sudo tail -200 /var/log/cloud-init-output.log
sudo systemctl status nginx --no-pager
sudo nginx -t
curl -I http://localhost
```

## Common CloudFormation Errors

- `ROLLBACK_COMPLETE`
- `AlreadyExists`
- `InvalidKeyPair.NotFound`
- `InsufficientCapabilities`
- `Resource handler returned message`
- Elastic IP quota exceeded
- Unsupported Availability Zone
- Invalid Security Group reference
- Target health timeout

## Production Improvements

- CI/CD template validation
- `cfn-lint`
- CloudFormation Guard
- Change Sets
- Drift detection
- Nested stacks
- StackSets
- Launch Templates
- Auto Scaling
- Session Manager
- HTTPS and WAF
