import unittest
from controller import EclatController
from chainloader import ChainLoader
import settings


class TestLoader(unittest.TestCase):
    def test_loader1(self):
        code = """
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
"""

        cl = ChainLoader(name="minimal_loader", package="test",
                         code=code)
        cl.clean()
        cl.compile()
        # hc.load()
