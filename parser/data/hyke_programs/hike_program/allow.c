HIKE_PROG(allow_any)
{
	bpf_printk("HIKe Prog: allow_any REG_1=0x%llx, REG_2=0x%llx", _I_REG(1), _I_REG(2));

	return XDP_PASS;
}
EXPORT_HIKE_PROG(allow_any, HIKE_EBPF_PROG_ALLOW_ANY);

