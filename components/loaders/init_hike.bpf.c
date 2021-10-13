#include <stddef.h>

/* HIKe Chain IDs and XDP eBPF/HIKe programs IDs */
#define HIKE_DEBUG 0

#include "hike_vm.h"

__section("hike_init") int __hike_init(struct xdp_md *ctx)
{

	/* default policy allows any unrecognized packed... */
	return XDP_PASS;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";
