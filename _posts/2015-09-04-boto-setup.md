---
layout: post
tags : ["AWS", "Python"]
title : "Use Amazon Machine Learning in Python"
---

A short note on setting up Python SDK for Amazon Machine Learning.

[Boto][1] is the official AWS SDK for Python, which can be installed
via `pip`:

# Install boto

    pip install boto3

If only for the current user, append `--user`.

# AWS Credentials

Appropriate credentials are required to access AWS services. AWS differentiates
two types of credentials: root credentials and IAM credentials.  Root
credentials are associated with AWS accounts and have full access to all
resources. A maximum of two root keys are allowed at a time. On the other end of
the spectrum, IAM (Identity and Authentication Management) credentials are
analogous to user (in contrast to root) accounts in a Unix system, which are
created by a root account and their capabilities are dynamically managed. AWS
advocates the usage of IAM credentials for security considerations. Of course,
one can still create and use root credentials, however, if they will.

To access AWS API through `boto`, one needs proper credentials files set up. The
first step of doing this is to create a user (if not already created) and
download the access key.

- To manage IAM credentials, use IAM console.
- To manage root credentials, see [this][2]

There are at least three ways to configure credential files for `boto`. For
instance, put the credential file downloaded from IAM at `~/.aws/credentials`,


```shell
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Another `~/.aws/config` file is required for other specifications, e.g. regions.

```shell
[default]
region=us-east-1
```

# Using boto3

To verify your credentials and other configurations are correct, run a minimal
boto3 application this like,

```python
import boto3
s3 = boto3.resource('s3')
# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
```

Boto has very nice [documentation][3] for ML APIs. It's easy to get started.


[1]:https://aws.amazon.com/sdk-for-python/
[2]:http://docs.aws.amazon.com/general/latest/gr/getting-aws-sec-creds.html
[3]:http://boto3.readthedocs.org/en/latest/reference/services/machinelearning.html
