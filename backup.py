import sys
import os
import shutil
import time
import argparse

def back_up_folder(source_dir, replica_dir,interval, log_file):
    # checkig if source folder exists
    if not os.path.exists(source_dir):
        print(f"Invalid path: source folder '{source_dir}' does not exist.")
        return

    # Create replica folder if it doesn't exist
    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)
    try:
        while True:
            # iteratively Synchronize files from source to replica directory
            for root, dirs, files in os.walk(source_dir):
                replica_root = os.path.join(replica_dir, os.path.relpath(root, source_dir))
                for dir in dirs:
                    replica_subdir = os.path.join(replica_root, dir)
                    if not os.path.exists(replica_subdir):
                        os.makedirs(replica_subdir)
                for file in files:
                    source_file = os.path.join(root, file)
                    replica_file = os.path.join(replica_root, file) #expected replica file
                    #check file name and last modified time stamp
                    if not os.path.exists(replica_file) or os.stat(source_file).st_mtime > os.stat(replica_file).st_mtime:
                        shutil.copy2(source_file, replica_file)
                        log(f"Copied {source_file} to {replica_file}",log_file)

            # Remove files from replica directory that do not exist in source directory
            for root, dirs, files in os.walk(replica_dir):
                source_root = os.path.join(source_dir, os.path.relpath(root, replica_dir))
                for dir in dirs:
                    source_subdir = os.path.join(source_root, dir)
                    if not os.path.exists(source_subdir):
                        shutil.rmtree(os.path.join(root, dir))
                        log(f"Removed directory {os.path.join(root, dir)}",log_file)
                for file in files:
                    replica_file = os.path.join(root, file)
                    source_file = os.path.join(source_root, file)
                    if not os.path.exists(source_file):
                        os.remove(replica_file)
                        log(f"Removed file {replica_file}",log_file)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n User terminated -> exited.")
        return



def log(message, log_file):
    print(message)
    with open(log_file, "a+") as f:
        f.write(f"{message}\n")

if __name__ == "__main__":

    # setting args usign argparse
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_dir", type=str, help="Source directory")
    parser.add_argument("replica_dir", type=str, help="Replica directory")
    parser.add_argument("log_file", type=str, help="Log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    args = parser.parse_args()

    print("Backup starting.....\nPress ctrl+c to exit.")

    back_up_folder(args.source_dir, args.replica_dir,  args.interval,args.log_file)
