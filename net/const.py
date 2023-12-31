NET_VERSION = 2
NET_MAX_PACKETSIZE = 1400
NET_MAX_PAYLOAD = NET_MAX_PACKETSIZE - 6
NET_MAX_CHUNKHEADERSIZE = 5
NET_PACKETHEADERSIZE = 3
NET_MAX_CLIENTS = 64
NET_MAX_CONSOLE_CLIENTS = 4
NET_MAX_SEQUENCE = 1 << 10
NET_SEQUENCE_MASK = NET_MAX_SEQUENCE - 1
NET_CONNSTATE_OFFLINE = 0
NET_CONNSTATE_CONNECT = 1
NET_CONNSTATE_PENDING = 2
NET_CONNSTATE_ONLINE = 3
NET_CONNSTATE_ERROR = 4
NET_PACKETFLAG_CONTROL = 1
NET_PACKETFLAG_CONNLESS = 2
NET_PACKETFLAG_RESEND = 4
NET_PACKETFLAG_COMPRESSION = 8
# NOT SENT VIA THE NETWORK DIRECTLY:
NET_PACKETFLAG_EXTENDED = 16
NET_CHUNKFLAG_VITAL = 1
NET_CHUNKFLAG_RESEND = 2
NET_CTRLMSG_KEEPALIVE = 0
NET_CTRLMSG_CONNECT = 1
NET_CTRLMSG_CONNECTACCEPT = 2
NET_CTRLMSG_ACCEPT = 3
NET_CTRLMSG_CLOSE = 4
NET_CONN_BUFFERSIZE = 1024 * 32
NET_CONNLIMIT_IPS = 16

SECURITY_TOKEN_MAGIC = "TKEN"

NET_SECURITY_TOKEN_UNKNOWN = -1
NET_SECURITY_TOKEN_UNSUPPORTED = 0

# Packer

PACKER_BUFFER_SIZE = 1024 * 2

# System messages
NETMSG_INVALID = 0
NETMSG_INFO = 1
NETMSG_MAP_CHANGE = 2
NETMSG_MAP_DATA = 3
NETMSG_CON_READY = 4
NETMSG_SNAP = 5
NETMSG_SNAPEMPTY = 6
NETMSG_SNAPSINGLE = 7
NETMSG_SNAPSMALL = 8
NETMSG_INPUTTIMING = 9
NETMSG_RCON_AUTH_STATUS = 10
NETMSG_RCON_LINE = 11
NETMSG_AUTH_CHALLANGE = 12
NETMSG_AUTH_RESULT = 13
NETMSG_READY = 14
NETMSG_ENTERGAME = 15
NETMSG_INPUT = 16
NETMSG_RCON_CMD = 17
NETMSG_RCON_AUTH = 17
NETMSG_REQUEST_MAP_DATA = 18
NETMSG_AUTH_START = 19
NETMSG_AUTH_RESPONSE = 20
NETMSG_PING = 21
NETMSG_PING_REPLY = 22
NETMSG_ERROR = 23
NETMSG_RCON_CMD_ADD = 24
NETMSG_RCON_CMD_REM = 25

