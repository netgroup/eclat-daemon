
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

bpf_map(ipv6_sc_map, ARRAY, __u32, __u32, 1);

static __always_inline int __hvxdp_handle_ipv6(struct xdp_md *ctx, struct pkt_info *info)
{
	struct hdr_cursor *cur = pkt_info_cur(info);
	struct ipv6hdr *ip6h;
	const __u32 key = 0;
	__u32 *chain_id;
	int nexthdr;
	int rc;

	if (!unlikely(cur))
		return XDP_ABORTED;

	nexthdr = parse_ip6hdr(ctx, cur, &ip6h);
	if (!ip6h || nexthdr < 0)
		return XDP_PASS;

	cur_reset_transport_header(cur);

	/* load the Chain-ID directly from the classifier config map */
	chain_id = bpf_map_lookup_elem(&ipv6_sc_map, &key);
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

__section("ipv6_sc") int __ipv6_sc(struct xdp_md *ctx)
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
	switch (proto)
	{
	case ETH_P_IPV6:
		return __hvxdp_handle_ipv6(ctx, info);
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
EXPORT_HIKE_MAP(__ipv6_sc, ipv6_sc_map);

char LICENSE[] SEC("license") = "Dual BSD/GPL";
