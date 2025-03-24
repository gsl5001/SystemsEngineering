import requests
import time

def process_image(image_data):
    # Placeholder function to process the image and return a matrix
    # For now, it returns a dummy matrix
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def poll_image_endpoint():
    while True:
        response = requests.get('http://172.22.11.2:8081/image')
        if response.status_code == 200:
            return response.content
        time.sleep(5)

def upload_matrix(matrix):
    response = requests.put('http://172.22.11.2:8081/matrix', json=matrix)
    if response.status_code == 200:
        print('Matrix uploaded successfully')
    else:
        print('Failed to upload matrix')

def wait_for_image_removal():
    while True:
        response = requests.get('http://172.22.11.2:8081/image')
        if response.status_code == 404:
            return
        time.sleep(5)

def main():
    while True:
        print('Polling for image...')
        image_data = poll_image_endpoint()
        print('Image found, processing...')
        matrix = process_image(image_data)
        print('Uploading matrix...')
        upload_matrix(matrix)
        print('Waiting for image removal...')
        wait_for_image_removal()
        print('Image removed, resetting...')

if __name__ == "__main__":
    main()
