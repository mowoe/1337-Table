import os

DATA_DIRECTORY = "Framework/data/^APP_NAME^/data/"

def get_data_directory(appname):
    dir = DATA_DIRECTORY.replace("^APP_NAME^", appname)
    if not os.path.exists(dir):
        os.system("mkdir -p \"%s\"" % dir)
    return dir

if __name__ == "__main__":
    print get_data_directory("test")