"""Google Drive API access"""

from apiclient import errors

FOLDER_MIMETYPE = "application/vnd.google-apps.folder"

class InvalidPathError(Exception):
    pass

class FileNotFoundError(Exception):
    pass


class DriveAPI(object):
    def __init__(self, service):
        self.service = service


    def download(self, file_id):
        """Get contents of a file"""
        download_url = self.file_metadata(file_id).get('downloadUrl')
        if download_url:
            resp, content = self.service._http.request(download_url)
            if resp.status == 200:
                return content
        return None


    def upload(self, title, contents, parent_id='root', metadata=None):
        """Upload a file, possibly overwriting an existing file"""
        pass


    def metadata(self, file_id):
        """Get file metadata as a dictionary"""
        try:
            return self.service.files().get(fileId=file_id).execute()
        except errors.HttpError as e:
            if e.resp.status == '404':
                raise FileNotFoundError(file_id)
            return None


    def metadata_for_children(self, file_id):
        """List (id, title) for children of a folder"""
        child_list = []
        page_token = None
        while True:
            # results may be returned in multiple pages
            param = {}
            if page_token:
                param['pageToken'] = page_token
            q = "trashed = false and '{}' in parents".format(file_id)
            try:
                children = self.service.files().list(q=q, **param).execute()
            except errors.HttpError:
                return None

            child_list.extend(children.get('items', []))
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        return child_list


    def metadata_for_path(self, path):
        if not path.startswith("/"):
            raise InvalidPathError("Path is not absolute")
        segments = path[1:].split("/")

        file_id = "root"
        file_data = self.metadata('root')
        for segment in segments:
            children = self.metadata_for_children(file_id)
            if children is None:
                raise FileNotFoundError(path)
            else:
                for child in children:
                    if child['title'] == segment:
                        file_id = child['id']
                        file_data = child
                        break
        return file_data


    def folder_create(self, title, parent='root'):
        """Create a folder"""
        pass
