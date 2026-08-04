# Project 04 — Highly Available and Scalable Web Application on AWS

![Project Architecture](infographic.png)

This folder contains the complete step-by-step documentation for deploying a highly available and scalable web application on AWS using Ubuntu EC2, Apache, an Application Load Balancer, an Auto Scaling Group, CloudWatch CPU target tracking, and Amazon S3 static website hosting.

## Documentation Order

1. [Part 1 — Introduction and Architecture](documentation/README_PART1.md)
2. [Part 2 — Launch Template, User Data and Apache](documentation/README_PART2.md)
3. [Part 3 — Target Group and Application Load Balancer](documentation/README_PART3.md)
4. [Part 4 — Auto Scaling and Stress Testing](documentation/README_PART4.md)
5. [Part 5 — Amazon S3 Static Website Hosting](documentation/README_PART5.md)
6. [Part 6 — Verification, Cleanup and Troubleshooting](documentation/README_PART6.md)
7. [Part 7 — Interview Questions and Answers](documentation/README_PART7.md)

## Included Files

```text
Task4_Highly_Available_Scalable_Web_Application/
├── README.md
├── infographic.png
├── documentation/
│   ├── README_PART1.md
│   ├── README_PART2.md
│   ├── README_PART3.md
│   ├── README_PART4.md
│   ├── README_PART5.md
│   ├── README_PART6.md
│   └── README_PART7.md
├── website/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── scripts/
    ├── user-data.sh
    └── cpu-stress-test.sh
```

> Complete the parts in sequence. Replace placeholder values such as repository URL, AMI ID, VPC, subnets, and security groups with values from your AWS account.
