# Project 03 — Amazon Machine Image and EBS Volume Management

![Task 3 Architecture](infographic.png)

Create an AMI from an Ubuntu EC2 instance, copy it to another AWS Region, launch from the copied AMI, and safely replace a non-root EBS volume.

## Documentation
1. [Introduction and Architecture](documentation/README_PART1.md)
2. [Prepare Ubuntu EC2 and Data Volume](documentation/README_PART2.md)
3. [Create and Copy the AMI](documentation/README_PART3.md)
4. [Replace the EBS Volume](documentation/README_PART4.md)
5. [Verification, Cleanup and Interview Q&A](documentation/README_PART5.md)

## Flow
```text
Ubuntu EC2 → Create AMI → Copy AMI cross-region → Launch destination EC2
     ↓
Detach old data EBS → Attach new EBS → Mount and verify → Delete old EBS
```
