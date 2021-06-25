
#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#define HIKE_DEBUG 1
#include "hike_vm.h"
#include "hdr_cursor.h"

/*
 *	struct vlan_hdr - vlan header
 *	@h_vlan_TCI: priority and VLAN ID
 *	@h_vlan_encapsulated_proto: packet type ID or len
 */
struct vlan_hdr {
	__be16	h_vlan_TCI;
	__be16	h_vlan_encapsulated_proto;
};

/* Allow users of header file to redefine VLAN max depth */
#ifndef VLAN_MAX_DEPTH
#define VLAN_MAX_DEPTH 4
#endif

static __always_inline int proto_is_vlan(__u16 h_proto)
{
	return !!(h_proto == bpf_htons(ETH_P_8021Q) ||
		  h_proto == bpf_htons(ETH_P_8021AD));
}

static __always_inline int parse_ethhdr(struct hdr_cursor *cur,
					struct ethhdr **ethhdr)
{
	struct ethhdr *eth = cur_data(cur);
	struct vlan_hdr *vlh;
	__u16 h_proto;
	int i;

	/* Byte-count bounds check; check if current pointer + size of header
	 * is after data_end.
	 */
	if (!cur_may_pull(cur, sizeof(*eth)))
		return -ENOBUFS;

	if (ethhdr)
		*ethhdr = eth;

	vlh = cur_pull(cur, sizeof(*eth));
	h_proto = eth->h_proto;

	/* Use loop unrolling to avoid the verifier restriction on loops;
	 * support up to VLAN_MAX_DEPTH layers of VLAN encapsulation.
	 */
#pragma unroll
	for (i = 0; i < VLAN_MAX_DEPTH; i++) {
		if (!proto_is_vlan(h_proto))
			break;

		if (!cur_may_pull(cur, sizeof(*vlh)))
			break;

		h_proto = vlh->h_vlan_encapsulated_proto;
		cur_pull(cur, sizeof(*vlh));
	}

	return h_proto; /* network-byte-order */
}

static __always_inline int parse_ip6hdr(struct hdr_cursor *cur,
					struct ipv6hdr **ip6hdr)
{
	struct ipv6hdr *ip6h = cur_data(cur);

	/* Pointer-arithmetic bounds check; pointer +1 points to after end of
	 * thing being pointed to. We will be using this style in the remainder
	 * of the tutorial.
	 */
	if (!cur_may_pull(cur, sizeof(*ip6h)))
		return -ENOBUFS;

	if (ip6hdr)
		*ip6hdr = ip6h;

	cur_pull(cur, sizeof(*ip6h));

	return ip6h->nexthdr;
}


#define MAP_IPV6_SIZE	64
bpf_map(map_ipv6, HASH, struct in6_addr, __u32, MAP_IPV6_SIZE);

static __always_inline
int __hvxdp_handle_ipv6(struct hdr_cursor *cur, struct xdp_md *ctx)
{
	struct in6_addr *key;
	struct ipv6hdr *ip6h;
	__u32 *chain_id;
	int nexthdr;
	int rc;

	nexthdr = parse_ip6hdr(cur, &ip6h);
	if (!ip6h || nexthdr < 0)
		goto pass;

	cur_reset_transport_header(cur);

	/* let's find out the chain id associated with the IPv6 DA */
	key = &ip6h->daddr;
	chain_id = bpf_map_lookup_elem(&map_ipv6, key);
	if (!chain_id)
		/* value not found, deliver the packet to the kernel */
		goto pass;

	DEBUG_PRINT("HIKe VM invoking Chain ID=0x%x", *chain_id);

	rc = hike_chain_boostrap(ctx, *chain_id);
	/* fallback */
	if (rc < 0)
		DEBUG_PRINT("HIKe VM returned error code=%d", rc);

pass:
	return XDP_PASS;
}

__section("hike_classifier")
int __hike_classifier(struct xdp_md *ctx)
{
	struct hdr_cursor cur;
	struct ethhdr *eth;
	__be16 eth_type;
	__u16 proto;

	cur_init(&cur, ctx);

	eth_type = parse_ethhdr(&cur, &eth);
	if (!eth || eth_type < 0)
		goto out;

	/* set the network header */
	cur_reset_network_header(&cur);

	proto = bpf_htons(eth_type);
	switch (proto) {
	case ETH_P_IPV6:
		return __hvxdp_handle_ipv6(&cur, ctx);
	case ETH_P_IP:
		/* fallthrough */
	default:
		/* TODO: IPv4 for the moment is not supported */
		DEBUG_PRINT("HIKe VM Classifier passthrough for proto=%x",
			    bpf_htons(eth_type));
		goto out;
	}

	/* default policy allows any unrecognized packed... */
out:
	return XDP_PASS;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";
