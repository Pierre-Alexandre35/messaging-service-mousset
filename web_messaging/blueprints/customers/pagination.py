from web_messaging.extensions import mongo
import math
from config.settings import ITEMS_PER_PAGE
from flask_pymongo import pymongo

def get_pagination(current_page_number, total_number_pages):
    """ 
    Generate a pagination dictionary given a page number
    :param current_page_number: current page to paginate
    :param total_number_pages: total number of pages in the current model 
    :return: dictionary of pagination 
    """
    previous_page = current_page_number - 1
    next_page = current_page_number + 1
    displayed_previous_page = None
    displayed_next_page = None
    if previous_page > 0:
        displayed_previous_page = previous_page
    if next_page < total_number_pages:
        displayed_next_page = next_page

    return {
        "first-page": 0,
        "previous-page": displayed_previous_page,
        "current-page": current_page_number,
        "next-page": displayed_next_page,
        "last-page": total_number_pages
    }    
    
def get_number_of_records(selected_customer_list):
    collection = mongo.db[selected_customer_list]
    total_items = collection.count()
    return total_items
    
def generate_pagination(requested_page_number, selected_customer_list):
    collection = mongo.db[selected_customer_list]
    total_items = collection.count()
    total_number_pages = math.floor(total_items / ITEMS_PER_PAGE)
    items_to_skip = requested_page_number * ITEMS_PER_PAGE
    cursor = collection.find().skip(items_to_skip).limit(ITEMS_PER_PAGE)
    all_customers_items = cursor.sort("Last Name", pymongo.ASCENDING)
    return all_customers_items, get_pagination(requested_page_number, total_number_pages)