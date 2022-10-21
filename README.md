# rcos i/o

## Running

First, make sure that you have `flask` installed. We are using a virtual environment
to manage the project environment & dependencies.

```
. venv/bin/activate
flask run
```

In addition to this, you will need `HASURA_SECRET` set in order to connect to Hasura. To do this,
simply make an `.env` file in the project root with the following contents:

```
HASURA_SECRET=<secret token>
```
