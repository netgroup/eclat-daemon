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

/* Loader program is a plain eBPF XDP program meant for invoking an HIKe Chain.
 * For the moment, the chain ID is harcoded.
 */
__section("hike_loader")
int __xdp_hike_loader(struct xdp_md *ctx)
{
	const __u32 chain_id = HIKE_CHAIN_FOO_ID;
	int rc;

	bpf_printk(">>> HIKe VM Chain Boostrap, chain_ID=0x%x", chain_id);

	rc = hike_chain_boostrap(ctx, chain_id);

	bpf_printk(">>> HIKe VM Chain Boostrap, chain ID=0x%x returned=%d",
		   chain_id, rc);

	return XDP_ABORTED;
}

__section("xdp_pass")
int xdp_pass_prog(struct xdp_md *ctx)
{
	return XDP_PASS;
}

/* ~~~~~~~~~~~~~~~~~~~~~ XDP eBPF/HIKe programs ~~~~~~~~~~~~~~~~~~~~ */

HIKE_PROG(allow_any)
{
	bpf_printk("HIKe Prog: allow_any REG_1=0x%llx, REG_2=0x%llx",
		   _I_REG(1), _I_REG(2));

	return XDP_PASS;
}
EXPORT_HIKE_PROG(allow_any);

HIKE_PROG(drop_any)
{
	bpf_printk("HIKe Prog: drop_any REG_1=0x%llx, REG_2=0x%llx",
		   _I_REG(1), _I_REG(2));

	return XDP_DROP;
}
EXPORT_HIKE_PROG(drop_any);

/* this HIKe program does not decide about the fate of the packet. Instead,
 * after being executed, it returns the control to the HIKe VM. Packet
 * processing continues in the calling HIKe Chain.
 */

#ifndef lock_xadd
#define lock_xadd(ptr, val)	((void)__sync_fetch_and_add(ptr, val))
#endif

enum {
	HIKE_PROG_MAP_COUNT_ALLOW	= 0,
	HIKE_PROG_MAP_COUNT_DENY	= 1,
	HIKE_PROG_MAP_COUNT_OVERRIDE	= 2,
	HIKE_PROG_MAP_COUNT_ERROR	= 3,
	__HIKE_PROG_MAP_COUNT_MAX,
};

#define HIKE_PROG_MAP_COUNT_MAX (__HIKE_PROG_MAP_COUNT_MAX - 1)
bpf_map(map_count_packet, ARRAY, __u32, __u32,
	HIKE_PROG_MAP_COUNT_MAX + 1);

/* count_packet takes 2 args: REG1 -> HIKE_PROG_ID, REG2 -> allow */
HIKE_PROG(count_packet)
{
	__u16 ret = -EINVAL; /* we consider only first 16 bits of counters */
	__u32 *value;
	__u32 key;

	bpf_printk("HIKe Prog: count_packet REG_1=0x%llx, REG_2=0x%llx",
		   _I_REG(1), _I_REG(2));

	key = _I_REG(2);
	switch (key) {
	case HIKE_PROG_MAP_COUNT_ALLOW:
	case HIKE_PROG_MAP_COUNT_DENY:
	case HIKE_PROG_MAP_COUNT_OVERRIDE:
		break;
	case HIKE_PROG_MAP_COUNT_ERROR:
	default:
		key = HIKE_PROG_MAP_COUNT_ERROR;
		break;
	}

	value = bpf_map_lookup_elem(&map_count_packet, &key);
	if (!value)
		goto out;

	/* and now a question for you... why do we need of this ? ;-) */
	lock_xadd(value, 1);
	ret = *value;
out:
	/* return the value to the HIKe Chain (the caller) */
	_I_REG(0) = ret;
	return HIKE_XDP_VM;
}
EXPORT_HIKE_PROG(count_packet);
EXPORT_HIKE_PROG_MAP(count_packet, map_count_packet);

char LICENSE[] SEC("license") = "Dual BSD/GPL";
