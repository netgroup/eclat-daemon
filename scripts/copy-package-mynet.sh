#!/bin/bash

PACKAGE_NAME=mynet

SOURCE_DIR=hike_v3/src
SOURCE_CONTRIB=hike_v3/contrib-src
TARGET_DIR=components/programs 

#cp $SOURCE_DIR/allow_any.bpf.c           $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/l2_redirect.bpf.c          $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/hike_drop.bpf.c            $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/hike_pass.bpf.c            $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_hset_srcdst.bpf.c      $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/lse.bpf.c                  $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/monitor.bpf.c              $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_hset.h                 $TARGET_DIR/$PACKAGE_NAME

cp $SOURCE_CONTRIB/ip6_dst_meter.bpf.c        $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/ip6_dst_tbmon.bpf.c        $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/ip6_sd_meter.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/ip6_sd_tbmon.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/ip6_sd_dec2zero.bpf.c      $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/ip6_alt_mark.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/tb_defs.h                  $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_CONTRIB/udp_port.bpf.c             $TARGET_DIR/$PACKAGE_NAME

