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

char LICENSE[] SEC("license") = "Dual BSD/GPL";