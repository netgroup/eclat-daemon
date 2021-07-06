HIKE_PROG(get_iflabel_id)
{
    bpf_printk("HIKe Prog: get_iflabel_id REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return 10;
}
EXPORT_HIKE_PROG(get_iflabel_id, HIKE_EBPF_PROG_GET_IFLABEL_ID);