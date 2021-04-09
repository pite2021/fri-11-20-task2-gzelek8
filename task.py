class Customer():
  def __init__(self, id, money = 0):
    self.id = id 
    self.money = money

    


class Bank():

  def __init__(self):
    self.customer_accounts = []
    self.ammount_of_money = 100000
    
  def add_new_customer(self, customer):
    new_customer = {'{}'.format(customer.id): customer.money}
    self.customer_accounts.append(new_customer)
    self.ammount_of_money += customer.money

  def check_customer_balance(self, customer):
    for account in self.customer_accounts:
      customr_id ='{}'.format(customer.id)
      if customr_id in account:
        return account[customr_id]

  def transfer_cash(self, sender, recipient, cash):
    for sending_account in self.customer_accounts:
      if '{}'.format(sender.id) in sending_account:
        for receving_account in self.customer_accounts:
          if '{}'.format(recipient.id) in receving_account:
            sending_account['{}'.format(sender.id)] -= cash
            receving_account['{}'.format(recipient.id)] += cash
            return True
          else:
            return False

  def withdraw_cash(self, customer, cash, flow):
    for account in self.customer_accounts:
      customr_id ='{}'.format(customer.id) 
      if customr_id in account:
        if cash <= account.get(customr_id):
          if flow:
            account[customr_id] += cash
            self.ammount_of_money += cash

          else:
            account[customr_id] -= cash
            self.ammount_of_money -= cash



if __name__ == '__main__':
  customer1 = Customer(1, 100)
  bank1 = Bank()
  bank1.add_new_customer(customer1)
  print(bank1.check_customer_balance(customer1))
  deposit = True
  cash = 10
  bank1.withdraw_cash(customer1, cash, deposit)
  print(bank1.check_customer_balance(customer1))