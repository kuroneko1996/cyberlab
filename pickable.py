class Pickable:
    def __init__(self, owner, id, stackable=False, amount=1, auto_pick=False):
        """
        :param owner: object with attached behavior
        :param id: string
        :param stackable: bool
        :param amount: int
        :param auto_pick: bool
        """
        self.owner = owner
        self.id = id
        self.stackable = stackable
        self.amount = int(amount)
        self.auto_pick = auto_pick

    def pick(self, wearer):
        if wearer.container is not None and wearer.container.add(self.owner):
            return True

        return False

    def drop(self, wearer):
        if wearer.container is not None:
            wearer.container.remove(self.owner)

    def use(self, wearer):
        if wearer.container is not None:
            self.destroy_after_use(wearer)
            return True

        return False

    def destroy_after_use(self, wearer):
        if wearer.container is not None:
            if self.amount == 1:
                wearer.container.remove(self.owner)
                # TODO destroy owner
            else:
                self.amount -= 1
            return True

        return False
