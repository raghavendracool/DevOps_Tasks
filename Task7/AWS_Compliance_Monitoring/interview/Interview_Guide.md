# Task 7 — Interview Guide

## 1. Explain the architecture.

EventBridge Scheduler invokes Lambda every 15 minutes. Lambda uses EC2 APIs to inspect tags and EBS encryption, IAM APIs to inspect active key creation dates, writes a structured report to CloudWatch Logs and publishes violations to SNS.

## 2. Why use Lambda?

The checks are scheduled, stateless and short-running. Lambda avoids server management and is cost-effective for periodic scans.

## 3. Why is the Lambda timeout 30 seconds?

It is a task requirement. The code also checks remaining execution time and marks a partial scan rather than failing abruptly.

## 4. Why can 30 seconds be a limitation?

Large accounts, multiple regions and many IAM users may require more API calls than can finish within 30 seconds.

## 5. Why use paginators?

AWS list and describe APIs return paginated results. Without paginators, the function may inspect only the first page and miss resources.

## 6. How are required EC2 tags evaluated?

The function converts the tag list into a dictionary and verifies that every configured key exists with a non-empty value.

## 7. Are stopped instances checked?

Yes. They still exist and remain subject to the required-tag rule.

## 8. How is EBS encryption checked?

The function inspects the `Encrypted` boolean returned by `DescribeVolumes`.

## 9. How is access-key age calculated?

Current UTC time minus the key `CreateDate` returned by `ListAccessKeys`.

## 10. Does the function rotate keys?

No. It only detects and reports non-compliance. Automated rotation requires a controlled application update process.

## 11. Why mask the access-key ID?

It reduces exposure of credential identifiers in email and logs while retaining enough characters for correlation.

## 12. Why is IAM scanned only once?

IAM is global, unlike EC2 and EBS, which are regional.

## 13. How would you scale this across all regions?

Use regional worker Lambdas, Step Functions, SQS, AWS Config aggregators or an Organizations-based central compliance account.

## 14. Why use SNS?

SNS supports fan-out notifications to email, SMS, SQS, Lambda and HTTPS subscribers.

## 15. How would you avoid duplicate notifications?

Store finding state in DynamoDB, publish only on state changes and add a finding fingerprint.

## 16. How would you remediate missing tags?

Use approved defaults, resource-owner workflow, Systems Manager Automation or a separate remediation Lambda.

## 17. Can an unencrypted EBS volume be encrypted in place?

A common migration pattern is snapshot, encrypted snapshot copy, new encrypted volume, attachment and data validation rather than directly changing the existing volume.

## 18. How would you use AWS Config instead?

Use managed rules for encrypted volumes and required tags, plus custom rules where needed. Config provides resource history and compliance timelines.

## 19. What metrics should be monitored?

Lambda Errors, Duration, Throttles, Invocations, SNS delivery failures and the number of findings per rule.

## 20. How would you deploy safely?

Use CloudFormation, SAM, CDK or Terraform, versioned Lambda aliases, tests, least-privilege IAM and controlled rollout.
