# Part 1 — Introduction, Architecture and Prerequisites

[← Main](../README.md) | [Next →](README_PART2.md)

![Architecture](../infographic.png)

## Objectives
- Create an AMI from an Ubuntu EC2 instance.
- Copy the AMI to another AWS Region.
- Launch EC2 from the copied AMI.
- Detach a non-root EBS volume.
- Attach and verify a replacement volume.
- Delete the old volume only after validation.

## Services
| Service | Purpose |
|---|---|
| EC2 | Ubuntu compute |
| EBS | Root and data block storage |
| AMI | Reusable instance image |
| S3 | AWS-managed backing for regional AMI copy |
| IAM | Permissions |
| VPC | EC2 networking |

## Example Regions
```text
Source: ap-south-1
Destination: us-east-1
```

## Prerequisites
AWS account, Ubuntu key pair, VPC/public subnet, SSH client, and EC2/EBS/AMI permissions.

> EBS volumes can attach only to EC2 instances in the same Availability Zone.
