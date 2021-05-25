HIKE_PROG(interface_load)
{
    bpf_printk("HIKe Prog: get_time_8_bit REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return 13;
}
EXPORT_HIKE_PROG(interface_load, HIKE_EBPF_PROG_PKT_INTERFACE_LOAD);