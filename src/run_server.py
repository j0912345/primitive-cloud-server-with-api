import sys
use_cloud=True

if __name__ == "__main__":
    argv = sys.argv
    print(len(argv))
    if len(argv) > 1:
        if argv[1] == "no_cloud":
            use_cloud=False