import argparse
import os
import shutil
import time
import logging

def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def file_should_be_copied(src, dst):
    """Check if the source file is larger than the destination, or if the destination doesn't exist."""
    if not os.path.exists(dst):
        logging.info(f"Destination file {dst} does not exist.")
        return True
    elif os.path.getsize(src) > os.path.getsize(dst):
        logging.info(f"Source file {src} is larger than destination file {dst}.")
        return True
    else:
        logging.info(f"No need to copy: Source file {src} is not larger than destination file {dst}.")
        return False

def copy_file(src, dst):
    """Copy the file from src to dst."""
    try:
        shutil.copy2(src, dst)
        logging.info(f"Copied {src} to {dst}")
    except Exception as e:
        logging.error(f"Failed to copy from {src} to {dst}. Error: {e}")

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Copy file based on size condition.")
    parser.add_argument("source", help="Source file path")
    parser.add_argument("destination", help="Destination file path")
    parser.add_argument("--loopmode", action="store_true", help="Enable loop mode for continuous check")
    parser.add_argument("--sleep", type=int, default=5, help="Sleep duration in seconds for loop mode")

    args = parser.parse_args()

    # Check if source file exists
    if not os.path.exists(args.source):
        logging.error(f"Source file {args.source} does not exist.")
        return

    if args.loopmode:
        logging.info("Starting in loop mode...")
        while True:
            if file_should_be_copied(args.source, args.destination):
                copy_file(args.source, args.destination)
            time.sleep(args.sleep)
    else:
        if file_should_be_copied(args.source, args.destination):
            copy_file(args.source, args.destination)

if __name__ == "__main__":
    main()

