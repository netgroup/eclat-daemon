#
# ddos_tb_sd.eclat
#
# - token bucket monitor per ip6 (src,dst) -> black lists the (src,dst) out-profile
# for a time interval (e.g. 10 s) which is defined in ip6_hset.h: HIKE_IPV6_HSET_EXP_TIMEOUT_NS
# token bucket parameters (rate, bucket) are defined in tb_defs.h


#
# ddos_tb_sd_met.eclat
#
# - overall counter per ip6 (src,dst)
# - token bucket monitor per ip6 (src,dst) -> black lists the (src,dst) out-profile
# for a time interval (e.g. 10 s) which is defined in ip6_hset.h: HIKE_IPV6_HSET_EXP_TIMEOUT_NS
# token bucket parameters (rate, bucket) are defined in tb_defs.h



# ddos_tb_dst_met.eclat

- overall counter per ip6 dst
- token bucket monitor per ip6 dst -> black lists the (src,dst) whose dst is out-profile
- token bucket parameters (rate, bucket) are defined in tb_defs.h


#
# ddos_tb_d_met_drop.eclat
#
# - overall counter per ip6 dst
# - drop the Nth packet (on the same cpu) for a given destination 
# - token bucket monitor per ip6 dst -> black lists the (src,dst) whose dst is out-profile
# for a time interval (e.g. 10 s) which is defined in ip6_hset.h: HIKE_IPV6_HSET_EXP_TIMEOUT_NS
# token bucket parameters (rate, bucket) are defined in tb_defs.h


#
# ddos_tb_2_levels
#
# # token bucket monitor per ip6 dst 
# the out-profile packets are processed by a token bucket per src,dst
# -> black lists the (src,dst) out-profile
# for a time interval (e.g. 10 s) which is defined in ip6_hset.h: HIKE_IPV6_HSET_EXP_TIMEOUT_NS
# token bucket parameters (rate, bucket) are defined in tb_defs.h