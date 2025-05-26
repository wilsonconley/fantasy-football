# fantasy-football

This application will scrape multiple fantasy football websites to gather
weekly rankings across various sources. The rankings and projected point values
will be averaged together in order to provide an unbiased, aggregated ranking
to help you set your lineups week to week.

The application currently pulls rankings from the following websites:

- [FantasyPros](https://www.fantasypros.com/)

Once the data has been collected, it will be sent to DynamoDB so it can be
stored and tracked.

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
