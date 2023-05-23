import os


def list_files(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            print(os.path.join(root, name))


if __name__ == '__main__':
    list_files('/home/ted/t')
