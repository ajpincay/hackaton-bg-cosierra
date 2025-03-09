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
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_subnet" "eks-subnet-a" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_subnet" "eks-subnet-b" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-west-2b"

  tags = {
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