resource "aws_sns_topic" "alerts" { name="${var.project_name}-alerts" }

resource "aws_iam_role" "lambda" {
  name_prefix="${var.project_name}-lambda-"
  assume_role_policy=jsonencode({Version="2012-10-17",Statement=[{Effect="Allow",Principal={Service="lambda.amazonaws.com"},Action="sts:AssumeRole"}]})
}
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role=aws_iam_role.lambda.name
  policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
resource "aws_iam_role_policy" "lambda" {
  role=aws_iam_role.lambda.id
  policy=jsonencode({
    Version="2012-10-17",
    Statement=[
      {Effect="Allow",Action=["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:ListBucket"],Resource=[aws_s3_bucket.files.arn,"${aws_s3_bucket.files.arn}/*"]},
      {Effect="Allow",Action=["ec2:DescribeInstances","ec2:DescribeVolumes","iam:ListUsers","iam:ListAccessKeys"],Resource="*"},
      {Effect="Allow",Action=["cloudwatch:PutMetricData"],Resource="*"},
      {Effect="Allow",Action=["sns:Publish"],Resource=aws_sns_topic.alerts.arn}
    ]
  })
}
