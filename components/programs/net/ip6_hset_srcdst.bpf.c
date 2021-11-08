// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause

#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

/* HIKe Chain IDs and XDP eBPF/HIKe programs IDs */
//#include "minimal.h"

#include "hike_vm.h"
#include "parse_helpers.h"

/* maps are defined here */
#include "ip6_hset.h"

bpf_map(ipv6_hset_srcdst_map,
		HASH,
		struct ipv6_hset_srcdst_key,
		struct ipv6_hset_value,
		HIKE_IPV6_HSET_MAX);

static __always_inline struct ipv6_hset_value *
ipv6_hset_srcdst_get_value(struct ipv6_hset_srcdst_key *key)
{
	return bpf_map_lookup_elem(&ipv6_hset_srcdst_map, key);
}

static __always_inline int
ipv6_hset_srcdst_key_exists(struct ipv6_hset_srcdst_key *key)
{
	return ipv6_hset_srcdst_get_value(key) ? 0 : -ENOENT;
}

static __always_inline int
ipv6_hset_srcdst_add_key(struct ipv6_hset_srcdst_key *key)
{
	struct ipv6_hset_value val = {
		0,
	};

	val.timeout_ns = HIKE_IPV6_HSET_EXP_TIMEOUT_NS;
	val.cts_ns = bpf_ktime_get_ns();

	return bpf_map_update_elem(&ipv6_hset_srcdst_map, key, &val,
							   BPF_NOEXIST);
}

static __always_inline int
ipv6_hset_srcdst_del_key(struct ipv6_hset_srcdst_key *key)
{
	return bpf_map_delete_elem(&ipv6_hset_srcdst_map, key);
}

static __always_inline int
ipv6_hset_srcdst_del_key_timeout(struct ipv6_hset_srcdst_key *key)
{
	struct ipv6_hset_value *val;
	__u64 current, timeout;

	val = ipv6_hset_srcdst_get_value(key);
	if (!val)
		return -ENOENT;

	current = bpf_ktime_get_ns();
	timeout = val->cts_ns + val->timeout_ns;

	if (timeout > current)
		return 0;

	ipv6_hset_srcdst_del_key(key);
	return -ENOENT;
}

/* HIKe Program
 * IPv6 Hahset on <SA,DA>
 *
 * The program allows the user to interact with the IPv6 <DA,SA> HSet.
 * Based on the action argument (ARG2), the program is able to:
 *   i) with ARG2 == IPV6_HSET_ACTION_LOOKUP, check whether the packet is in
 *	the blacklist or not;
 *  ii) with ARG2 == IPV6_HSET_ACTION_ADD, add the packet to the blacklist if
 *	it is not already present.
 *
 * input:
 * - ARG1:	HIKe Program ID;
 * - ARG2:	action
 *
 * output:
 *  - REG0:	ret code operation
 */
HIKE_PROG(ipv6_hset_srcdst)
{
	struct pkt_info *info = hike_pcpu_shmem();
	struct ipv6_hset_srcdst_key key;
	struct hdr_cursor *cur;
	int action = HVM_ARG2;
	int rc;

	/* take the reference to the cursor object which has been saved into
	 * the HIKe per-cpu shared memory
	 */
	cur = pkt_info_cur(info);
	if (unlikely(!cur))
		goto drop;

	/* ctx is injected by the HIKE VM */
	rc = ipv6_hset_srcdst_get_key(ctx, cur, &key);
	if (unlikely(rc < 0))
		goto drop;

	switch (action)
	{
	case IPV6_HSET_ACTION_LOOKUP:
		rc = ipv6_hset_srcdst_key_exists(&key);
		break;
	case IPV6_HSET_ACTION_ADD:
		rc = ipv6_hset_srcdst_add_key(&key);
		break;
	case IPV6_HSET_ACTION_LOOKUP_AND_CLEAN:
		rc = ipv6_hset_srcdst_del_key_timeout(&key);
		break;
	default:
		/* default case */
		goto drop;
	}

	HVM_RET = rc;
	return HIKE_XDP_VM;

drop:
	DEBUG_PRINT("ipv6_hset_srcdst: drop packet");
	return HIKE_XDP_ABORTED;
}
EXPORT_HIKE_PROG_2(ipv6_hset_srcdst, __u64, action);
EXPORT_HIKE_PROG_MAP(ipv6_hset_srcdst, ipv6_hset_srcdst_map);

char LICENSE[] SEC("license") = "Dual BSD/GPL";
