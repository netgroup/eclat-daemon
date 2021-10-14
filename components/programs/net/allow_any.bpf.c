// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause

#include <stddef.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ipv6.h>
#include <linux/seg6.h>
#include <linux/errno.h>

#include "hike_vm.h"
#include "parse_helpers.h"

HIKE_PROG(allow_any)
{
    DEBUG_PRINT("HIKe Prog: allow_any REG_1=0x%llx, REG_2=0x%llx",
                _I_REG(1), _I_REG(2));

    return XDP_PASS;
}
EXPORT_HIKE_PROG(allow_any);