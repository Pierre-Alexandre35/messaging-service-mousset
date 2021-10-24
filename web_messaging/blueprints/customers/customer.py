from web_messaging.extensions import mongo


def user_already_exits(collection, new_user):
    new_user_phone = new_user['Phone']
    is_already_present = collection.find_one({'Phone': new_user_phone})
    return is_already_present


def create_customer(first_name, last_name, phone, selected_list):
    new_user = {'First Name': first_name,
                'Last Name': last_name, 'Phone': phone}
    collection = mongo.db[selected_list]
    if user_already_exits(collection, new_user):
        return "alrady exits"
    else:
        collection.insert_one(new_user)


def delete_customer(selected_list, phone):
    collection = mongo.db[selected_list]
    to_delete = {'Phone': phone}
    collection.delete_one(to_delete)
