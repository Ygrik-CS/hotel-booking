class Maybe:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def some(value):
        return Maybe(value)

    @staticmethod
    def nothing():
        return Maybe(None)

    def map(self, fn):
        return Maybe(fn(self.value)) if self.value is not None else self

    def bind(self, fn):
        return fn(self.value) if self.value is not None else self

    def get_or_else(self, default):
        return self.value if self.value is not None else default

    def is_some(self):
        return self.value is not None

    def is_none(self):
        return self.value is None



class Either:
    def __init__(self, left=None, right=None):
        self.left = left # type: ignore
        self.right = right # type: ignore

    @staticmethod
    def left(value):
        return Either(left=value)

    @staticmethod
    def right(value):
        return Either(right=value)

    def map(self, fn):
        return Either.right(fn(self.right)) if self.right is not None else self

    def bind(self, fn):
        return fn(self.right) if self.right is not None else self

    def get_or_else(self, default):
        return self.right if self.right is not None else default

    def is_left(self):
        return self.left is not None

    def is_right(self):
        return self.right is not None

    def left_value(self):
        return self.left

    def right_value(self):
        return self.right