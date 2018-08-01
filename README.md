# New Acropolis UK frontend  [![Build Status](https://travis-ci.org/NewAcropolis/frontend.svg?branch=master)](https://travis-ci.org/NewAcropolis/frontend)

## Using Makefile

Run `Make` to list available commands

## Adding secrets

Add secrets as environment vars to `app.yaml`

Then run `make deploy`, this will add the env vars to the datastore.

Then remove the secret environment vars.
