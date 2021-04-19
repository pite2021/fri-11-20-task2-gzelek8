class Customer:
    def __init__(self, id_key, money=0, monthly_income=0):
        self.id_key = id_key
        self.money = money
        self._monthly_income = monthly_income
    
    @property
    def monthly_income(self):
         return self._monthly_income
       
     # a setter function
    @monthly_income.setter
    def monthly_income(self, income):
        if(income < 0):
          raise ValueError("Sorry you income is below 0")
        self._monthly_income = income


class Bank:

    def __init__(self, name):
        self.customer_accounts = []
        self.name = name
        self.ammount_of_money = 100000
    

    def __str__(self):
        return 'Bank {}'.format(self.name)

    @classmethod
    def create_anonymus_bank(cls):
      anonymus_bank_name = "*****"
      return cls(anonymus_bank_name)

    @staticmethod
    def can_take_loan(monthly_income):
      minimum_income = 2000
      return monthly_income > minimum_income

    def find_customer(self, customer):
      for account in self.customer_accounts:
            customr_id = '{}'.format(customer.id_key)
            if customr_id in account:
                return account, customr_id

    def take_loan(self, customer, cash):
        account, customer_id = self.find_customer(customer)
        

    def add_new_customer(self, customer):
        new_customer = {'{}'.format(customer.id_key): customer.money}
        self.customer_accounts.append(new_customer)
        self.ammount_of_money += customer.money

    def check_customer_balance(self, customer):
      account, customer_id = self.find_customer(customer)
      return account[customer_id]

    def transfer_cash_internal_bank(self, sender, recipient, cash):
        sending_account, sender_id = self.find_customer(sender)
        receving_account, recipient_id = self.find_customer(recipient)
        sending_account[sender_id] -= cash
        receving_account[recipient_id] += cash

    def withdraw_cash(self, customer, cash, flow):
        account, customer_id = self.find_customer(customer)
        if cash <= account.get(customer_id):
          if flow:
            account[customer_id] += cash
            self.ammount_of_money += cash
          else:
            account[customer_id] -= cash
            self.ammount_of_money -= cash


if __name__ == '__main__':
    customer_one_cash = 100
    customer_one_id = 1
    customer1 = Customer(customer_one_id, customer_one_cash)
    customer_two_cash = 0
    customer_two_id = 2
    customer2 = Customer(customer_two_id, customer_two_cash)
    bank1 = Bank("mBank")
    print(bank1)
    bank1.add_new_customer(customer1)
    bank1.add_new_customer(customer2)
    print(bank1.check_customer_balance(customer1))
    print(bank1.check_customer_balance(customer2))
    deposit = True
    cash = 10
    bank1.withdraw_cash(customer1, cash, deposit)
    print(bank1.check_customer_balance(customer1))
    print(bank1.check_customer_balance(customer2))
    cash = 25
    bank1.transfer_cash_internal_bank(customer1, customer2, cash)
    print(bank1.check_customer_balance(customer1))
    print(bank1.check_customer_balance(customer2))