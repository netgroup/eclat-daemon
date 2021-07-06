// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause


#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#define HIKE_DEBUG 1
#include "hike_vm.h"

/* HIKe Chain IDs and XDP eBPF/HIKe programs IDs */
#include "minimal.h"

#include "eclat_output.c"

HIKE_CHAIN_1(HIKE_CHAIN_FOO_ID)
{
#define __ETH_PROTO_TYPE_ABS_OFF	12
#define __IPV4_TOTAL_LEN_ABS_OFF	16
#define __IPV6_HOP_LIM_ABS_OFF		21
	__u16 eth_type;
	__u8 allow = 1;			/* allow any by default */
	__u16 ip4_len;
	__u8 hop_lim;

	hike_packet_read_u16(&eth_type, __ETH_PROTO_TYPE_ABS_OFF);
	if (eth_type == 0x800) {
		hike_packet_read_u16(&ip4_len, __IPV4_TOTAL_LEN_ABS_OFF);
		if (ip4_len >= 128)
			goto out;

		/* drop any IPv4 packet if IPv4 Total Len  < 128 */
		allow = 0;
		goto out;
	}

	if (eth_type == 0x86dd) {
		/* change the TTL of the IPv6 packet */
		hike_packet_read_u8(&hop_lim, __IPV6_HOP_LIM_ABS_OFF);
		if (hop_lim != 64)
			goto out;

		/* rewrite the hop_limit */
		hike_packet_write_u8(__IPV6_HOP_LIM_ABS_OFF, 17);
	}

out:
	hike_elem_call_3(HIKE_CHAIN_BAR_ID, allow, eth_type);

	return 0;
#undef __ETH_PROTO_TYPE_ABS_OFF
#undef __IPV4_TOTAL_LEN_ABS_OFF
#undef __IPV6_HOP_LIM_ABS_OFF
}

HIKE_CHAIN_3(HIKE_CHAIN_BAR_ID, __u8, allow, __u16, eth_type)
{
	__u32 prog_id = allow ? HIKE_EBPF_PROG_ALLOW_ANY :
				HIKE_EBPF_PROG_DROP_ANY;
	/* FIXME: counter is an u64 but for the moment we consider it u16;
	 * shift operators still need to be implemented in HIKe VM...
	 */
	__u8 override = 0;
	__u16 counter;

	/* let's count the number of processed packet based on the allow flag.
	 * In counter we have the number of allowed or dropped packets, so far.
	 */
	counter = hike_elem_call_2(HIKE_EBPF_PROG_COUNT_PACKET, allow);
	if (allow)
		goto out;

	if ((__s16)counter < 0) {
		prog_id = HIKE_EBPF_PROG_DROP_ANY;
		override = 1;
	} else if (counter >= 32) {
		/* when the number of dropped packet is above a given
		 * threshold, override the prog and the alow code.
		 */
		prog_id = HIKE_EBPF_PROG_ALLOW_ANY;
		override = 1;
	}

	if (override)
		/* increase also the override counter rather than allow or
		 * drop. We can call the same program many times (until you do
		 * not hit the tail call limit.
		 */
		hike_elem_call_2(HIKE_EBPF_PROG_COUNT_PACKET, 2);
out:
	hike_elem_call_2(prog_id, eth_type);

	/* prog_id is a final HIKe Program, we should not return from this
	 * call. If we return from that call, it means that we have experienced
	 * some issues... so the HIKe VM applies the default policy on such a
	 * packet.
	 */
	return 0;
}
