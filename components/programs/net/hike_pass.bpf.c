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

HIKE_PROG(hike_pass)
{
	DEBUG_PRINT("HIKe Prog: hike_pass REG_1=0x%llx", _I_REG(1));

	return XDP_PASS;
}
EXPORT_HIKE_PROG(hike_pass);

char LICENSE[] SEC("license") = "Dual BSD/GPL";
