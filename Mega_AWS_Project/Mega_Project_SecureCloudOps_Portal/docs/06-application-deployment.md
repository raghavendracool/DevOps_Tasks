# 6. Application Deployment

## EC2 Bootstrapping

Terraform renders:

```text
infra/terraform/user_data.sh.tftpl
```

The script:

- Installs Docker
- Pulls application source
- Creates environment file
- Starts backend and frontend containers
- Configures NGINX
- Starts CloudWatch Agent
- Signals readiness

## Application URL

```bash
terraform output -raw alb_dns_name
```

Open:

```text
http://<ALB_DNS_NAME>
```

## Verify Multiple Instances

```bash
for i in {1..10}; do
  curl -s http://<ALB_DNS_NAME>/api/instance
  echo
done
```

## Auto Scaling Test

```bash
sudo apt install stress-ng -y
stress-ng --cpu "$(nproc)" --cpu-load 100 --timeout 15m
```

Verify ASG activity in AWS Console or CLI.
