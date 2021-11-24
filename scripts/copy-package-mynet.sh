#!/bin/bash

PACKAGE_NAME=mynet

SOURCE_DIR=hike_v3/src
TARGET_DIR=components/programs 

#cp $SOURCE_DIR/allow_any.bpf.c $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/hike_drop.bpf.c            $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/hike_pass.bpf.c            $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_hset_srcdst.bpf.c      $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_dst_meter.bpf.c        $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_dst_tbmon.bpf.c        $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_sd_meter.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_sd_meter.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_sd_tbmon.bpf.c         $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/lse.bpf.c                  $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/monitor.bpf.c              $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/ip6_hset.h                 $TARGET_DIR/$PACKAGE_NAME
cp $SOURCE_DIR/tb_defs.h                  $TARGET_DIR/$PACKAGE_NAME

