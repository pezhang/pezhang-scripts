queues=2
cores=8
/root/dpdk/install/bin/testpmd \
-l 0,2,4,6,8,10,12,14,16 \
--socket-mem=1024 \
-n 4 \
--vdev net_vhost0,iface=/tmp/vhost-user1,queues=${queues} \
--vdev net_vhost1,iface=/tmp/vhost-user2,queues=${queues} -- \
--portmask=f \
--disable-hw-vlan \
-i \
--rxq=${queues} --txq=${queues} \
--nb-cores=${cores} \
--forward-mode=io \

