import json

f = open("contacts.json")

data = json.load(f)

"""
data = [
    {'Id': 0, 'Email': 'John@gmail.com', 'Phone': '', 'OrderId': "12345678", "Contacts": 5},
    {'Id': 1, 'Email': '', 'Phone': '682212345', 'OrderId': "12345678", "Contacts": 2},
    {'Id': 34567, 'Email': 'Wick@gmail.com', 'Phone': '682212345', 'OrderId': "", "Contacts": 4},
    {'Id': 78999, 'Email': 'Wick@gmail.com', 'Phone': '', 'OrderId': "", "Contacts": 3}
]
"""

email_dict = {}
phone_dict = {}
order_id_dict = {}
record_id_dict = {}

linked_orders = [] # [[{email: x, phone: y, ...}, record_id_1, record_id_2...], ...]

for order in data:
    record_id = str(order['Id'])
    email = order['Email']
    phone = order['Phone']
    contacts = order['Contacts']
    order_id = order['OrderId']

    found = None

    if email != '' and email in email_dict:
        linked_order = linked_orders[email_dict[email]]
        linked_order.append(record_id)
        linked_order[0]['contacts'] += contacts

        found = email_dict[email]

    elif phone != '' and phone in phone_dict:
        linked_order = linked_orders[phone_dict[phone]]
        linked_order.append(record_id)
        linked_order[0]['contacts'] += contacts

        found = phone_dict[phone]

    elif order_id != '' and order_id in order_id_dict:
        linked_order = linked_orders[order_id_dict[order_id]]
        linked_order.append(record_id)
        linked_order[0]['contacts'] += contacts

        found = order_id_dict[order_id]

    if found:
        linked_orders[found][0]['email'].add(email)
        linked_orders[found][0]['phone'].add(phone)
        linked_orders[found][0]['order_id'].add(order_id)

        email_dict[email] = found
        phone_dict[phone] = found
        order_id_dict[order_id] = found
        record_id_dict[record_id] = found

    else:
        linked_orders.append([{
            'email': {email},
            'phone': {phone},
            'contacts': contacts,
            'order_id': {order_id}
        }, record_id])
        
        email_dict[email] = len(linked_orders) - 1
        phone_dict[phone] = len(linked_orders) - 1
        order_id_dict[order_id] = len(linked_orders) - 1
        record_id_dict[record_id] = len(linked_orders) - 1

    if int(record_id) % 1000 == 0:
        print("Progress:", record_id)

with open('submission_final.csv', 'w') as f:
    f.write("ticket_id,ticket_trace/contact\n")
    for record_id in range(len(data)):

        linked_order = linked_orders[record_id_dict[str(record_id)]]

        ticket_trace = linked_order[1:]
        contacts = linked_order[0]['contacts']
    
        f.write(f"{record_id},\"{'-'.join(ticket_trace)}, {contacts}\"\n")