#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#define HIKE_DEBUG 1
#include "hike_vm.h"


#define HIKE_CHAIN_76_ID 76

#define HIKE_EBPF_PROG_DROP_ANY 12

HIKE_CHAIN_1(HIKE_CHAIN_76_ID) {
	hike_elem_call_1(HIKE_EBPF_PROG_DROP_ANY);
	return 0;
}
