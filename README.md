# Medium Crawler

[![Build Status](https://travis-ci.com/ChiaYinChen/medium_crawler.svg?branch=master)](https://travis-ci.com/ChiaYinChen/medium_crawler)

## Installation

Install requirements

```
$ pipenv install
```

Install requirements for developing packages

```
$ pipenv install --dev
```

## Configurable variables

|  variable name                |   default value       | overridable |
| ----------------------------- | --------------------- | ----------- |
| PROXY                         | http://127.0.0.1:8787 | YES         |
| PROXY_ENABLED                 | FALSE                 | YES         |

## Usage

### Run a spider via `scrapy crawl`

```
Syntax: scrapy crawl medium <arguments>

Pass arguments to spider using the `-a` option.

Supported arguments:
    usernames: comma-separated writer's profile page names
    date: crawling date (YYYYMMDD)
    back: number of days to be crawled
    urls: comma-separated url list

* If `urls` is set, `usernames` will be ignored.
* If `date` is set, `back` will be ignored.
```

Usage examples:

```
# Retrieve data from certain writer's profile pages and a specific date on
$ scrapy crawl medium -a usernames=chiayinchen -a date=20180801

# Retrieve data from certain urls
$ scrapy crawl medium -a urls=https://medium.com/8045c82962e2/be290cd1f9d8
```

### Run a spider from a script

```
$ python medium_crawler/run.py --spider medium
```

## Running the tests

```
$ tox
```

---

# Docker

Pull docker image

```
$ docker pull chiayinchen/medium-crawler:<version>
```

Build docker container

```
$ docker run --rm -it -d --name <container_name> chiayinchen/medium-crawler:<version>
```

Run a command in a running container

```
$ docker exec -it <container_name> sh
```
