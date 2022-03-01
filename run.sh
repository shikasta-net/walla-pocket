#! /bin/bash

set -e

docker run --rm shikasta/wallapocket --wallabag-host=app.wallabag.it --wallabag-user=USER --wallabag-secret=SECRET --pocket-key=KEY --pocket-secret=SECRETER "$@"
