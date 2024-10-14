import pandas as pd
import json

class Customer:

    def __init__(self):
        
        self.customers = pd.read_csv("customers_data.csv")
        self.customer_data_len = len(self.customers)

    def add_customer(self, customer_name:str, phone_number:int, state:str, pincode:int, suburb:str, email:str):

        # Check if the number provided is already exist or not.
        is_already_register = self.check_customer(phone_number)

        # if customer is already exist.
        if is_already_register:
            print("Customer already exist..")
            return None

        # open customer_data csv file and add the new data.
        data = pd.DataFrame({
            'Customer_name':customer_name.title(),
            'Phone_number':phone_number,
            'State':state,
            'Pincode':pincode,
            'Suburbs':suburb,
            'email':email,
        }, index=[0])

        data.to_csv('customers_data.csv', mode='a', index=False, header=False)

        # new customer added, update the list.
        self.customer_data_len += 1
        return None

    def check_customer(self, phone_number):

        # Loop over each phone number and check if the number already exist.
        return phone_number in self.customers['Phone_number'].values

    def add_suburbs_interested(self,phone_number:int, state:list, suburbs:list, pincode:list):

        # Open json file.
        with open("customer_suburbs.json", 'r') as file:
            customer_data = json.load(file)

        # create a dictionary of new customer.
        data =  {
                 "suburbs":suburbs,
                 "pincode":pincode,
                 "state":state
                }

        # add new data to customer data json file.
        customer_data[phone_number] = data

        # Write back to json file.
        with open("customer_suburbs.json", "w") as file:
            json.dump(customer_data, file, indent=4)

test = Customer()
test.add_suburbs_interested(phone_number=449932325, state=['vic', 'qld'], suburbs=['Bundoora', 'Wollert'], pincode=[3083, 3006])
