data "aws_availability_zones" "available" { state = "available" }

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = { Name = "${var.project_name}-vpc", Project = var.project_name }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = { Name = "${var.project_name}-igw" }
}

locals {
  public_cidrs = ["10.0.1.0/24","10.0.2.0/24"]
  app_cidrs    = ["10.0.11.0/24","10.0.12.0/24"]
  db_cidrs     = ["10.0.21.0/24","10.0.22.0/24"]
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = local.public_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = { Name = "${var.project_name}-public-${count.index+1}" }
}
resource "aws_subnet" "app" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = local.app_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
  tags = { Name = "${var.project_name}-app-${count.index+1}" }
}
resource "aws_subnet" "db" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = local.db_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
  tags = { Name = "${var.project_name}-db-${count.index+1}" }
}

resource "aws_route_table" "public" { vpc_id = aws_vpc.main.id tags = { Name = "${var.project_name}-public-rt" } }
resource "aws_route" "public" { route_table_id = aws_route_table.public.id destination_cidr_block = "0.0.0.0/0" gateway_id = aws_internet_gateway.main.id }
resource "aws_route_table_association" "public" { count = 2 subnet_id = aws_subnet.public[count.index].id route_table_id = aws_route_table.public.id }

resource "aws_eip" "nat" { domain = "vpc" depends_on = [aws_internet_gateway.main] }
resource "aws_nat_gateway" "main" { allocation_id = aws_eip.nat.id subnet_id = aws_subnet.public[0].id }
resource "aws_route_table" "app" { vpc_id = aws_vpc.main.id tags = { Name = "${var.project_name}-app-rt" } }
resource "aws_route" "app" { route_table_id = aws_route_table.app.id destination_cidr_block = "0.0.0.0/0" nat_gateway_id = aws_nat_gateway.main.id }
resource "aws_route_table_association" "app" { count = 2 subnet_id = aws_subnet.app[count.index].id route_table_id = aws_route_table.app.id }
resource "aws_route_table" "db" { vpc_id = aws_vpc.main.id tags = { Name = "${var.project_name}-db-rt" } }
resource "aws_route_table_association" "db" { count = 2 subnet_id = aws_subnet.db[count.index].id route_table_id = aws_route_table.db.id }
