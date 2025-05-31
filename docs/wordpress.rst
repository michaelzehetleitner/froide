WordPress Integration via OAuth2
===============================

This guide shows how to expose Froide functionality to a separate WordPress site.
It assumes that the Froide backend with the Django services continues to run on
your server.

Create an OAuth2 application
----------------------------

1. Log in to the Django admin of your Froide instance and open ``/account/applications/register/``.
2. Register a new application and set the ``allowed_origins`` field to the domain
   of your WordPress site so that browsers can send cross‑origin requests.
3. Note the ``client_id`` and ``client_secret`` for later use.

Signing in from WordPress
-------------------------

Use the OAuth2 Authorization Code flow (optionally with PKCE) to obtain an
access token.  The authorization endpoint is ``/oauth2/authorize/`` and the token
endpoint is ``/oauth2/token/``.  Store the token on the WordPress side and send
it as a Bearer token when calling the API.

Creating and managing requests
------------------------------

- **Create FOI request** – ``POST /api/v1/request/`` with the fields defined in
  the API schema.  The access token must include the ``make:request`` scope.
- **List own requests** – ``GET /api/v1/request/?user=<your user id>`` using the
  ``read:request`` scope to retrieve private requests.
- **Escalate a request** – ``POST /api/v1/request/<id>/escalate/`` with the
  escalation message parameters.  This uses the new API action added in this
  repository.

The WordPress plugin or theme code can call these endpoints with ``fetch`` or
WordPress' HTTP client and display the results on the site.
