// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause
/* Copyright (c) 2020 Facebook */
#include <linux/bpf.h>
#include <linux/btf.h>
#include <bpf/bpf_helpers.h>

#error "It won't compile!"

char LICENSE[] SEC("license") = "Dual BSD/GPL";

bpf_map(jmp_table, PROG_ARRAY, __u32, __u32, 8);

struct __hike_foo_map_value {
	unsigned int a;
	short b;
	unsigned short __pad;
};
bpf_map(hike_foo_map, ARRAY, __u32, struct __hike_foo_map_value, 4);
bpf_map(hike_bar_map, ARRAY, int, __u64, 16);

SEC("xdp_root")
int xdp_prog_1(struct xdp_md *ctx)
{
	bpf_printk(">>> xdp_1 called<<<");

	bpf_tail_call(ctx, &jmp_table, 2);

	bpf_printk(">>> xdp_1 tail_call fallback<<<");

	return XDP_PASS;
}

SEC("xdp/2")
int xdp_prog_2(struct xdp_md *ctx)
{
	bpf_printk(">>> xdp_2 called<<<");

	return XDP_DROP;
}
HIKE_MAP_EXPORT(xdp_prog_2, hike_bar_map);

SEC("xdp/3")
int xdp_prog_3(struct xdp_md *ctx)
{
	struct __hike_foo_map_value v = { .a = 17, .b = 3, .__pad = 0, };
	__u32 key = 0;

	bpf_map_update_elem(&hike_foo_map, &key, &v, 0); 

	bpf_printk(">>> xdp_3 called<<<");

	return XDP_PASS;
}
HIKE_MAP_EXPORT(xdp_prog_3, hike_bar_map);
HIKE_MAP_EXPORT(xdp_prog_3, hike_foo_map);
