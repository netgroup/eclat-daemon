class Packet():
    def readU8(parametri):
        return "hike_packet_read_u8(" + parametri

    def readU16(parametri):
        return "hike_packet_read_u16(" + parametri
        
    def readU32(parametri):
        return "hike_packet_read_u32(" + parametri
        
    def readU64(parametri):
        return "hike_packet_read_u64(" + parametri
        
    # parametri[2:] per eliminare lo spazio e la virgola
    # all'inizio della stringa
    def writeU8(parametri):
        return "hike_packet_write_u8(" + parametri[2:]

    def writeU16(parametri):
        return "hike_packet_write_u16(" + parametri[2:]

    def writeU32(parametri):
        return "hike_packet_write_u32(" + parametri[2:]

    def writeU64(parametri):
        return "hike_packet_write_u64(" + parametri[2:]
