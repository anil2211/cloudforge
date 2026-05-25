resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "cloudforge-vpc"
  }
}

resource "aws_subnet" "public_1" {
  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
  }
}