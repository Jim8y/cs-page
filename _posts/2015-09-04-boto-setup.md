---
layout: post
tags : ["aws", "Python"]
title : "Use Amazon Machine Learning in Python"
---

# AWS Credentials

Appropriate credentials are required to access aws service API. Amazon Web Service
differentiates two types of credentials: root credentials and IAM credentials.
Root credentials are associated with aws accounts and have full access to all
resources. A maximum of two keys are allowed at a time. On the other end of
spectrum, IAM (Identity and Authentication Management) credentials are analogous
to user accounts in a Unix system, which are created by a root account and their
capabilities can be dynamically managed. AWS advocates the usage of IAM
credentials for security consideration. Of course, one can still create and use
root credentials, however, if they will.

To access aws API through boto, one needs proper credentials set up. The first
step of doing this is to create a user (if not already created) and download the
access key.

- To manage IAM credentials, use IAM console.
- To manage root credentials, see [this](http://docs.aws.amazon.com/general/latest/gr/getting-aws-sec-creds.html)

There are multiple ways to configure credential file for Boto's usage. For
instance, put the credential file downloaded from IAM at `~/.aws/credentials`,

    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY

Not sure if it's mandatory but Boto document suggest doing so

    [default]
    region=us-east-1

# Install Boto

    pip install boto3

If for current user only, append `--user`.

# Using Boto3

To verify your credentials and other configurations are correct, run a minimal
boto3 script this like,

    import boto3
    s3 = boto3.resource('s3')
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)


# Amazon Machine Learning API

    import boto3

    client = boto3.client('machinelearning')
