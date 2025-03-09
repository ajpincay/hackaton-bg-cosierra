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
    Name        = "cosierra-vpc"
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

resource "aws_route_table" "eks_public_route_table" {
  vpc_id = aws_vpc.eks-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cosierra-igw.id
  }

  tags = {
    Name        = "cosierra-public"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_route_table_association" "public-associantion" {
  subnet_id      = aws_subnet.eks-subnet-public.id
  route_table_id = aws_route_table.eks_public_route_table.id
}

resource "aws_subnet" "eks-subnet-public" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name        = "cosierra-public"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_subnet" "eks-subnet-private" {
  vpc_id            = aws_vpc.eks-vpc.id
  cidr_block        = "10.0.2.0/24"

  tags = {
    Name        = "cosierra-private"
    Environment = var.env
    Solution    = var.solutionName
  }
}

resource "aws_eks_cluster" "cosierra-eks-cluster" {
  name     = "cosierra-eks-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  vpc_config {
    subnet_ids = [
      aws_subnet.eks-subnet-public.id,
      aws_subnet.eks-subnet-private.id
    ]
  }

  tags = {
    Environment = var.env
    Solution    = var.solutionName
  }
}

data "aws_eks_cluster" "k8s" {
  name = aws_eks_cluster.cosierra-eks-cluster.name
}

data "aws_eks_cluster_auth" "k8s" {
  name = aws_eks_cluster.cosierra-eks-cluster.name
}


resource "aws_iam_policy" "lb_controller_policy" {
  name        = "AWSLoadBalancerControllerIAMPolicy"
  description = "IAM policy for the AWS Load Balancer Controller"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "acm:DescribeCertificate",
          "acm:ListCertificates",
          "acm:RequestCertificate",
          "acm:DeleteCertificate",
          "acm:RenewCertificate",
          "elasticloadbalancing:CreateLoadBalancer",
          "elasticloadbalancing:DeleteLoadBalancer",
          "elasticloadbalancing:DescribeLoadBalancers",
          "elasticloadbalancing:ModifyLoadBalancerAttributes",
          "elasticloadbalancing:CreateTargetGroup",
          "elasticloadbalancing:DeleteTargetGroup",
          "elasticloadbalancing:DescribeTargetGroups",
          "elasticloadbalancing:DescribeLoadBalancerAttributes",
          "elasticloadbalancing:RegisterTargets",
          "elasticloadbalancing:DeregisterTargets",
          "elasticloadbalancing:ModifyTargetGroup",
          "elasticloadbalancing:ModifyTargetGroupAttributes",
          "elasticloadbalancing:DescribeListeners",
          "elasticloadbalancing:CreateListener",
          "elasticloadbalancing:DeleteListener",
          "elasticloadbalancing:ModifyListener",
          "elasticloadbalancing:CreateRule",
          "elasticloadbalancing:DeleteRule",
          "elasticloadbalancing:ModifyRule",
          "elasticloadbalancing:DescribeRules",
          "elasticloadbalancing:DescribeSSLPolicies",
          "elasticloadbalancing:SetSubnets",
          "elasticloadbalancing:SetSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeVpcs",
          "iam:PassRole",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "service-discovery:CreateService",
          "service-discovery:DeleteService",
          "service-discovery:UpdateService",
          "service-discovery:GetService",
          "service-discovery:ListServices",
          "service-discovery:RegisterInstance",
          "service-discovery:DeregisterInstance",
          "service-discovery:ListInstances",
          "service-discovery:GetInstance",
          "service-discovery:ListNamespaces",
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "eks_cluster_role" {
  name = "eks-cluster-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy" #aws_iam_policy.lb_controller_policy.arn
  role       = aws_iam_role.eks_cluster_role.name
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
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
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