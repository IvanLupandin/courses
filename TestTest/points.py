class Customers:
    def __init__(self, first_name,second_name,city, balance):
        self.first_name = first_name
        self.second_name = second_name
        self.balance = balance
        self.city = city

    def __str__(self):
        return f'''{self.first_name} {self.second_name}.{self.city}. Баланс: {self.balance} руб.'''

    def get_customrs(self):
        return f'{self.first_name} {self.second_name} г.{self.city}'

client_1 = Customers('Иван', 'Петров', 'Москва', 50)
client_2 = Customers('Михаил', 'Иванов', 'Санкт-Петербург', 50)
client_3 = Customers('Иван', 'Гоген', 'Екатеренбург', 50)

guet_list = [client_1, client_2, client_3]

for guest in guet_list:
    print(guest.get_customrs())