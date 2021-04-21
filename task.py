import logging
import multiprocessing
import os
import random
from multiprocessing import Pool

logging.basicConfig(filename='events.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class Customer:
    def __init__(self, id_key, money=0, monthly_income=0, own_bank=None):
        self.id_key = id_key
        self.money = money
        self._monthly_income = monthly_income
        self.own_bank = own_bank

    def __str__(self):
        return 'Customer {} his cash {}, his bank {}'.format(self.id_key, self.money, self.own_bank)

    @property
    def monthly_income(self):
        return self._monthly_income

    @monthly_income.setter
    def monthly_income(self, income):
        if income < 0:
            raise ValueError("Sorry you income is below 0")
        self._monthly_income = income


class Bank(multiprocessing.Process):

    def __init__(self, name):
        multiprocessing.Process.__init__(self)
        self.customer_accounts = []
        self.name = name
        self.amount_of_money = 100000

    def __str__(self):
        return 'Bank {} on process {}'.format(self.name, os.getpid())

    @classmethod
    def create_anonymus_bank(cls):
        anonymus_bank_name = "*****"
        return cls(anonymus_bank_name)

    @staticmethod
    def can_take_loan(monthly_income):
        minimum_income = 2000
        return monthly_income > minimum_income

    def add_new_customer(self, customer):
        new_customer = {'{}'.format(customer.id_key): customer.money}
        self.customer_accounts.append(new_customer)
        self.amount_of_money += customer.money
        customer.money -= customer.money
        success_message = "Customer {} create account in {}".format(customer.id_key, self.name)
        return success_message

    def find_customer(self, customer):
        for account in self.customer_accounts:
            customer_id = '{}'.format(customer.id_key)
            if customer_id in account:
                return account, customer_id

    def delete_account(self, customer):
        account, customer_id = self.find_customer(customer)
        self.customer_accounts.remove(account)

    def take_loan(self, customer, cash):
        can_take = Bank.can_take_loan(customer.monthly_income)
        if can_take:
            self.amount_of_money -= cash
            customer.money += cash
            success_message = "Customer {} from Bank {} take {} loan".format(customer.id_key, self.name, cash)
            return success_message
        else:
            failure_message = "Customer {} from Bank {} has too little income".format(customer.id_key, self.name)
            return failure_message

    def check_customer_balance(self, customer):
        account, customer_id = self.find_customer(customer)
        return account[customer_id]

    def transfer_cash_internal_bank(self, sender, recipient, cash):
        sending_account, sender_id = self.find_customer(sender)
        receving_account, recipient_id = self.find_customer(recipient)
        sending_account[sender_id] -= cash
        receving_account[recipient_id] += cash
        success_message = "Customer {} transfer {} to client {}".format(sender.id_key, cash, recipient.id_key)
        return success_message

    def transfer_cash_external_bank(self, sender, recipient_bank, recipient, cash):
        sending_account, sender_id = self.find_customer(sender)
        receving_account, recipient_id = recipient_bank.find_customer(recipient)
        sending_account[sender_id] -= cash
        receving_account[recipient_id] += cash
        success_message = "Customer {} form {} transfer {} to client {} form {}".format(sender.id_key, self.name, cash,
                                                                                        recipient.id_key,
                                                                                        recipient_bank.name)
        self.amount_of_money -= cash
        recipient_bank.amount_of_money += cash
        return success_message

    def withdraw_cash(self, customer, cash, flow):
        account, customer_id = self.find_customer(customer)
        if flow:
            account[customer_id] += cash
            self.amount_of_money += cash
            customer.money -= cash
            success_message = "Customer {} deposit {}".format(customer.id_key, cash)
            return success_message
        else:
            if cash <= account.get(customer_id):
                account[customer_id] -= cash
                self.amount_of_money -= cash
                customer.money += cash
                success_message = "Customer {} withdraw {}".format(customer.id_key, cash)
                return success_message


if __name__ == '__main__':
    pool = Pool(3)
    minimum_customer_cash = 100
    maximum_customer_cash = 10000
    minimum_transfer_cash = 10
    maximum_transfer_cash = 1000
    customer_amount = 16
    bank_amount = 3
    bank_names = ["mBank", "PKO", "BNP", "Krakowski Bank", "Python Bank"]
    customers = []
    banks = []
    for customer_id in range(customer_amount):
        customer_cash = random.randint(minimum_customer_cash, maximum_customer_cash)
        customer_id += 1
        customers.append(Customer(customer_id, customer_cash))
    for bank in range(bank_amount):
        max_bank_names_list_index = len(bank_names) - 1
        bank_name = bank_names[random.randint(0, max_bank_names_list_index)]
        bank_names.remove(bank_name)
        banks.append(Bank(bank_name))
    for customer in customers:
        max_banks_list_index = len(banks) - 1
        bank = banks[random.randint(0, max_banks_list_index)]
        logging.info(bank.add_new_customer(customer))
        customer.own_bank = bank
    random_customer_index = random.randint(0, customer_amount - 1)
    random_bank_index = random.randint(0, bank_amount - 1)
    random_customer = customers[random_customer_index]
    anonymous_bank = Bank.create_anonymus_bank()
    banks.append(anonymous_bank)
    random_customer_bank = random_customer.own_bank
    random_customer.monthly_income = 2001
    logging.info(random_customer_bank.check_customer_balance(random_customer))
    logging.info(random_customer_bank.take_loan(random_customer, cash=1000))
    random_customer.monthly_income = 1999
    logging.info(random_customer_bank.take_loan(random_customer, cash=1000))
    deposit = True
    cash = 250
    logging.info(random_customer_bank.withdraw_cash(random_customer, cash, deposit))
    logging.info(random_customer_bank.check_customer_balance(random_customer))
    for transaction in range(12):
        random_customer_index = random.randint(0, customer_amount - 1)
        random_sender = customers[random_customer_index]
        sender_bank = random_sender.own_bank
        random_customer_index = random.randint(0, customer_amount - 1)
        random_recipient = customers[random_customer_index]
        recipient_bank = random_recipient.own_bank
        cash = random.randint(minimum_transfer_cash, maximum_transfer_cash)
        if recipient_bank == sender_bank:
            logging.info(sender_bank.transfer_cash_internal_bank(random_sender, random_recipient, cash))
        else:
            logging.info(sender_bank.transfer_cash_external_bank(random_sender, recipient_bank, random_recipient, cash))