# Game messages
NETMSGTYPE_INVALID = 0
NETMSGTYPE_SV_MOTD = 1
NETMSGTYPE_SV_BROADCAST = 2
NETMSGTYPE_SV_CHAT = 3
NETMSGTYPE_SV_KILLMSG = 4
NETMSGTYPE_SV_SOUNDGLOBAL = 5
NETMSGTYPE_SV_TUNEPARAMS = 6
NETMSGTYPE_SV_EXTRAPROJECTILE = 7
NETMSGTYPE_SV_READYTOENTER = 8
NETMSGTYPE_SV_WEAPONPICKUP = 9
NETMSGTYPE_SV_EMOTICON = 10
NETMSGTYPE_SV_VOTECLEAROPTIONS = 11
NETMSGTYPE_SV_VOTEOPTIONLISTADD = 12
NETMSGTYPE_SV_VOTEOPTIONADD = 13
NETMSGTYPE_SV_VOTEOPTIONREMOVE = 14
NETMSGTYPE_SV_VOTESET = 15
NETMSGTYPE_SV_VOTESTATUS = 16
NETMSGTYPE_CL_SAY = 17
NETMSGTYPE_CL_SETTEAM = 18
NETMSGTYPE_CL_SETSPECTATORMODE = 19
NETMSGTYPE_CL_STARTINFO = 20
NETMSGTYPE_CL_CHANGEINFO = 21
NETMSGTYPE_CL_KILL = 22
NETMSGTYPE_CL_EMOTICON = 23
NETMSGTYPE_CL_VOTE = 24
NETMSGTYPE_CL_CALLVOTE = 25
NETMSGTYPE_CL_ISDDNETLEGACY = 26
NETMSGTYPE_SV_DDRACETIMELEGACY = 27
NETMSGTYPE_SV_RECORDLEGACY = 28
NETMSGTYPE_UNUSED = 29
NETMSGTYPE_SV_TEAMSSTATELEGACY = 30
NETMSGTYPE_CL_SHOWOTHERSLEGACY = 31

SERVER_TICK_SPEED = 50
SERVER_FLAG_PASSWORD = 0x1
MAX_CLIENTS = 64
VANILLA_MAX_CLIENTS = 16
MAX_INPUT_SIZE = 128
MAX_SNAPSHOT_PACKSIZE = 900
MAX_NAME_LENGTH = 16
MAX_CLAN_LENGTH = 12
# message packing
MSGFLAG_VITAL = 1
MSGFLAG_FLUSH = 2
MSGFLAG_NORECORD = 4
MSGFLAG_RECORD = 8
MSGFLAG_NOSEND = 16

VERSION_VANILLA = 0
VERSION_DDRACE = 1
VERSION_DDNET_OLD = 2
VERSION_DDNET_WHISPER = 217
VERSION_DDNET_GOODHOOK = 221
VERSION_DDNET_EXTRATUNES = 302
VERSION_DDNET_RCONPROTECT = 408
VERSION_DDNET_ANTIPING_PROJECTILE = 604
VERSION_DDNET_HOOKDURATION_TUNE = 607
VERSION_DDNET_FIREDELAY_TUNE = 701
VERSION_DDNET_UPDATER_FIXED = 707
VERSION_DDNET_GAMETICK = 10042


# UUID

UUID_MAXSTRSIZE = 37  # 12345678-0123-5678-0123-567890123456
UUID_INVALID = -2
UUID_UNKNOWN = -1
OFFSET_UUID = 1 << 16

NETMSG_EX_INVALID = UUID_INVALID
NETMSG_EX_UNKNOWN = UUID_UNKNOWN
OFFSET_NETMSG_UUID = OFFSET_UUID
__NETMSG_UUID_HELPER = OFFSET_NETMSG_UUID - 1

NETMSG_WHATIS = __NETMSG_UUID_HELPER + 1
NETMSG_ITIS = __NETMSG_UUID_HELPER + 2
NETMSG_IDONTKNOW = __NETMSG_UUID_HELPER + 3

NETMSG_RCON_TYPE = __NETMSG_UUID_HELPER + 4
NETMSG_MAP_DETAILS = __NETMSG_UUID_HELPER + 5
NETMSG_CAPABILITIES = __NETMSG_UUID_HELPER + 6
NETMSG_CLIENTVER = __NETMSG_UUID_HELPER + 7
NETMSG_PINGEX = __NETMSG_UUID_HELPER + 8
NETMSG_PONGEX = __NETMSG_UUID_HELPER + 9
NETMSG_CHECKSUM_REQUEST = __NETMSG_UUID_HELPER + 10
NETMSG_CHECKSUM_RESPONSE = __NETMSG_UUID_HELPER + 11
NETMSG_CHECKSUM_ERROR = __NETMSG_UUID_HELPER + 12
