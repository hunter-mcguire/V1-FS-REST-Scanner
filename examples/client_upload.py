import requests

# Specify the API endpoint where you want to upload the file
upload_url = 'http://localhost:8000/scan'

# Specify the file you want to upload
file_path = 'path/to/your/file.txt'

# Create a dictionary with the file key and the file object
files = {'file': ('file.txt', open(file_path, 'rb'))}

# Make the request with the files parameter
response = requests.post(upload_url, files=files)

# Check the response
if response.status_code == 200:
    print('File uploaded successfully!')
else:
    print(f'Error uploading file. Status code: {response.status_code}')
    print(response.text)
