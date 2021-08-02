class TupleTypeError(Exception):
    def __init__(self, variable):
        super().__init__(f"Expected a string of a tuple yet found {type(variable)}\ntuple_convert will not raise this"
                         f" error for non-string lists or tuples by default but this can be enabled by setting "
                         f"must_be_string to True")