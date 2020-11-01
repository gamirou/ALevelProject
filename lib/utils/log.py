class Log:
    """
    Better print thing
        Log.i(self.TAG, "Something")
        Log.e(self.TAG, "Bruh something happened", ValueError())
        Log.w(self.TAG, "Warning")
        
    """

    COLOURS = {
        "red": '1;31;40m',
        "blue": '1;34;40m',
        "yellow": '1;33;40m'
    }

    def __init__(self):
        pass

    @classmethod
    def e(cls, tag, message, error=None):
        print("\x1b[{}E/{}: {}; Error: {}\x1b[0m".format(cls.COLOURS["red"], tag, message, error))

    @classmethod
    def i(cls, tag, message):
        print("\x1b[{}I/{}: {}\x1b[0m".format(cls.COLOURS["blue"], tag, message))

    @classmethod
    def w(cls, tag, message):
        print("\x1b[{}W/{}: {}\x1b[0m".format(cls.COLOURS["yellow"], tag, message))