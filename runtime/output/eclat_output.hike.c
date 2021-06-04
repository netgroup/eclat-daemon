
#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#define HIKE_DEBUG 1
#include "hike_vm.h"

#define HIKE_CHAIN_75_ID 75
#define HIKE_CHAIN_76_ID 76

#define HIKE_EBPF_PROG_DROP_ANY 12

#define HIKE_EBPF_PROG_ALLOW_ANY 11

HIKE_CHAIN_1(HIKE_CHAIN_75_ID) {
	__u64 eth_type;
	__u64 ttl;
	hike_packet_read_u16(&eth_type, 12);
	if ( eth_type == 0x86dd ) {
		hike_elem_call_2(HIKE_EBPF_PROG_DROP_ANY, eth_type);
		return 0;
	}
	ttl = 64;
	if ( eth_type == 0x800 ) {
		hike_packet_write_u8(ttl, 22);
	}
	hike_elem_call_2(HIKE_EBPF_PROG_ALLOW_ANY, eth_type);

	return 0;
}

HIKE_CHAIN_1(HIKE_CHAIN_76_ID) {
	__u64 eth_type;
	__u64 ttl;
	hike_packet_read_u16(&eth_type, 12);
	if ( eth_type == 0x86dd ) {
		hike_packet_read_u8(&ttl, 21);
		if ( ttl == 64 ) {
			hike_packet_write_u8(17, 21);
		}
	}
	if ( eth_type == 0x800 ) {
		hike_elem_call_2(HIKE_EBPF_PROG_DROP_ANY, eth_type);
		return 0;
	}
	hike_elem_call_2(HIKE_EBPF_PROG_ALLOW_ANY, eth_type);
	return 0;
	
}
