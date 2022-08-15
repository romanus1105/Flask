import requests

baseUrl = 'http://127.0.0.1:5000'

try:
    resp = requests.post(f'{baseUrl}/adverts/', json={
        'id': 1,
        'header': 'header_1',
        'description': 'very long decription 11!!11',
        'create_date': '21/11/1994',
        'owner': 'user1',
    })
    print(resp.status_code)
    print(resp.json())
except Exception as ex:
    print(f'Trying connection to {baseUrl}, the next exception has occured:')
    print(ex)

try:
    resp = requests.delete(f'{baseUrl}/adverts/', json={
        'id': 7,
    })
    print(resp.status_code)
    print(resp.json())
except Exception as ex:
    print(f'Trying connection to {baseUrl}, the next exception has occured:')
    print(ex)