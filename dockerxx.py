import logging
import docker
from docker.errors import APIError
import sys
import argparse

# # 设置日志配置
# logging.basicConfig(filename=logs_file, level=logging.INFO,
#                     format='%(asctime)s:%(levelname)s:%(message)s')

def log_info(message):
    print(message)
    logging.info(message)

# def pull_image(image_name):
#     try:
#         log_info(f"Pulling image {image_name}")
#         client.images.pull(image_name)
#         log_info(f"Image {image_name} pulled successfully.")
#     except APIError as e:
#         log_info(f"Failed to pull image {image_name}: {e}")
    # except KeyboardInterrupt:
    #     log_info("Operation interrupted by user.")
    #     sys.exit(1)

# def tag_image(image_name, repo):
#     try:
#         if repo.endswith('/'):
#             repo = repo[:-1]
#         repo = repo + '/' + image_name.split(':')[0]
#         if ':' in image_name:
#             tag = image_name.split(':')[-1].replace(' ', '')
#         else:
#             tag = "latest"

#         log_info(f"Tagging image {image_name} with {repo}: {tag}")
#         client.api.tag(image_name, repo, tag)
#         log_info(f"Image {image_name} tagged successfully.")
#     except APIError as e:
#         log_info(f"Failed to tag image {image_name}: {e}")
    # except KeyboardInterrupt:
    #     log_info("Operation interrupted by user.")
    #     sys.exit(1)

# def push_image(image_name):
#     try:
#         log_info(f"Pushing image {image_name}")
#         for line in client.images.push(image_name, stream=True, decode=True):
#             if 'status' in line:
#                 log_info(line['status'])
#     except APIError as e:
#         log_info(f"Failed to push image {image_name}: {e}")
#     # except KeyboardInterrupt:
#     #     log_info("Operation interrupted by user.")
#     #     sys.exit(1)

def remove_image(image_name):
    try:
        log_info(f"Removing image {image_name}")
        client.images.remove(image=image_name, force=True)
        log_info(f"Image {image_name} removed successfully.")
    except APIError as e:
        log_info(f"Failed to remove image {image_name}: {e}")
    # except KeyboardInterrupt:
    #     log_info("Operation interrupted by user.")
    #     sys.exit(1)

def read_images_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        log_info(f"File not found: {filename}")
        return []

def tag_change(image_name, repo):
    if repo.endswith('/'):
        repo = repo[:-1]
    repo = repo + '/' + image_name.split(':')[0]
    if ':' in image_name:
        tag = image_name.split(':')[-1].replace(' ', '')
    else:
        tag = "latest"

    return (repo, tag)
def process_images(images, repo, remove):
    try:
        for index, image_name in enumerate(images, start=1):
            log_info(f"[[{index}/{len(images)}]]: {image_name}")

            log_info(f"Pulling image {image_name}")
            client.images.pull(image_name)
            log_info(f"successfully")

            new_repo, tag = tag_change(image_name, repo)
            new_image = new_repo + ":" + tag

            log_info(f"Tagging image {image_name} with {new_image}")
            client.api.tag(image_name, new_repo, tag, force=True)
            log_info(f"successfully")

            log_info(f"Pushing image {new_image}")
            if True:
                client.images.push(new_image, stream=True, decode=True)
            else:
                for line in client.images.push(new_image, stream=True, decode=True):
                    if 'status' in line:
                        log_info(line['status'])
            log_info(f"successfully")
            
            if remove:
                log_info(f"Removing image {image_name}")
                client.images.remove(image=image_name, force=True)
                log_info(f"successfully")

                log_info(f"Removing image {new_image}")
                client.images.remove(image=new_image, force=True)
                log_info(f"successfully")

    except Exception as e:
        log_info(f"An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        log_info("Operation interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process Docker images from a list and push them to a repository.")
    parser.add_argument("-t", "--txt-file", dest="txt_file", type=str, required=True, help="Path to the text file containing image names.")
    parser.add_argument("-r", "--repo", type=str, required=True, help="Repository URL to which the images will be pushed.")
    parser.add_argument("-rm", "--remove", type=bool, default=True, help="Remove the local image after pushing (default: True).")
    parser.add_argument("-l", "--logs", type=str, default="dockerxx_operations.log", help="Remove the local image after pushing (default: True).")

    args = parser.parse_args()

    images = read_images_from_file(args.txt_file)
    repo = args.repo
    remove = args.remove
    logs_file = args.logs

    # 设置日志配置
    logging.basicConfig(filename=logs_file, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    client = docker.from_env()

    log_info("Starting image processing...")
    try:
        
        
        process_images(images, repo, remove)
        log_info("All operations completed.")
    except KeyboardInterrupt:
        log_info("Operation interrupted by user.")
        sys.exit(1)

# pyinstaller --onefile dockerxx.py
# .\dockerxx.exe -t "path\to\images.txt" -r "your-repo.com/new-name" --remove False
