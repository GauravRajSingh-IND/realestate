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

    def add_suburbs_interested(self, phone_number:int, state:list, suburbs:list, pincode:list):

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


    def delete_customer_data(self, phone_number):
        """
        This function takes phone number of the customer and delete the customer data
        from both customer json and csv file. Once the data is delete from the database
        no further communication is done.
        :param phone_number: number of the customer
        :return:
        """

        # read data from customer data csv file.
        data = pd.read_csv("customers_data.csv")
        data.drop(data[data['Phone_number'] == phone_number].index, inplace=True)

        # save the data again to the same file.
        data.to_csv('customers_data.csv', mode='w', index=False, header=True)

        # read json data.
        with open("customer_suburbs.json", "r") as file:
            json_data = json.load(file)

        if str(phone_number) in json_data:
            json_data.pop(str(phone_number))

        # saving the updated JSON data back to the file
        with open("customer_suburbs.json", "w") as file:
            json.dump(json_data, file, indent=4)
