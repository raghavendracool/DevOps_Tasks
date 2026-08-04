# Recommended Alarms

- ALB Target 5XX >= 5 in 5 minutes
- UnhealthyHostCount >= 1
- ASG InServiceInstances < desired
- EC2 CPU > 80%
- RDS CPU > 80%
- RDS DatabaseConnections > 80% of max
- Lambda Errors >= 1
- ComplianceScore < 100
- SecurityEvents >= 1
