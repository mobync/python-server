<div align="center">
<p>
    <img width="80" src="https://raw.githubusercontent.com/mobync/python-server/master/examples/in_memory_server_example/example_data/images/logo-round.png">
</p>
<h1>The Mobync Python Lib</h1>
</div>

<div align="center">

[![Build Status](https://travis-ci.com/mobync/python-server.svg?branch=master)](https://travis-ci.com/mobync/python-server)

</div>

## Introduction

Mobync is a synchronization library aimed to facilitate online-offline sync between multiple devices for any frontend, any backend, and any database.

This repository implements mobync server in python, that means you can start using mobync sync on your python backend regardless of which backend you might be using, or even which database.

As mobync aims to provide online-offline sync between client and server, you will need to use mobync library both on your frontend application and backend.

Currently mobync has a client dart implementation and a server python implementation. That means you can plug mobync on your flutter app and provide online-offline synchronization.

### Online-offline synchronization

Online-offline synchronization means that your app will work seamlessly both online and offline, the user can use without noticing any difference, and you can implement your app not worrying about this when using mobync.

Mobync will automatically make your app store your changes locally on your app's database when the user has no connection, and automatically sync the data to the backend when the user has internet.

### Multiple devices support

Mobync is a protocol that allows mobile applications running on distributed clients to get synced to a single source of truth to manage users’ data using any storage type. Mobync users Dart and Flutter to implement this protocol and communicate to a web server written in Python.




## Mobync Flutter Server Package

Using Mobync, you will wrap your database operations in such a way that any local data will get synced to a remote server, what will allow users from multiple clients to have an offline-online experience.



#### Postgres implementation
