import urllib2
import os
import mimetypes
import zipfile
import tarfile
import re
import json
import shutil


class FPM(object):
    def __init__(self):
        self.dir_path = os.path.dirname(__file__)

    def install(self, url=None, target_name=None):
        try:
            request = urllib2.urlopen(url)
        except Exception, error:
            print error
            return

        filename = self._get_filename(request)
        download_path = self._download(request, filename)
        installed_path = self._extract_and_remove_src(
            download_path, target_name
        )
        print 'installed to : ' + installed_path

    def _get_filename(self, request):
        try:
            filename = request.info().get('content-disposition')
            m = re.match('.*(?P<file_name>filename.*=.*);?', filename)
            filename = m.group('file_name').split('=')[1]
            filename = filename.replace('"', '')
        except:
            filename = os.path.basename(
                urllib2.urlparse.urlparse(request.url).path
            )

        return filename

    def _download(self, request, filename):
        download_path = os.path.join(
            self.dir_path,
            filename,
        )
        print 'download_path: ' + download_path
        f = open(download_path, 'w')
        print('Downloading ' + request.url)
        f.write(request.read())
        f.close()
        print('Download Finished')
        print('Saved to `' + download_path + '`')
        return download_path

    def _extract_and_remove_src(self, path, target_name):
        if zipfile.is_zipfile(path):
            zip_file = zipfile.ZipFile(path)
            zip_file.extractall(self.dir_path)
            filename = zip_file.infolist()[0].filename
        elif tarfile.is_tarfile(path):
            print 'Tar file has not been implemented'
            return
        else:
            print('Unsupport file type')
            return path

        os.remove(path)
        print('Removed downloaded file')
        try:
            target_path = os.path.join(self.dir_path, target_name)
            shutil.move(
                os.path.join(self.dir_path, filename),
                target_path
            )
        except Exception, e:
            print e
        return target_path


def run():
    fpm = FPM()
    package = os.path.join(fpm.dir_path, 'fpkg.json')
    package = open(package)
    package = json.load(package)
    for key in package:
        fpm.install(package[key], key)

if __name__ == '__main__':
    run()
