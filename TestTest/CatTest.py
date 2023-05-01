from Cat import TypeCat

cat_1 = TypeCat("Baron", "man", 2)
cat_2 = TypeCat("Sam", "man", 2)
Cat3 = TypeCat("Muhtar", "man", 0)

print(cat_1.get_name(), cat_1.get_sex(), cat_1.get_age())
print(cat_2.get_name(), cat_2.get_sex(), cat_2.get_age())

class Dog(TypeCat):
    def get_pet(self):
        return f'{self.get_name()} {self.get_age()}'

dog_1 = Dog("Felix", "boy", 2)

print(dog_1.get_pet())