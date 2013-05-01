"""Google Web APIs Authentication"""

import os
import sys
import gflags
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OOB_CALLBACK_URN
from oauth2client.tools import run
import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

def set_flags(browser=False):
    argv = set()

    # run the local web browser?
    if not browser:
        argv.add('--noauth_local_webserver')

    gflags.FLAGS(['prog'] + list(argv))

def get_credentials(token_file, initialize=False, **flags):
    set_flags(**flags)

    storage = Storage(token_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        if initialize:
            flow = flow_from_clientsecrets(CLIENT_SECRETS,
                                   scope="https://www.googleapis.com/auth/drive",
                                   redirect_uri=OOB_CALLBACK_URN)
            credentials = run(flow, storage)

    return credentials

def get_service(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    try:
        return build('drive', 'v2', http=http)
    except HttpError as e:
        if e.resp.status == 502:
            print >>sys.stderr, "Temporarily unavailable. Try again in 30 seconds."
        else:
            print >>sys.stderr, "Error: %s" % e.resp.status
            print >>sys.stderr, e.content
        sys.exit(2)
