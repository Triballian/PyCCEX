PyCCEX
=========

Python binding to the C-CEX API (https://c-cex.com/?id=api)

This is a minimalist implementation for a minimalist API.  C-CEX uses HTTP
GET requests for its API, with an API key included for some calls.  This API
assembles the query, fires it off to the server, and decodes the JSON
response into a Python data structure.

example.py is a similarly minimal example that returns the available trading
pairs.
