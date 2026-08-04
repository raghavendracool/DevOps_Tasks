resource "aws_security_group" "alb" {
  name = "${var.project_name}-alb-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port=80 to_port=80 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  egress { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
resource "aws_security_group" "bastion" {
  name = "${var.project_name}-bastion-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port=22 to_port=22 protocol="tcp" cidr_blocks=[var.admin_cidr] }
  egress { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
resource "aws_security_group" "app" {
  name = "${var.project_name}-app-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port=80 to_port=80 protocol="tcp" security_groups=[aws_security_group.alb.id] }
  ingress { from_port=22 to_port=22 protocol="tcp" security_groups=[aws_security_group.bastion.id] }
  egress { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
resource "aws_security_group" "rds" {
  name = "${var.project_name}-rds-sg"; vpc_id = aws_vpc.main.id
  ingress { from_port=3306 to_port=3306 protocol="tcp" security_groups=[aws_security_group.app.id] }
  egress { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
