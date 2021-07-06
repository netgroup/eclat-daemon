HIKE_PROG(get_ingress_ifindex)
{
    bpf_printk("HIKe Prog: get_ingress_ifindex REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

    return 11;
}
EXPORT_HIKE_PROG(get_ingress_ifindex, HIKE_EBPF_PROG_GET_INGRESS_IFINDEX);