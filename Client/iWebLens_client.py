# Generate the parallel requests based on the  ThreadPool Executor
import glob
import sys
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests


# send http request
avg_time =0
def call_object_detection_service(image):
    try:
        global  avg_time

        url = str(sys.argv[2])

        files = {
            'image': open(image, 'rb')
        }

        print("Calling object detection service, URL: {} Image:{}".format(url, image))
        thread_start_time = time.time()
        response = requests.post(url, files=files)
        thread_elapsed_time = time.time() - thread_start_time
        avg_time = avg_time + thread_elapsed_time
        if response.ok:
            output = "Thread : {}, Time Spent: {}, Input Image: {} ,  Output:{}".format(
                threading.current_thread().getName(), thread_elapsed_time,
                image, response.text)
            print(output)

        else:
            print("Error, response status:{}".format(response))

    except Exception as e:
        print("Exception in webservice call: {}".format(e))


# gets the list of all image paths from the input folder
def get_images_to_be_processed(input_folder):
    images = []
    for image_file in glob.iglob(input_folder + "*.jpg"):
        images.append(image_file)
    return images


def main():
    ## provide the argumetns: inputfolder, url, number of wrokers
    if len(sys.argv) != 4:
        raise ValueError("Arguments list is wrong. Please use the following format: {} {} {}".
                         format("python iWebLens_cilent.py", "<input_folder>", "<URL> <number_of_workers>"))

    input_folder = os.path.join(sys.argv[1], "")
    images = get_images_to_be_processed(input_folder)
    num_images = images.__len__()
    num_workers = int(sys.argv[3])
    start_time = time.time()
    print(num_images)
    # create a worker  thread pool to invoke the requests in parallel
    with PoolExecutor(max_workers=num_workers) as executor:
        for _ in executor.map(call_object_detection_service, images):
            pass
    elapsed_time = time.time() - start_time

    print("Total client script time: {}, average thread time: {}".format(elapsed_time, avg_time/num_images))


if __name__ == "__main__":
    main()

