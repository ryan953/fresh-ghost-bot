from debug import *
import sys
import urllib2

class Downloader(object):

  def download(self, url):
    sys.stdout.write('Downloading: %s\n' % (url, ))

    request = urllib2.Request(url=url)
    request.add_header('User-Agent', 'ryan953/fresh-ghost-bot')
    remote = urllib2.urlopen(request)

    if PageDownloader.verbose:
      data = self.chunk_read(remote, report_hook=self.chunk_report)
    else:
      data = self.chunk_read(remote)

    return data

  def save(self, data, filename):
    local = open(filename, 'w')
    local.write(data)
    local.close()
    sys.stdout.write('Saved To: %s\n\n' % (filename, ))

  def chunk_report(self, bytes_so_far, chunk_size, total_size):
    percent = 0 if total_size == 0 else float(bytes_so_far) / total_size
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
      (bytes_so_far, total_size, percent*100))

    if bytes_so_far >= total_size:
      sys.stdout.write('\n')

  def chunk_read(self, response, chunk_size=4096, report_hook=None):
    try:
      total_size = response.info().getheader('Content-Length').strip()
      total_size = int(total_size)
    except AttributeError:
      total_size = 0;

    bytes_so_far = 0
    data = []

    while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
        break

      data += chunk
      if report_hook:
        report_hook(bytes_so_far, chunk_size, total_size)

    return "".join(data)
