from abc import ABCMeta, abstractmethod, abstractproperty


class BaseResult:
    """
    Base checking result
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_success(self):
        return False

    @abstractproperty
    def output(self):
        return ""

    def __bool__(self):
        return self.is_success()


class Result(BaseResult):
    """
    Code checking result
    """

    target = ""
    status = -1
    output = ""
    _is_success = False

    def __init__(self, target=None, output="", status=None):
        self.target = target
        self.output = str(output) if output is not None else ""
        self.status = int(status)
        self._is_success = True if self.status == 0 else False

    def is_success(self):
        return self._is_success


class ResultSet(BaseResult):
    """
    Set of code checking results
    """

    _is_success = False

    def __init__(self):
        self._results = []

    @property
    def results(self):
        return self._results

    def add(self, result):
        if not result.is_success():
            self._is_success = False
        self._results.append(result)

    @property
    def output(self):
        output = ""
        for result in self.results:
            output += result.output
            if not output.endswith('\n'):
                output += '\n'
        return output

    def is_success(self):
        if len(self.results) == 0:
            return False
        return self._is_success
