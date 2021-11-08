
#ifndef _MAP_H
#define _MAP_H

#include <linux/bpf.h>
#include <linux/btf.h>
#include <bpf/bpf_helpers.h>

#define bpf_map(name, _type, type_key, type_val, _max_entries)		\
struct bpf_map_def SEC("maps") name = {                         	\
        .type        = BPF_MAP_TYPE_##_type,                    	\
        .key_size    = sizeof(type_key),                        	\
        .value_size  = sizeof(type_val),                        	\
        .max_entries = _max_entries,                            	\
};                                                              	\
struct ____btf_map_##name {                                     	\
        type_key key;                                           	\
        type_val value;                                         	\
};                                                              	\
struct ____btf_map_##name						\
__attribute__((section(".btf.maps." #name), used))			\
 ____btf_map_##name = { 0, }	

#endif
