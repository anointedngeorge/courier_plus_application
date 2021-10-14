from contextlib import contextmanager

class MessageWriter:
	def __init__(self, filename, permission):
		self.file_name = filename
		self.permission = permission

	@contextmanager
	def open_file(self):
		try:
			file = open(f'error/{self.file_name}', self.permission)
			yield file
		finally:
			file.close()


