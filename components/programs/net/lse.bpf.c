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

#include "ip6_hset.h"

#define HIKE_PCPU_LSE_MAX 4096

bpf_map(map_pcpu_lse,
		LRU_PERCPU_HASH,
		struct ipv6_hset_srcdst_key,
		struct ipv6_hset_value,
		HIKE_PCPU_LSE_MAX);

/* per-CPU Event Monitor HIKe Program
 *
 * input:
 * - ARG1:	HIKe Program ID;
 */
HIKE_PROG(pcpu_lse)
{
	struct pkt_info *info = hike_pcpu_shmem();
	struct ipv6_hset_value new_val, *val;
	struct ipv6_hset_srcdst_key key;
	struct hdr_cursor *cur;
	__u64 current, tmp;
	int rc;

	/* take the reference to the cursor object which has been saved into
	 * the HIKe per-cpu shared memory
	 */
	cur = pkt_info_cur(info);
	if (unlikely(!cur))
		goto drop;

	rc = ipv6_hset_srcdst_get_key(ctx, cur, &key);
	if (unlikely(rc < 0))
		goto drop;

	current = bpf_ktime_get_ns();

	val = bpf_map_lookup_elem(&map_pcpu_lse, &key);
	if (!val)
	{
		/* new_val should be set to 0, anyway it is only made of one
		 * field. Keep in mind if you add more fields to that
		 * structure.
		 */
		new_val.cts_ns = current;
		new_val.timeout_ns = 0; /* not used here */
		bpf_map_update_elem(&map_pcpu_lse, &key, &new_val, BPF_ANY);

		/* since we do not have any previous time reference, we return
		 * an "invalid" timestamp.  In this way the caller can
		 * understand whether the event has been seen for the fist time
		 * or not.
		 */
		tmp = ~0ul;
		goto out;
	}

	tmp = current - val->cts_ns;
	val->cts_ns = current;
out:
	HVM_RET = tmp;
	return HIKE_XDP_VM;

drop:
	DEBUG_PRINT("ipv6_flow_meter_srcdst: drop packet");
	return HIKE_XDP_ABORTED;
}
EXPORT_HIKE_PROG(pcpu_lse);
EXPORT_HIKE_PROG_MAP(pcpu_lse, map_pcpu_lse);

char LICENSE[] SEC("license") = "Dual BSD/GPL";
