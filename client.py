from impacket.dcerpc import transport
from impacket import uuid
import random

def main():
	uoclient = UOClient()
	uoclient.setupConnection()

class UOClient:
	params = {
		# DCERPC options
		'idempotent': 0,      # 
		'dcerpc_frag': -1,    # -1 - don't fragment
		'alter_ctx': 0,       # use alter_ctx instead of bind(). Will issue a bogus bind first
		'bogus_binds': 0,     # number of bogus UUIDs in bind() request
		'bogus_alter': 0,     # number of bogus UUIDs in alter_ctx(), implies alter_ctx
		'endianness': '<',    # < for little endian, > for big endian
		                      # When switching to big endian you also need to change the
				      # endianness of the parameters to the function (in dce.call())
				      # Structure does not currently have decent support for this,
				      # specially for the 'w' fields.
	}
	UUID = ('01010101-2323-4545-6767-898989898989','1.0')


	#payload = [0x74, 0x65, 0x73, 0x74, 0x00, 0x72, 0x65, 0x72, 0x73, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xa8, 0x0b, 0x02, 0x54, 0x68, 0x6f, 0x72, 0x61, 0x6e, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66, 0x56, 0x0e, 0x00, 0x00, 0xe1, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

	#payload_buffer = buffer(payload, 0, 116)

	login_payload = "7465737400726572730000000000000000000000c0a80b0254686f72616e3200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000066560e0000e109000000000000"
	
	login_payload = login_payload.decode('hex')

	msg_payload = "7465737400726572730000000000000000000000c0a80b0200000000010000000000020008000000000000000800000054686f72616e32000d000000040002000d00000061736461736461736461736400"
	
	msg_payload = msg_payload.decode('hex')

	"""
	payload = "test"
	for i in range(20 - len(payload)):
		payload += '\x00'
	payload += "Zokol"
	for i in range(20 - len(payload)):
		payload += '\x00'
	"""

	def setupConnection(self):
		stringbinding  = 'ncacn_ip_tcp:93.186.196.107[2000]'
		stringbinding %= self.params

		print "Using stringbinding: %r" % stringbinding

		self.trans = transport.DCERPCTransportFactory(stringbinding)
		self.trans.set_max_fragment_size(-1)
		self.trans.set_dport(2000)
		"""
		try:
		    # SMB parameters handling
		    self.trans.connect()
		    self.trans.send(payload)
		    print self.trans.recv()

		except Exception, e:
		    pass
		"""
		self.trans.connect()

		self.dce = self.trans.DCERPC_class(self.trans)
		self.dce.endianness = self.params['endianness']

		# DCERPC parameters handling
		self.dce.set_max_fragment_size(int(self.params['dcerpc_frag']))
		self.dce.set_idempotent(int(self.params['idempotent']))

		self.dce.bind(uuid.uuidtup_to_bin(self.UUID), bogus_binds = int(self.params['bogus_binds']))

		self.dce.set_max_tfrag(-1)

		self.dce.call(42, self.login_payload)

		#self.dce.send(self.msg_payload)
		#print self.trans.recv()

if __name__ == '__main__':
	main()