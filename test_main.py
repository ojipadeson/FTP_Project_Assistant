import argparse

from download_ftp import ftp_connect
from download_ftp import download_file
from test_function import accuracy_test

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", type=str, help="Remote path of FTP server")
    parser.add_argument("--local", type=str, default='', help="Local path of FTP server")
    parser.add_argument("--host", type=str, default=None, help="Host of FTP server")
    parser.add_argument("--username", type=str, default=None, help="Username for FTP server")
    parser.add_argument("--password", type=str, default=None, help="Password of FTP server")
    parser.add_argument("--target", type=str, default='.tsv,.csv', help="Target files' type")
    parser.add_argument("--ignore", type=str, default=None, help="Name of ignored folders")
    parser.add_argument("--standard", type=str, default=None, help="Standard file for project")
    parser.add_argument("--header", type=int, default=None, help="Test files' header format")
    parser.add_argument("--index", type=int, default=None, help="Test files' index column")
    args = parser.parse_args()

    args.remote = '/' + args.remote

    if not args.host:
        args.host = input('Enter FTP Host: ')
    if not args.username:
        args.username = input('Enter Username: ')
    if not args.password:
        args.password = input('Enter Password: ')
    if not args.ignore:
        args.ignore = input('Enter ignore files or directories: ')
    if not args.standard:
        args.ignore = input('Enter path of standard file: ')

    args.target = args.target.split(',')
    args.ignore = args.ignore.split(',')

    ftp = ftp_connect(args.host, args.username, args.password)
    download_file(ftp, args.remote, args.local, args.target, args.ignore)
    ftp.quit()

    accuracy_test(args.standard, index=args.index, header=args.header)
