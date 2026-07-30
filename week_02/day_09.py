def atm():

  balance = 1000
  def validateUser(pin : int) -> bool:
    """Check whether pin is correct."""
    correct_pin = 2005

    if pin == correct_pin:
      return True
    else:
      return False

  def showBalance(balance : int) -> None:
    """Display current balance of the user."""
    print(f"Current Balance: {balance}")

  def withdraw(amount : int,balance : int) -> None:
    """Perform the withdraw operation"""
    if amount < 0:
      print("Amount cannot be negative.")
      return

    if amount > balance:
      print("Not enough funds.")
      return
    print("Please collect your cash.")
    balance -= amount
    showBalance(balance)

  pin = int(input("Enter your PIN: "))
  status = validateUser(pin)
  if status is False:
    print("PIN incorrect. Please try again.")
    return
  print("Authentication completed.")
  showBalance(balance)

  amount = int(input("Please enter amount greater than 0: "))

  withdraw(amount,balance)

atm()