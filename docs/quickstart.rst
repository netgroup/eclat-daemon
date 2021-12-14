Quick Start
===========

Working with offline and preinstalled doker image, on LINUX

#. Download the docker image eclat.tar.gz

#. Load the image: ``docker load < eclat.tar.gz``

#. Create and execute container: ``docker run --rm -t -i --privileged --name eclat eclat:testbed  /sbin/my_init -- bash -l``

#. Inside the container: ``cd /opt/eclat-daemon && bash testbed/ddos_double_token_bucket_with_sampler.sh``

A tmux will start, implementing the topology depicted below.
There are three namespaces:

* SUT (System Under Test)
* TG (Traffic Generator)
* COLLECTOR

The SUT is the namespace in which we run the eCLAT daemon and the HIKe VM is attached to the XDP hook on the incoming interface enp6s0f0. The TG is the namespace in which we generate traffic to be processed by our HIKe / eCLAT framework. The COLLECTOR namespace is used in some examples in which we redirect some incoming packets to the outgoing interface cl0 of the SUT.

::

   #      +------------------+      +------------------+
   #      |        TG        |      |       SUT        |
   #      |                  |      |                  |
   #      |         enp6s0f0 +------+ enp6s0f0 <--- HIKe VM XDP loader
   #      |                  |      |                  |
   #      |                  |      |                  |
   #      |         enp6s0f1 +------+ enp6s0f1         |
   #      |                  |      |         + cl0  <-|- towards the collector
   #      +------------------+      +---------|--------+
   #                                          |
   #                                +---------|------+
   #                                |         + veth0|
   #                                |                |
   #                                |    COLLECTOR   |
   #                                +----------------+

There are 7 windows in the TMUX, click with the mouse on the window name in the status bar to activate them.

In window TG1 and TG2 you can run the ping commands to generate traffic.
On TG1 the command ``ping -i 0.01 fc01::2`` which sends 100 p/s is displayed and ready to be executed.
On TG2 the command ``ping -i 0.5 fc01::3`` which sends 2 p/s is displayed and ready to be executed.

In window MAPS you can see the content of the eBPF maps.

In window CLT we have run the ``tcpdump -i veth0`` command to display the packets that are redirected to the collector.

To perform an experirent first run the 2 p/s ping ``ping -i 0.5 fc01::3`` on TG2. Go in MAPS window and can see that the flow with destination fc01::3 is monitored in the per destination token bucket and it remains IN_PROFILE. The packet monitor (map ``map_pcpu_mon``) counts the transmitted packets (code 0). 

Then add the 100 p/s ping ``ping -i 0.01 fc01::2`` on TG1. You will notice that after few seconds the ping are not replied, because the (src, dst) flow has been blacklisted (for 10 seconds). After 10 seconds the flow is removed from the blacklist and some ping replies are again received. Looking in the MAPS windows, you can see that token bucket per (src, dst) has been activated and that the packet monitor (map ``map_pcpu_mon``) shows many dropped packets (code 1). One packet every 500 packets is shown as redirected (code 2). You can check on the CLT window that the redirected packet has been captured by tcpdump.
