import pandas as pd


class Customer:

    def __init__(self):
        self.customers = pd.read_csv("customers_data.csv")
        self.customer_data_len = len(self.customers)

    def add_customer(self, customer_name:str, phone_number:str, state:str, pincode:int, suburb:list, email:str):

        # open customer_data csv file and add the new data.
        data = pd.DataFrame({
            'Customer_name':customer_name.title(),
            'Phone_number':phone_number,
            'State':state,
            'Pincode':pincode,
            'Suburbs':suburb,
            'email':email
        })

        data.to_csv('customers_data.csv', mode='a', index=False, header=False)

        # new customer added, update the list.
        self.customer_data_len += 1
