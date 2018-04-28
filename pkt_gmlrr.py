# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO



if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class PktGmlrr(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class Fstring(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u2le()
            self.str = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.len), 0, False)).decode("ascii")


    class Packet(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.result_code = self._io.read_u2le()
            self.guild_id = self._io.read_u8le()
            self.member_count = self._io.read_u2le()
            self.member = [None] * (20)
            for i in range(20):
                self.member[i] = self._root.GuildMember(self._io, self, self._root)



    class GuildMember(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.player_id = self._io.read_u8le()
            self.name = self._root.Fstring(self._io, self, self._root)
            self.clan_role = self._io.read_u1()
            self.race = self._io.read_u4le()
            self.p_class = self._io.read_u4le()
            self.lvl = self._io.read_u2le()
            self.offline = self._io.read_u8le()
            self.contribution = self._io.read_u4le()
            self.total_contrib = self._io.read_u4le()
            self.greet = self._io.read_u1()
            self.greet_recv = self._io.read_u1()
            self.checkin = self._io.read_u1()
            self.player_cp = self._io.read_u8le()
            self.grant_recv_count = self._io.read_u1()
            self.world_info_id = self._io.read_u4le()
            self.intro = self._root.Fstring(self._io, self, self._root)
            self._io.align_to_byte()
            self.voice_emp = self._io.read_u1()


    @property
    def packet(self):
        if hasattr(self, '_m_packet'):
            return self._m_packet if hasattr(self, '_m_packet') else None

        _pos = self._io.pos()
        self._io.seek(2)
        self._m_packet = self._root.Packet(self._io, self, self._root)
        self._io.seek(_pos)
        return self._m_packet if hasattr(self, '_m_packet') else None


