import math

class Pagination():
    def __init__(self, total_items, items_per_page, page_range):
        self.total_items = total_items  # total number of article to display in total
        self.items_per_page = items_per_page  # maximum number of article per page
        self.page_range = page_range  # number of previous and next pages to display
        self.current_page = 0
        self.number_of_pages = math.ceil(
            self.total_items / self.items_per_page)

        # if the current_page is 7 and page_range is 3 then self.following will be [8, 9, 10] and self.previous [4, 5 ,6]
        self.following = list(
            range(self.current_page + 1, self.current_page + self.page_range + 1))

        # empty because by default the current page is 0 so no previous
        self.previous = list()

    def increase(self, quantity):
        if self.current_page + quantity > self.number_of_pages:
            raise ValueError(
                f'The maximum number of pages is {self.number_of_pages}')
        else:
            self.current_page += quantity
            self.following = list()
            self.previous = list()
            for i in range(1, self.page_range + 1):
                new_following_page_number = i + self.current_page
                new_previous_page_number = self.current_page - i
                self.previous.insert(i, new_previous_page_number)
                if new_following_page_number < self.number_of_pages:
                    self.following.insert(i, new_following_page_number)

    def decrease(self, quantity):
        if self.current_page - quantity < self.number_of_pages:
            raise ValueError(f'The mimimum number of pages is 0')
        else:
            self.current_page -= quantity
            self.following = list()
            self.previous = list()
            for i in range(1, self.page_range + 1):
                new_following_page_number = i + self.current_page
                new_previous_page_number = self.current_page - i
                self.following.insert(i, new_following_page_number)
                if new_previous_page_number > self.number_of_pages:
                    self.previous.insert(i, new_previous_page_number)
       
       
    def number_of_previous_items(self):
        """ Sum of all items in all previous pages not including the current page """
        if self.current_page == 0:
            return 0
        return self.items_per_page * self.current_page

    # method call to display elements on the HTML page
    def dict(self):
        return {
            "current_page": self.current_page,
            "next_pages": self.following,
            "previous_pages": self.previous,
            "number_of_pages": self.number_of_pages
        }
        
        
            



