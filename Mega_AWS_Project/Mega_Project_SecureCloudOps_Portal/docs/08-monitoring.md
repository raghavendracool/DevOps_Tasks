# 8. Monitoring and Grafana

## CloudWatch Metrics

Namespace:

```text
SecureCloudOps
```

Metrics:

- ComplianceScore
- NonCompliantResources
- SecurityEvents
- FileClassificationSuccess
- FileClassificationFailure
- ApplicationErrors
- UploadCount

## Infrastructure Metrics

- ALB request count
- ALB target response time
- ALB 4XX and 5XX
- EC2 CPU
- ASG desired/in-service capacity
- RDS CPU and connections
- Lambda errors and duration

## Grafana

Import:

```text
monitoring/grafana/dashboard.json
```

Alerts:

- Compliance score below 100
- SecurityEvents >= 1
- Lambda Errors >= 1
- ALB 5XX > threshold
- RDS connections high
