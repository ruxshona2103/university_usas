import base64
import os

from django.core.files.uploadedfile import UploadedFile
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio_storage.storage import MediaImagekitStorage


class PatchedMediaImagekitStorage(MediaImagekitStorage):
    """
    ImageKit storage bug fix: the original library passes the full
    upload_to path as file_name to the API (e.g. 'ilmiy_faoliyat/files/doc.pdf'),
    while the same path is already set as the destination folder.
    ImageKit treats slashes in file_name as sub-folders, so every new
    upload adds one more level of nesting in the CDN path.

    Fix: use only os.path.basename(name) as file_name so the folder
    and the filename are passed separately and correctly.
    """

    def _save(self, name, content):
        self.UPLOAD_OPTIONS['folder'] = self._get_upload_path(name)
        options = UploadFileRequestOptions(**self.UPLOAD_OPTIONS)

        file_name = os.path.basename(self._normalise_name(name))

        content = UploadedFile(content, file_name)
        encoded = base64.b64encode(content.read())

        response = self._upload(file=encoded, file_name=file_name, options=options)
        return response.file_id
