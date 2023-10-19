class Inventory:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
            print(f"UPDATED Item {item_name}")
        else:
            self.inventory[item_name] = quantity
            print(f"ADDED Item {item_name}")

    def delete_item(self, item_name, quantity):
        if item_name not in self.inventory:
            print(f"Item {item_name} does not exist")
        else:
            current_quantity = self.inventory[item_name]
            if current_quantity < quantity:
                print(f"Item {item_name} could not be DELETED")
            else:
                self.inventory[item_name] -= quantity
                print(f"DELETED Item {item_name}")

inventory = Inventory()

operations = [
    "ADD Pen 10",
    "ADD Paper 20",
    "DELETE Pen 5",
    "DELETE Eraser 3",
]

for operation in operations:
    parts = operation.split()
    if len(parts) >= 4:
        command, item_name, quantity = parts[0], parts[1], int(parts[2])
        if command == "ADD":
            inventory.add_item(item_name, quantity)
        elif command == "DELETE":
            inventory.delete_item(item_name, quantity)
    else:
        print("Invalid operation format")


print("Updated Inventory:")
for item, quantity in inventory.inventory.items():
    print(f"{item}: {quantity}")
