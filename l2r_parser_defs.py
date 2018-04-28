from scapy.all import sniff
from scapy.all import *
from itertools import cycle
from pkt_gmlrr import PktGmlrr
import binascii


#########
'''

	Parser functions going in this file to keep file bloat potential low.
	
	There are thousands of L2R packet defs so might as well keep them separate.

'''
########


###########
#
#   Packet ID: 1404
#
#  "PktGuildMemberListReadResult"
#

def guild_member_list_read_result(payload):

	class Data:

		def __init__(self):

			self.packet_id = 1404
			self.packet_type = "GuildMemberListReadResult"			
			self.members = []
			
			return

			
	try:

		with open('dump', 'wb')  as f:
			 f.write(payload)		

	except Exception as e:

		print("Unable to dump payload - ", e)
		print("Ending process..")
		sys.exit(0)
	
	data = Data()

	pkt = PktGmlrr.from_file("data/tmp")
	
	data.guild_id 	= pkt.packet.guild_id
	data.member_count 	= pkt.packet.member_count

	for i in range(0, len(pkt.packet.member)):
		
		mem = {}

		current_member = pkt.packet.member[i]
		
		mem['player_id'] 	= current_member.player_id
		mem['player_name'] 	= current_member.name.str
		mem['clan_role'] 	= current_member.clan_role
		mem['player_race'] 	= current_member.race
		mem['player_class'] 	= current_member.p_class
		mem['player_level'] 	= current_member.lvl
		mem['offline'] 	= current_member.offline
		mem['contribution']	= current_member.contribution
		mem['total_contrib']	= current_member.total_contrib
		mem['greet']		= current_member.greet
		mem['greet_recv']	= current_member.greet_recv
		mem['checkin']		= current_member.checkin
		mem['player_cp'] 	= current_member.player_cp
		mem['grant_recv_c'] 	= current_member.grant_recv_count
		mem['world_info_id']	= current_member.world_info_id
		mem['player_intro']	= current_member.intro.str
		mem['voice_emp']	= current_member.voice_emp	
		
		data.members.append(mem)

	return data
