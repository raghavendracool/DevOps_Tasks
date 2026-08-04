data "aws_ssm_parameter" "ubuntu" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}

resource "aws_iam_role" "ec2" {
  name_prefix = "${var.project_name}-ec2-"
  assume_role_policy = jsonencode({
    Version="2012-10-17", Statement=[{Effect="Allow",Principal={Service="ec2.amazonaws.com"},Action="sts:AssumeRole"}]
  })
}
resource "aws_iam_role_policy_attachment" "ssm" {
  role = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
resource "aws_iam_role_policy" "s3" {
  role = aws_iam_role.ec2.id
  policy = jsonencode({
    Version="2012-10-17",
    Statement=[
      {Effect="Allow",Action=["s3:ListBucket"],Resource=aws_s3_bucket.files.arn},
      {Effect="Allow",Action=["s3:GetObject","s3:PutObject","s3:DeleteObject"],Resource="${aws_s3_bucket.files.arn}/*"}
    ]
  })
}
resource "aws_iam_instance_profile" "ec2" { role = aws_iam_role.ec2.name }

resource "aws_lb" "main" {
  name = "${var.project_name}-alb"
  load_balancer_type = "application"
  security_groups = [aws_security_group.alb.id]
  subnets = aws_subnet.public[*].id
}
resource "aws_lb_target_group" "app" {
  name = "${var.project_name}-tg"
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  health_check { path="/health" matcher="200" }
}
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port = 80
  protocol = "HTTP"
  default_action { type="forward" target_group_arn=aws_lb_target_group.app.arn }
}

resource "aws_launch_template" "app" {
  name_prefix = "${var.project_name}-"
  image_id = data.aws_ssm_parameter.ubuntu.value
  instance_type = var.instance_type
  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile { name = aws_iam_instance_profile.ec2.name }
  metadata_options { http_tokens="required" http_endpoint="enabled" }
  block_device_mappings {
    device_name="/dev/sda1"
    ebs { volume_size=20 volume_type="gp3" encrypted=true delete_on_termination=true }
  }
  user_data = base64encode(templatefile("${path.module}/user_data.sh.tftpl", {
    db_host=aws_db_instance.main.address
    db_user=var.db_username
    db_password=var.db_password
    bucket=aws_s3_bucket.files.id
    region=var.aws_region
  }))
}
resource "aws_autoscaling_group" "app" {
  min_size=var.min_size
  max_size=var.max_size
  desired_capacity=var.desired_capacity
  vpc_zone_identifier=aws_subnet.app[*].id
  target_group_arns=[aws_lb_target_group.app.arn]
  health_check_type="ELB"
  launch_template { id=aws_launch_template.app.id version="$Latest" }
}
resource "aws_autoscaling_policy" "cpu" {
  name="${var.project_name}-cpu70"
  autoscaling_group_name=aws_autoscaling_group.app.name
  policy_type="TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification { predefined_metric_type="ASGAverageCPUUtilization" }
    target_value=70
  }
}

resource "aws_instance" "bastion" {
  ami=data.aws_ssm_parameter.ubuntu.value
  instance_type="t3.micro"
  subnet_id=aws_subnet.public[0].id
  vpc_security_group_ids=[aws_security_group.bastion.id]
  key_name=var.key_name
  associate_public_ip_address=true
  tags={Name="${var.project_name}-bastion"}
}
