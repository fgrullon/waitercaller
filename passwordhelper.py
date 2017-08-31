import hashlib
import os
import base64

class PasswordHelper:

	#This method use a hash function to create a final hash that we will store.
	def get_hash(self, plain):
		result = hashlib.sha512(plain.encode('utf-8'))
		return result.hexdigest()

	#This method usin generate a random string and we encode it as base64
	def get_salt(self):
		return base64.b64encode(os.urandom(20))
 
	def validate_password(self, plain, salt, expected):
		return self.get_hash(plain + salt) == expected