import requests
import json

headers = {
    'device': '6Fk1rB',
    'user-agent': 'Mozilla/56.36'
}

action = input("Enter the action: ")
sum = input("Enter the sum: ")
card_id = input("Enter the card ID: ")
back = input("Enter the back URL: ")
desc = input("Enter the transaction description: ")

if (action == 'create'):
    sum1 = int(sum) * 100

    data = {
        "method": "p2p.create",
        "params": {
            "card_id": card_id,
            "amount": sum1,
            "description": desc
        }
    }

    response = requests.post('https://payme.uz/api/p2p.create', headers=headers, json=data)
    res = response.json()
    print(res)

    csv = {
        '_id': res['result']['cheque']['_id'],
        '_url': 'https://checkout.paycom.uz',
        '_pay_amount': str(sum) + ' UZS',
        '_pay_url': 'https://checkout.paycom.uz/' + str(res['result']['cheque']['_id'])
    }

    ec = {
        '_details': csv
    }

    ec2 = {
        '_result': ec
    }

    print(json.dumps(csv, indent=4))

elif (action == 'info'):
    transaction_id = input("Enter the transaction ID: ")

    data = {
        "method": "cheque.get",
        "params": {
            "id": transaction_id
        }
    }

    response = requests.post('https://payme.uz/api/cheque.get', headers=headers, json=data)
    res = response.json()

    if res['result']['cheque'] is not None and 'pay_time' in res['result']['cheque']:
        print("Transaction was successful.")
    else:
        print("Transaction was unsuccessful")

else:
    print("Invalid action.")