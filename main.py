import glob
import subprocess
import os
import zipfile
import time
import logging

mount_path = '/mnt/data'
disk_path = '/dev/sda'
source_path = '/opt/mysql/data/'
target_path = f'{mount_path}/mysql/'

logging.basicConfig(filename='app.log', format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)


# 挂载磁盘
def mnt_disk():
    if not os.path.exists(mount_path):
        logging.info("mkdir /mnt/data")
        os.mkdir(mount_path)
    if os.path.ismount(mount_path):
        logging.info('Had mounted')
        return
    if os.stat(disk_path).st_dev != os.stat(mount_path).st_dev:
        logging.info("Wrong mount point")
        subprocess.call(['umount', '/mnt/data'])
        subprocess.call(['mount', '/dev/sda', '/mnt/data'])


# 查找待压缩binlog
def find_binlog():
    binlogs = []
    for filename in glob.glob(f'{source_path}binlog.*'):
        if filename.endswith('.index') or filename.endswith('.gz'):
            continue
        binlogs.append(filename.replace(source_path,''))
    binlogs = sorted(binlogs)
    last = binlogs[-1]
    logging.info(f"last is {last}")
    for target in os.listdir(target_path):
        target = target.replace('.gz','')
        if target not in binlogs:
            continue
        binlogs.remove(target)
    result = set(binlogs)
    result.add(last)
    logging.info(f"find binlog:{result}")
    return result


# 压缩binlog
def gzip_binlog(files):
    for file in files:
        source_file = f'{source_path}{file}'
        target_file = f'{target_path}{file}'
        with zipfile.ZipFile(f'{target_file}.gz', 'w', zipfile.ZIP_DEFLATED) as zipf:
            logging.info(f"Gzip file {source_file} to {target_file}.gz")
            zipf.write(source_file)
# 运行
def run():
    try:
        mnt_disk()
        files = find_binlog()
        gzip_binlog(files)
    except Exception as e:
        logging.error("run task exception", e)


if __name__ == '__main__':
    while True:
        run()
        time.sleep(60*60)