# Medium Crawler

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
| PROXY_DEPTH                   | 0                     | YES         |

## Usage

Run a spider via `scrapy crawl`

```
$ scrapy crawl medium -a usernames=chiayinchen -a date=20180801
$ scrapy crawl medium -a urls=https://medium.com/8045c82962e2/be290cd1f9d8
```

Run a spider from a script

```
$ python medium_crawler/run.py --spider medium
```

---

# Docker

Build docker image

```
$ docker build -t medium-crawler:<version> . --no-cache
```

Build docker container

```
$ docker run --rm -it -d --name <container_name> medium-crawler:<version>
```

Run a command in a running container

```
$ docker exec -it <container_name> sh
```
