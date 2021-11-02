#define HIKE_EBPF_PROG_TEST_ALLOW_ANY 13
#define HIKE_CHAIN_TEST_MINIMAL_CHAIN 10
# include <linux/errno.h>

# include "hike_vm.h"
# include "parse_helpers.h"


//__sec_hike_chain_
HIKE_CHAIN_1(HIKE_CHAIN_TEST_MINIMAL_CHAIN)
{
# define __ETH_PROTO_TYPE_ABS_OFF 12

	__u16 eth_type;

	hike_packet_read_u16(&eth_type, __ETH_PROTO_TYPE_ABS_OFF);
	if (eth_type == 0x800)
	{
		hike_elem_call_2(HIKE_EBPF_PROG_TEST_ALLOW_ANY, 2);
	}

	if (eth_type == 0x86dd)
	{
		hike_elem_call_2(HIKE_EBPF_PROG_TEST_ALLOW_ANY, 2);
	}

	return 0;
# undef __ETH_PROTO_TYPE_ABS_OFF
}
