import hashlib
import requests
from ..metric_functions import timer

@timer
def download_file(url, target):
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    sha256 = hashlib.sha256()  # Typical hashing algorithm
    with open(target, "wb") as f:
      for chunk in r.iter_content(chunk_size=10*1024*1024):  # set chunk size to 10MB/ can be scalled depending on available resources
        if chunk:
          sha256.update(chunk)
          f.write(chunk)
  return sha256.hexdigest()  # return the SHA-256 hash of the file
