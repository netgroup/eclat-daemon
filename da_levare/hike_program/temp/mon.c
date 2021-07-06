HIKE_PROG(mon)
{
    __u64 *R0 = _I_RREG(0);

    bpf_printk("HIKe Prog: mon REG_0=0x%llx", *R0);

    return HIKE_XDP_VM;
}
EXPORT_HIKE_PROG(mon, HIKE_EBPF_PROG_MON);