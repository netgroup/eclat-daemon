HIKE_PROG(pkt_mem_move)
{
    bpf_printk("HIKe Prog: pkt_mem_move REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return XDP_PASS;
}
EXPORT_HIKE_PROG(pkt_mem_move, HIKE_EBPF_PROG_PKT_MEM_MOVE);