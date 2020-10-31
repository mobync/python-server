# Mobync





If error:

```
Is the server running locally and accepting
connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
```

run:

```
brew services stop postgresql
rm /usr/local/var/postgres/postmaster.pid # adjust path accordingly to your install
brew services start postgresql
```

if doesn't work, try:

```
rm -rf /usr/local/var/postgres && initdb /usr/local/var/postgres -E utf8
```

