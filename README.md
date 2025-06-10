# fantasy-football

This application will scrape multiple fantasy football websites to gather
weekly rankings across various sources. The rankings and projected point values
will be averaged together in order to provide an unbiased, aggregated ranking
to help you set your lineups week to week.

The application currently pulls rankings from the following websites:

- [FantasyPros](https://www.fantasypros.com/)

Once the data has been collected, it will be sent to DynamoDB so it can be
stored and tracked.

## Project Structure

The project consists of three main components:

- `scraper/`: Python-based scraper that collects fantasy football rankings
- `backend/`: Express.js server that serves the data to the frontend
- `frontend/`: React application that displays the rankings in a user-friendly interface

## Prerequisites

Before proceeding, install the following components on your system:

- [Task](https://taskfile.dev/installation/)
- [uv](https://github.com/astral-sh/uv)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Node.js](https://nodejs.org/) (v18 or later)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Setup

1. Configure AWS credentials:

```shell
aws configure
```

2. Install backend dependencies:

```shell
cd backend
npm install
```

3. Install frontend dependencies:

```shell
cd frontend
npm install
```

## Usage

1. To scrape new rankings:

```shell
task scrape
```

2. Start the backend server:

```shell
cd backend
npm start
```

3. Start the frontend UI:

```shell
cd frontend
npm start
```

The application will be available at http://localhost:3000
