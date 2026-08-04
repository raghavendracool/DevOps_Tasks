output "alb_dns_name" { value = aws_lb.main.dns_name }
output "rds_endpoint" { value = aws_db_instance.main.address sensitive = true }
output "s3_bucket_name" { value = aws_s3_bucket.files.id }
output "bastion_public_ip" { value = aws_instance.bastion.public_ip }
output "sns_topic_arn" { value = aws_sns_topic.alerts.arn }
