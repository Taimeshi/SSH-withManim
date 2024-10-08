

class UpdatersSection:

    def __init__(self):
        self.updaters: set[Updater] = set()
        self._children: list[UpdatersSection] = []

    def update(self):
        for child in self._children:
            child.update()

        updaters_sorted = sorted(self._updaters, key=lambda ud: ud.priority, reverse=True)
        for u in updaters_sorted:
            u.func()
        if self._enables_track:
            self._track()

    def branch(self) -> UpdatersSection:
        child = UpdatersSection()
        self._children.append(child)
