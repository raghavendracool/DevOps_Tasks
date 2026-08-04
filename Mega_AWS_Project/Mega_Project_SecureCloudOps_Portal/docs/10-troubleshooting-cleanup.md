# 10. Troubleshooting and Cleanup

## ALB 503

- Check target health
- Check app container
- Check NGINX
- Check App SG from ALB SG

## Backend DB Failure

- Check RDS state
- Check RDS SG from App SG
- Check secret
- Check database and user grants

## Upload Failure

- Check instance role
- Check bucket name
- Check S3 policy
- Check object size

## Cleanup

```bash
cd infra/terraform
terraform destroy
```

Then verify:

- NAT Gateway deleted
- Elastic IP released
- ALB deleted
- RDS deleted or snapshot retained
- S3 bucket emptied
- CloudWatch logs reviewed
