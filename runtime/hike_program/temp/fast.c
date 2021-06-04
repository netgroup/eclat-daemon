HIKE_PROG(fast)
{
    bpf_printk("HIKe Prog: fast REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return HIKE_XDP_VM;
}
EXPORT_HIKE_PROG(fast, HIKE_EBPF_PROG_FAST);