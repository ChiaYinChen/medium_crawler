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

---

## Docker

Build docker image

```
$ docker build -t <image name>:<image tag> . --no-cache
```

Build docker container

```
$ docker run --rm -it -d --name <container name> <image name>:<image tag>
```

Run a command in a running container

```
$ docker exec -it <container name> sh
```
