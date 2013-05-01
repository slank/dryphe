Dryphe
======

A command-line client for Google Drive

Installation
-------------

    cd dryphe
    virtualenv --no-site-packages ve
    . ve/bin/activate
    pip install -r requirements.txt

Configuring API Access
----------------------

Dryphe makes use of authenticated access to the Google Drive API. The
application must be registered as an API project and be issued a client ID. The
client ID tracks access via the API and allows Google to impose quotas on its
use. The free quota for Google Drive is currently very high.

Here's how to issue your own client ID via the API console.

1. Visit https://code.google.com/apis/console
2. Create a new project. The name is unimportant, but "Dryphe" is recommended.
3. Enable the "Drive API" service.
4. In "API Access", create an OAuth 2.0 client ID. The product name is
   unimportant, but "Dryphe" is recommended.
5. In the Client ID Settings, choose "Installed Application". This is important,
   as it indicates that your credentials will be unprotected. See
   https://developers.google.com/accounts/docs/OAuth2InstalledApp

Once your Client ID is created, choose "Download JSON". Save (or symlink) the
file inside your copy of dryphe (in the same directory as auth.py).

Usage
-----

Type ```dryphe -h``` for built-in help. You can get help for a particular command with ```dryphe <command> -h```.

Commands are:

    auth   Obtain authorization to access Google Drive
    ls     List files
    mkdir  Create a folder (not implemented)
    get    Download files and directories (not implemented)
    put    Upload files and directories (not implemented)

The first thing to do is to authorize the application using ```dryphe auth```.
Dryphe will output a URL that you may visit in your web browser. The web
browser used does not have to reside on the same system as dryphe. Once you've
authenticated and authorized the application, Google will provide a token which
you must provide to dryphe to complete the process.

Your authorization information is stored (by default) in ~/.dryphe/authorization. You may specify an alternate file (perhaps for working with multiple accounts) with ```--auth-file```.
