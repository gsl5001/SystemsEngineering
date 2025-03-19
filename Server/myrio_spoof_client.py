import requests
import time
import os

def upload_image(image_path):
    relative_path = os.path.join(os.path.dirname(__file__), image_path)
    with open(relative_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.put('http://localhost:8080/image', files=files)
        if response.status_code == 200:
            print('Image uploaded successfully')
        else:
            print('Failed to upload image')

def poll_matrix_endpoint():
    while True:
        response = requests.get('http://localhost:8080/matrix')
        if response.status_code == 200:
            return response.json()
        time.sleep(5)

def main():
    while True:
        image_path = input('Enter the path to the image: ')
        print('Uploading image...')
        upload_image(image_path)
        print('Polling for matrix...')
        matrix = poll_matrix_endpoint()
        print('Matrix found:')
        print(matrix)
        input('Press Enter to restart the process...')

if __name__ == "__main__":
    main()
