
#include <linux/errno.h>
#include "hike_vm.h"
#include "parse_helpers.h"

#define HIKE_EBPF_PROG_NET_HIKE_DROP 1
#define HIKE_EBPF_PROG_NET_HIKE_PASS 2
#define HIKE_EBPF_PROG_NET_IP6_HSET_SRCDST 3
#define HIKE_EBPF_PROG_NET_LSE 4
#define HIKE_EBPF_PROG_NET_MONITOR 5
#define HIKE_CHAIN_DDOS_PKG_DDOS 6
HIKE_CHAIN_1(HIKE_CHAIN_DDOS_PKG_DDOS)
{
        __u64 rs = hike_elem_call_2(HIKE_EBPF_PROG_NET_IP6_HSET_SRCDST, 2);
        if (!rs)
        {
                hike_elem_call_2(HIKE_EBPF_PROG_NET_MONITOR, 1);
                hike_elem_call_1(HIKE_EBPF_PROG_NET_HIKE_DROP);
                return 0;
        }
        __u64 ts = hike_elem_call_1(HIKE_EBPF_PROG_NET_LSE);
        if (ts < 500000000)
        {
                hike_elem_call_2(HIKE_EBPF_PROG_NET_IP6_HSET_SRCDST, 1);
                hike_elem_call_1(HIKE_EBPF_PROG_NET_HIKE_DROP);
                return 0;
        }
        hike_elem_call_2(HIKE_EBPF_PROG_NET_MONITOR, 0);
        hike_elem_call_1(HIKE_EBPF_PROG_NET_HIKE_PASS);
        return 0;
}
