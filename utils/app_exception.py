class ApplicationException(Exception):
  def __init__(self, message='Interal Server Error'):
    self.message = message
    super().__init__(self.message)