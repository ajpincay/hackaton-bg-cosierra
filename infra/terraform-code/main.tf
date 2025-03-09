# AppConfiguration
resource "aws_appconfig_application" "ac-cosierra" {
  name        = "appConfig-cosierra"
  description = "Configuracion"

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_appconfig_configuration_profile" "cp-cosierra" {
  application_id = aws_appconfig_application.ac-cosierra.id
  description    = "Base Configuration Profile"
  name           = "base-configuration-profile"
  location_uri   = "hosted"

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_appconfig_hosted_configuration_version" "hc-cosierra" {
  application_id           = aws_appconfig_application.ac-cosierra.id
  configuration_profile_id = aws_appconfig_configuration_profile.cp-cosierra.configuration_profile_id
  content_type             = "application/json"
  description              = "Initial configuration version"
  content = jsonencode(
    { "feature_enabled" : true,
      "message" : "Hello, AppConfig!"
  })
}

# Database
resource "aws_db_instance" "db-cosierra" {
  allocated_storage    = 10
  db_name              = "cosierraDb"
  engine               = "mysql"
  engine_version       = "8.0"
  identifier           = "cosierra-db"
  instance_class       = "db.m5.large"
  username             = var.db-username
  password             = var.db-password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

# Container Registry
resource "aws_ecr_repository" "cosierra-ecr-backend" {
  name                 = "ecr-cosierra-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_ecr_repository" "cosierra-ecr-frontend" {
  name                 = "ecr-cosierra-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "cw-logs-cosierra" {
  name              = "cosierra-logs"
  retention_in_days = 7

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

# EKS
resource "aws_vpc" "eks-vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "cosierra-vpc"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_internet_gateway" "cosierra-igw" {
  vpc_id = aws_vpc.eks-vpc.id
  tags = {
    Name        = "cosierra-igw"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.eks-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cosierra-igw.id
  }

  tags = {
    Name = "cosierra-public"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_route_table_association" "public-associantion" {
  subnet_id      = aws_subnet.eks-subnet-a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private-associantion2" {
  subnet_id      = aws_subnet.eks-subnet-b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_eip" "nat-eip" {
  vpc = true

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_nat_gateway" "cosierra-nat-gw" {
  allocation_id = aws_eip.nat-eip.id
  subnet_id     = aws_subnet.eks-subnet-a.id

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_subnet" "eks-subnet-a" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Name = "cosierra-public"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_subnet" "eks-subnet-b" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-west-2b"

  tags = {
    Name = "cosierra-private"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_eks_cluster" "cosierra-eks-cluster" {
  name     = "cosierra-eks-cluster"
  role_arn = aws_iam_role.cosierra-eks-role.arn
  vpc_config {
    subnet_ids = [
      aws_subnet.eks-subnet-a.id,
      aws_subnet.eks-subnet-b.id
    ]
  }

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_iam_role" "cosierra-eks-role" {
  name = "cosierra-eks-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "eks.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
    }]
  })
}

data "aws_eks_cluster" "k8s" {
  name = aws_eks_cluster.cosierra-eks-cluster.name
}

data "aws_eks_cluster_auth" "k8s" {
  name = aws_eks_cluster.cosierra-eks-cluster.name
}

resource "aws_lb" "cosierra-lb" {
  name               = "cosierra-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.cosierra-sg.id]
  subnets            = [aws_subnet.eks-subnet-a.id, aws_subnet.eks-subnet-b.id]

  enable_deletion_protection = false

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_security_group" "cosierra-sg" {
  name        = "cosierra-lb-sg"
  description = "Allow HTTP and HTTPS traffic"
  vpc_id      = aws_vpc.eks-vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb_listener" "http-listener" {
  load_balancer_arn = aws_lb.cosierra-lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"

    forward {
      target_group {
        arn = aws_lb_target_group.cosierra-tg.arn
      }
    }
  }
}

#resource "aws_lb_listener" "https-listener" {
#  load_balancer_arn = aws_lb.cosierra-lb.arn
#  port              = 443
#  protocol          = "HTTPS"

#  ssl_policy = "ELBSecurityPolicy-2025"
#  #certificate_arn = 

#  default_action {
#    type = "forward"

#    forward {
#      target_group {
#        arn = aws_lb_target_group.cosierra-tg.arn
#      }
#    }
#  }
#}

resource "aws_lb_target_group" "cosierra-tg" {
  name     = "cosierra-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.eks-vpc.id

  health_check {
    path                = "/"
    interval            = "30"
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Resource Group
resource "aws_resourcegroups_group" "cosierra-prod-rg" {
  name = "cosierra-prod-rg"

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }

  resource_query {
    query = <<JSON
    {
      "ResourceTypeFilters": [
        "AWS::ECR::Repository",
        "AWS::AppConfig::ConfigurationProfile",
        "AWS::RDS::DBInstance",
        "AWS::Logs::LogGroup",
        "AWS::EKS::Cluster"
      ],
      "TagFilters": [
        {
          "Key": "Solution",
          "Values": [
            "${var.solutionName}"
          ]
        },
        {
          "Key": "Environment",
          "Values": [
            "${var.env}"
          ]
        }
      ]
    }
    JSON
  }
}
