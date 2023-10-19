import requests

api_url = 'http://0.0.0.0:6969/convert_csv_to_json'

csv_file_path = '/home/vatsal.zinzuvadiya/Desktop/json_master_api/Big.csv'

files = {'csv_file': open(csv_file_path, 'rb')}

try:
    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
    else:
        print(f"API request failed with status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
