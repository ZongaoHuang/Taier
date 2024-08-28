import requests
import pprint

file_path = 'E:/Study/Code/Project/taier/code/backend/jailbreak/task2_Test1_testSuite.json'
set_id = '1'  # Replace with an actual set_id

with open(file_path, 'rb') as file:
    files = {'file': file}
    data = {'set_id': 1}
    response = requests.post('http://127.0.0.1:8888/api/upload-json', files=files, data=data)

pprint.pprint(response.json())

