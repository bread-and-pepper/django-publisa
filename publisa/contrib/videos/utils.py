import time
from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
    
class ProgressUploadHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(ProgressUploadHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None
        self.request = request

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
        if self.progress_id:
           self.cache_key = self.progress_id
           self.request.session['upload_progress_%s' % self.cache_key] =  {
                'length': self.content_length,
                'uploaded' : 0
           }

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        data = self.request.session['upload_progress_%s' % self.cache_key]
        data['uploaded'] += self.chunk_size
        self.request.session['upload_progress_%s' % self.cache_key] = data
        self.request.session.save()

        return raw_data
    
    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        del self.request.session['upload_progress_%s' % self.cache_key]



