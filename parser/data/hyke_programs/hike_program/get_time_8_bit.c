HIKE_PROG(get_time_8_bit)
{
    bpf_printk("HIKe Prog: get_time_8_bit REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return 12;
}
EXPORT_HIKE_PROG(get_time_8_bit, HIKE_EBPF_PROG_GET_TIME_8_BIT);