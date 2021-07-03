class DummyTlc5947Light:
    """ Dummy Light class that's used in the controller slots where no real lights are defined
        Always returns 0 """

    @property
    def brightness(self):
        return 0


