class Container:
    def __init__(self, owner, max_size=0, on_update=None):
        """
        :param owner: object holding this container
        :param max_size: 0 for infinity
        """
        self.owner = owner
        self.max_size = max_size
        self.inventory = [None] * self.max_size  # init with None's
        self.on_update = on_update

    def add(self, item):
        if self.max_size > 0 and len(self.inventory) >= self.max_size:
            if self.try_to_stack(item):
                return True
            elif self.try_to_put_on_first_empty(item):
                return True
            else:
                return False

        if self.try_to_stack(item):
            return True
        else:
            self.inventory.append(item)
            self.call_on_update()
            return True

    def remove(self, item):
        try:
            # dequip
            index = self.inventory.index(item)
            self.inventory[index] = None
            self.call_on_update()
        except ValueError:
            pass

    def try_to_stack(self, item):
        if item.stackable:
            same_index = self.find_same_index(item)
            if same_index != -1:
                self.inventory[same_index].amount += item.amount
                self.call_on_update()
                return True

        return False

    def try_to_put_on_first_empty(self, item):
        empty_index = self.find_empty_index()
        if empty_index != -1:
            self.inventory[empty_index] = item
            self.call_on_update()
            return True

        return False

    def find_same_index(self, item):
        for i, v in enumerate(self.inventory):
            if v is not None and v.id is not None and v.id == item.id:
                return i

        return -1

    def find_empty_index(self):
        for i, v in enumerate(self.inventory):
            if v is None:
                return i

        return -1

    def call_on_update(self):
        if self.on_update is not None:
            self.on_update()
