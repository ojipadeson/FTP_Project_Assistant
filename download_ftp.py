import ftplib
import os
import time
from ftplib import FTP


def ftp_connect(host, username, password):
    ftp_server = FTP()
    ftp_server.encoding = "ISO-8859-1"
    timeout = 30
    port = 21
    ftp_server.connect(host, port, timeout)
    ftp_server.login(username, password)
    return ftp_server


def find_tsv_in_dir(ftp_server, local_dir_path, dir_path, previous_path, target_format, ignore_dirs):
    if dir_path in ignore_dirs:
        return False
    try:
        ftp_server.cwd(previous_path + '/' + dir_path)
    except ftplib.error_perm:
        return False

    files_list = ftp_server.nlst()
    for files in files_list:
        try:
            local_files = files.encode("iso-8859-1").decode('gbk')
        except UnicodeDecodeError:
            local_files = files.encode("iso-8859-1").decode('utf-8')

        if find_tsv_in_dir(ftp_server, local_dir_path,
                           files, previous_path + '/' + dir_path,
                           target_format, ignore_dirs):
            return True
        else:
            ftp_server.cwd(previous_path + '/' + dir_path)

        if files[-4:] not in target_format:
            pass
        else:
            f = open(local_dir_path + '/' + local_files, 'wb')
            filename = files
            ftp_server.retrbinary('RETR ' + filename, f.write)
            get_time_stamp(ftp_server, filename)
            print('{0:{1}<35}'.format('Get test file: ' + local_files, chr(12288)))
            ftp_server.set_debuglevel(0)
            f.close()
            return True
    return False


def get_time_stamp(ftp_server, file):
    L = list(ftp_server.sendcmd('MDTM ' + file))
    dir_t = L[4] + L[5] + L[6] + L[7] + '-' + L[8] + L[9] + '-' + L[10] + L[11] + ' ' + L[12] + L[13] + ':' + L[14] + L[
        15] + ':' + L[16] + L[17]
    print('{0:{1}^30}'.format(dir_t, chr(12288)), end='')
    timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    current_time = int(time.time())
    period = current_time - timeStamp
    day_count = period // (3600 * 24)
    hour_count = period % (3600 * 24) // 3600
    min_count = period % (3600 * 24) % 3600 // 60
    if day_count:
        time_text = '{} day{} ago'.format(day_count, 's' if day_count > 1 else '')
    elif hour_count:
        time_text = '{} hour{} ago'.format(hour_count, 's' if hour_count > 1 else '')
    elif min_count >= 1:
        time_text = '{} minute{} ago'.format(min_count, 's' if min_count > 1 else '')
    else:
        time_text = 'just now'
    print('{0:{1}<20}'.format(time_text, chr(12288)), end='')
    return


def download_file(ftp_server, remotepath, localpath, target_format, ignore_dirs):
    ftp_server.cwd(remotepath)
    dirs_list = ftp_server.nlst()
    hand_in_count = 0
    tsv_count = 0
    for stu_dirs in dirs_list:
        try:
            local_dirs = stu_dirs.encode("iso-8859-1").decode('gbk')
        except UnicodeDecodeError:
            local_dirs = stu_dirs.encode("iso-8859-1").decode('utf-8')
        if local_dirs.startswith(tuple([str(i) for i in list(range(10))])):
            print('downloading:   {0:{1}^20}'.format(local_dirs, chr(12288)), end='')
            path = localpath + '/' + local_dirs
            if not os.path.exists(path):
                os.mkdir(path)

            if not find_tsv_in_dir(ftp_server, path, stu_dirs, remotepath, target_format, ignore_dirs):
                print()
            else:
                tsv_count += 1
            hand_in_count += 1
    print('{} Students have handed in .tsv in total'.format(tsv_count))
    print('{} Students have made their own directory'.format(hand_in_count))
