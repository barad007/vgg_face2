class Logger:
    """The Logger object logs the activity of an extractor/matcher and writes debug info to file.

    Args:
        _logs: List of messages.
        log_file_path: Path to the log file.
    """

    def __init__(self):
        self._logs = []
        self.log_file_path = False

    def error(self, msg: str):
        """Saves error message and all logs into the file.

        Args:
            msg (str): Additional information to add to the logs.
        """
        log_msg = f"{msg}\n"
        self._logs.append(log_msg)
        self.save()
        self._logs = []

    def save(self):
        """ Saves logs into the file."""
        try:
            with open(self.log_file_path, 'a') as f:
                f.writelines(self._logs)
        except OSError as err:
            print(f"OS error: {err}")
