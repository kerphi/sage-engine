# utils.py
# Author: Thomas MINIER - MIT License 2017-2018
from flask import Response
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from base64 import b64encode, b64decode
from json import dumps


def sort_qparams(v):
    """Sort query params as subject, predicate, object, page, as the current ldf-client require about this particular order..."""
    if v[0] == 'subject':
        return 0
    elif v[0] == 'predicate':
        return 1
    elif v[0] == 'object':
        return 2
    elif v[0] == 'page':
        return 3
    return 4


def secure_url(url):
    """Secure potentially ill formatted urls"""
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    qparams = parse_qs(query)
    query = urlencode(qparams, doseq=True)
    return urlunparse((scheme, netloc, path, params, query, fragment)).replace("%7E", "~")


def format_graph_uri(uri, server_url):
    """Format a GRAPH IRI if its belong to the same server than the current one"""
    if not server_url.endswith('/'):
        server_url += '/'
    if uri.startswith(server_url):
        index = uri.index(server_url)
        return uri[index + len(server_url):]
    return '_:UnkownGraph'


def format_marshmallow_errors(errors):
    """Format mashmallow validation errors in string format"""
    return dumps(errors, indent=2)


def encode_saved_plan(savedPlan):
    if savedPlan is None:
        return None
    bytes = savedPlan.SerializeToString()
    return b64encode(bytes).decode('utf-8')


def decode_saved_plan(bytes):
    return b64decode(bytes) if bytes is not None else None


def sage_http_error(text, status=400):
    content = """
        <!DOCTYPE html>
        <html lang="en" dir="ltr">
          <head>
            <meta charset="utf-8">
            <title>SaGe server Error</title>
          </head>
          <body>
            <h1>SaGe server error</h1>
            <p>{}</p>
          </body>
        </html>
    """.format(text)
    return Response(content, status=status, content_type="text/html")
