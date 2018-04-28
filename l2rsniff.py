from scapy.all import sniff
from scapy.all import *
from itertools import cycle
from L2RParser import L2RPktParser
import binascii
import sys

CIPHER = b'\xa7\x84\x20\xd0\xc9\x78\xb3\x9a'

class L2RPacketSniffer:
	
	########
	#
	#   Simple constructor, extend as needed
	#
	#
	
	def __init__(self, server_ip="34.237.41.153"):
		self.server_ip = server_ip
		self.L2R_parser = L2RPktParser()	
		
		self.buf_state = False		
		self.BUFFER = []
		self.BUFF_C = 0
		self.BUFFER_CAP = 10
		self.current_stream_len = 0	
		self.stream_len = 100000

	########
	#
	#   Begin sniffing your emulator, listens to RX packets from game-server, WW03 is default server
	#
	#
	
	def sniff_emu(self, ip_addr):
		port_filt = "ip src " + ip_addr
		sniff(filter=port_filt, prn=self.main_pkt_handler)
		return
	
	#######
	#
	#    During sniffing, parse L2R packet header structures and forward to correct deparser.
	#    
	#    struct L2R_header {
	#        uint24 length,
	#        uint16 pkt_id,
	#	 uint data[]
	#    }
	#
	#    Packet data is read struct-wise little-endian - eg, 0xabcd is 0xdcba
	#    @length: not encrypted, excluded in xor step
	#    @pkt_id: decrypted in same step with data 
	#    @data: parsed based on pkt_id
	#
	#
	
	def main_pkt_handler(self, pkt):
		
		#pkt.show()
	
		if TCP in pkt:
	
			print("\n - Packet in - ")
			print("Source: ", pkt[IP].src)

			# Decode L2R Packet Header
			try:	
				payload = pkt[TCP].payload.load
				
				# parse length from packet (not XOR'd)
				p_len = int.from_bytes(payload[:3], byteorder='little')
	
				# Decrypt data (packet ID included) - XOR Cipher decryption..
				# Notice decryption happens twice, should probably be fixed.
				# Reason we decrypt here is mainly for the packet type so we can decide on branching
				decrypted = bytes([(a ^ b) for (a,b) in zip(payload[3:], cycle(CIPHER)) ])
			
				# parse packet ID
				p_type = int.from_bytes(decrypted[:2], byteorder='little')		


				self.log_packet_stats(payload, p_len, p_type, decrypted)			

				
				'''
					Veryyyy lazy TCP Stream logic.
					

					1 - if match on a defined packet, start tracking and storing data.
					2 - each packet that comes in adds to the 'buffer' of data (just a 2d list)
					3 - when total payload in buffer (current_stream_len) > length of stream (stream_len),
						stitch data together,
						decrypt data,
						send to parser,
						reset stream tracking variables

					Assumptions:
						- only things we can parse right now are multi segment TCP stream RX 
						- packets will always arrive in order, if not just throw your hands up
	
					TODO:
						- thread the shit out of this for performance reasons
						- let process fail more gracefully and recover better
						- allow custom callbacks?
						- got lazy and made this sequence of if blocks, def need to clean up for readability some time
						- put command line args in
				'''
				if self.L2R_parser.parser_available(p_type) and not self.buf_state: 
					self.buf_state = True
					self.BUFFER.append([p_len, p_type, payload, decrypted])	
					self.stream_len = p_len		
					self.current_stream_len = len(payload)	


				if self.buf_state == True:	
					self.BUFFER.append([p_len, p_type, payload, decrypted])
					self.current_stream_len += len(payload)

#				if len(self.BUFFER[2]) >= self.stream_len:
					
				if self.current_stream_len >= self.stream_len:
					
					print("Buffer full, attempting to parse...")
			
					self.buf_state = False
					
					res = b"".join([self.BUFFER[i][2] for i in range(0, len(self.BUFFER))])
					res = bytes([(a ^ b) for (a,b) in zip(res[3:], cycle(CIPHER)) ])[:self.BUFFER[0][0]]

					result = self.L2R_parser.parse(self.BUFFER[0][1], decrypted[2:], self.BUFFER, res)		
					
					self.BUFFER = []	# empty buffer	
					self.current_stream_len = 0
					self.stream_len = 100000
					
					# Callback here? Maybe add a fancy decorator to the main_pkt_handler that takes a user supplied function?
					
					# Hard code print the results of one packet we can parse right now
					print("Guild ID: ", result.guild_id)
					print("Member Count: ", result.member_count)
					for member in result.members:
						print("\nMember: ")
						for k in member.keys():
							print(k +" : ", member[k])

					sys.exit(0)	
		
			except Exception as e:
				
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print("Could not load packet payload.")
				print("Exception: ", e)
				print("Line: ", exc_tb.tb_lineno)
				print("Obj: ", exc_tb.tb_frame.f_code.co_name)

					

		return

	def log_packet_stats(self, payload, p_len, p_type, decrypted):
		
		print("PLen bytes: ", payload[:3])
		print("PID bytes: ", binascii.hexlify(decrypted[:2]))
		print("Packet len: ", p_len)
		print("Packet ID (hex, int): ", hex(p_type), p_type)
		print("Buffer length: ", len(self.BUFFER))
		print("Buffer state ", self.buf_state)				

		return
if __name__ == "__main__":
	
	app = L2RPacketSniffer()
	app.sniff_emu(app.server_ip)

