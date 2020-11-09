# Mobync

[![Build Status](https://travis-ci.com/mobync/python-server.svg?branch=master)](https://travis-ci.com/mobync/python-server)

## Introduction

Mobync is a protocol that allows mobile applications running on distributed clients to get synced to a single source of truth to manage users’ data using any storage type. Mobync users Dart and Flutter to implement this protocol and communicate to a web server written in Python.

## Mobync Flutter Server Package

Using Mobync, you will wrap your database operations in such a way that any local data will get synced to a remote server, what will allow users from multiple clients to have an offline-online experience.

## Run tests

```buildoutcfg
python3 -m unittest test
```

#### Postgres implementation
