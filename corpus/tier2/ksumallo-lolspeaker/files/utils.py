class Log:
    PREFIX_DEBUG = "D"
    PREFIX_INFO = "I"
    PREFIX_YELL = "!"
    PREFIX_WARN = "W"
    PREFIX_ERROR = "E"

    COLOR_DEBUG = '\033[30m' # BLACK (GRAY)
    COLOR_YELL = '\033[32m' # GREEN
    COLOR_INFO = '\033[34m' # BLUE
    COLOR_WARN = '\033[33m' # YELLOW
    COLOR_ERROR = '\033[31m' # RED
    COLOR_CLEAR = '\033[0m' # CLEAR FORMATTING

    show_logs = True

    @staticmethod
    def show(enable: bool):
        Log.show_logs = enable

    @staticmethod
    def d(message: str, tag: str = "", end: str = "\n"):
        if Log.show_logs:
            tag = f':{tag}' if tag else ''
            print(Log.COLOR_DEBUG, end='')
            print(f"[{Log.PREFIX_DEBUG}{tag}]", message, end=end)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def i(message: str, tag: str = ""):
        if Log.show_logs:
            tag = f':{tag}' if tag else ''
            print(Log.COLOR_INFO, end='')
            print(f"[{Log.PREFIX_INFO}{tag}]", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def yell(message: str, tag: str = ""):
        if Log.show_logs:
            tag = f':{tag}' if tag else ''
            print(Log.COLOR_YELL, end='')
            print(f"[{Log.PREFIX_YELL}{tag}]", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def w(message: str, tag: str = ""):
        if Log.show_logs:
            tag = f':{tag}' if tag else ''
            print(Log.COLOR_WARN, end='')
            print(f"[{Log.PREFIX_WARN}]{tag}", message)
            print(Log.COLOR_CLEAR, end='')

    @staticmethod
    def e(message: str, tag: str = ""):
        if Log.show_logs:
            tag = f':{tag}' if tag else ''
            print(Log.COLOR_ERROR, end='')
            print(f"[{Log.PREFIX_ERROR}{tag}]", message)
            print(Log.COLOR_CLEAR, end='')