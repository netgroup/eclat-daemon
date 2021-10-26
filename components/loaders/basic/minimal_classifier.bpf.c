
#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

/* HIKe Chain IDs and XDP eBPF/HIKe programs IDs */
#include "minimal.h"

#include "hike_vm.h"
#include "parse_helpers.h"

#define MAP_IPV6_SIZE	64
bpf_map(map_ipv6, HASH, struct in6_addr, __u32, MAP_IPV6_SIZE);

static __always_inline
int __hvxdp_handle_ipv6(struct xdp_md *ctx, struct hdr_cursor *cur)
{
	struct in6_addr *key;
	struct ipv6hdr *ip6h;
	__u32 *chain_id;
	int nexthdr;
	int rc;

	nexthdr = parse_ip6hdr(ctx, cur, &ip6h);
	if (!ip6h || nexthdr < 0)
		return XDP_PASS;

	cur_reset_transport_header(cur);

	/* let's find out the chain id associated with the IPv6 DA */
	key = &ip6h->daddr;
	chain_id = bpf_map_lookup_elem(&map_ipv6, key);
	if (!chain_id)
		/* value not found, deliver the packet to the kernel */
		return XDP_PASS;

	DEBUG_PRINT("HIKe VM invoking Chain ID=0x%x", *chain_id);

	rc = hike_chain_boostrap(ctx, *chain_id);

	/* the fallback behavior of this classifier consists in dropping any
	 * packet that has not been delivered by any of the selected HIKe
	 * Chains in an explicit way.
	 */
	if (rc < 0)
		DEBUG_PRINT("HIKe VM returned error code=%d", rc);

	return XDP_ABORTED;
}

__section("hike_classifier")
int __hike_classifier(struct xdp_md *ctx)
{
	struct pkt_info *info = hike_pcpu_shmem();
	struct hdr_cursor *cur;
	struct ethhdr *eth;
	__be16 eth_type;
	__u16 proto;

	if (!info)
		return XDP_ABORTED;

	cur = pkt_info_cur(info);
	cur_init(cur);

	eth_type = parse_ethhdr(ctx, cur, &eth);
	if (!eth || eth_type < 0)
		return XDP_ABORTED;	

	/* set the network header */
	cur_reset_network_header(cur);

	proto = bpf_htons(eth_type);
	switch (proto) {
	case ETH_P_IPV6:
		return __hvxdp_handle_ipv6(ctx, cur);
	case ETH_P_IP:
		/* fallthrough */
	default:
		DEBUG_PRINT("HIKe VM Classifier passthrough for proto=%x",
			    bpf_htons(eth_type));
		break;
	}

	/* default policy allows any unrecognized packed... */
	return XDP_PASS;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";
