# fantasy-football

## Prerequisites

Before proceeding, install the following components on your system:

- [Task](https://taskfile.dev/installation/)
- [uv](https://github.com/astral-sh/uv)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

## Setup

To save the data to DynamoDB, you'll first need to configure your AWS credentials:

```shell
aws configure
```

## Usage

To scrape the rankings, simply run the script:

```shell
task run
```
