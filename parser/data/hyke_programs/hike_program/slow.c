HIKE_PROG(slow)
{
    __u64 *R0 = _I_RREG(0);

    bpf_printk("HIKe Prog: slow REG_0=0x%llx", *R0);

    return HIKE_XDP_VM;
}
EXPORT_HIKE_PROG(slow, HIKE_EBPF_PROG_SLOW);