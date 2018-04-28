meta:
  id: pkt_gmlrr
  file-extension: dump

instances:
  packet:
    type: packet
    pos: 2

types:
  fstring:
    seq:
      - id: len
        type: u2le
      - id: str
        type: strz
        size: len
        encoding: ascii
        
  packet:
    seq:
      - id: result_code
        type: u2le
      - id: guild_id
        type: u8le
      - id: member_count
        type: u2le
      - id: member
        type: guild_member
        repeat: expr
        repeat-expr: 20 # member_count

  guild_member:
    seq:
      - id: player_id
        type: u8le
      - id: name
        type: fstring
      - id: clan_role
        type: u1
      - id: race
        type: u4le
      - id: p_class
        type: u4le
      - id: lvl
        type: u2le
      - id: offline
        type: u8le
      - id: contribution
        type: u4le
      - id: total_contrib
        type: u4le
      - id: greet
        type: u1
      - id: greet_recv
        type: u1
      - id: checkin
        type: u1
      - id: player_cp
        type: u8le
      - id: grant_recv_count
        type: u1
      - id: world_info_id
        type: u4le
      - id: intro
        type: fstring
      - id: voice_emp
        type: u1

        


