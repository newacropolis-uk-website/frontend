# New Acropolis UK frontend  [![Build Status](https://travis-ci.org/NewAcropolis/frontend.svg?branch=master)](https://travis-ci.org/NewAcropolis/frontend)

## Using Makefile

Run `Make` to list available commands

## Adding secrets

Make a copy of `app.yaml` to `app-dev.yaml` and add secrets as environment vars to `app-dev.yaml`

```
env_variables:
  SECRET_KEY: <secret key>
  API_BASE_URL: <new acropolis api url>
  FRONTEND_BASE_URL: <frontend base url>
  ADMIN_CLIENT_ID: <admin client id - should match api>
  ADMIN_CLIENT_SECRET: <admin secret - should match api>
  AUTH_USERNAME: <basic auth username>
  AUTH_PASSWORD: <basic auth password>
```

Then run `make deploy`, this will add the env vars to the datastore.

Pushing changes to the github repo will trigger an automatic deployment onto appengine.
