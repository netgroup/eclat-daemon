HIKE_PROG(drop_any)
{
    bpf_printk("HIKe Prog: drop_any REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return XDP_DROP;
}
EXPORT_HIKE_PROG(drop_any, HIKE_EBPF_PROG_DROP_ANY);