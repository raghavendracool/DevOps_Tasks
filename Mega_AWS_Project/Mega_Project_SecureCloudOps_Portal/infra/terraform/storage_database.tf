resource "aws_s3_bucket" "files" {
  bucket_prefix = "${var.project_name}-files-"
  force_destroy = true
}
resource "aws_s3_bucket_versioning" "files" {
  bucket = aws_s3_bucket.files.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "files" {
  bucket = aws_s3_bucket.files.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}
resource "aws_s3_bucket_public_access_block" "files" {
  bucket = aws_s3_bucket.files.id
  block_public_acls=true
  block_public_policy=true
  ignore_public_acls=true
  restrict_public_buckets=true
}

resource "aws_db_subnet_group" "main" {
  name = "${var.project_name}-db-subnets"
  subnet_ids = aws_subnet.db[*].id
}
resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-mysql"
  engine = "mysql"
  engine_version = "8.4"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  storage_type = "gp3"
  storage_encrypted = true
  db_name = "securecloudops"
  username = var.db_username
  password = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible = false
  multi_az = false
  backup_retention_period = 7
  skip_final_snapshot = true
}
