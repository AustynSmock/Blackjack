import csv

def write_money(money):
    with open("money.txt", "w") as file:
        file.write(money)

def read_money():
    with open("money.txt", "r") as file:
        final_money = file.readline()
    return float(final_money)
