# walla-pocket
Wallabag to Pocket mirror.

Kobo has Pocket integration and is great for reading collected articles, unless you use any other save-for-later service.

This script simply mirrors the unread list from wallabag RSS feed into Pocket, archiving items from Pocket that are extraneous found (read or deleted).

To generate a Pocket access token, first generate an API key, then use something like https://reader.fxneumann.de/plugins/oneclickpocket/auth.php to generate a user token.

Invoke either the script or docker image with the following flags
```
--wallabag-host
--wallabag-user
--wallabag-secret
--pocket-key
--pocket-secret
```

If you want to delete all of Pocket's unread list, use the `--purge` flag.  These articles will be removed prior to syncing.
