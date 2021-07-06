HIKE_PROG(parse_ethernet)
{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct hdr_cursor nh;
    struct ethhdr *eth;
    __be16 h_proto;

    nh.pos = data;

    h_proto = parse_ethhdr(&nh, data_end, &eth);
    _I_REG(0) = 0xffff & bpf_ntohs(h_proto);

    return HIKE_XDP_VM;
}
EXPORT_HIKE_PROG(parse_ethernet, HIKE_EBPF_PROG_PARSE_ETHERNET_ANY);