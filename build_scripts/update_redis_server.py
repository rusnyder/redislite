#!/usr/bin/env python3
""" Update the redis.submodule in the redislite repo to the latest stable version """
import os
import re
import shutil
import urllib.request
import tarfile
import tempfile


def latest_stable_url():
    with urllib.request.urlopen("http://download.redis.io/releases/") as f:
        index = f.read().decode("utf-8")
    versions = re.findall(r"href=.*?redis[._-]v?(\d+(?:\.\d+)+)\.t", index)
    versions.sort(key=lambda s: list(map(int, s.split('.'))))
    return "http://download.redis.io/releases/redis-{}.tar.gz".format(versions[-1])


if __name__ == "__main__":
    url = latest_stable_url()
    shutil.rmtree('redis.submodule')
    with tempfile.TemporaryDirectory() as tempdir:
        print(f'Downloading {url} to temp directory {tempdir}')
        ftpstream = urllib.request.urlopen(url)
        tf = tarfile.open(fileobj=ftpstream, mode="r|gz")
        directory = tf.next().name

        print(f'Extracting archive {directory}')
        tf.extractall(tempdir)

        print(f'Moving {os.path.join(tempdir, directory)} -> redis.submodule')
        shutil.move(os.path.join(tempdir, directory), 'redis.submodule')

        # print('Updating jemalloc')
        # os.system('(cd redis.submodule;./deps/update-jemalloc.sh 4.0.4)')

        print('Adding new redis.submodule files to git')
        os.system('git add redis.submodule')
