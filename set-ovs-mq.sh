queues=2
ovs-vsctl set Open_vSwitch . other_config={} 
ovs-vsctl set Open_vSwitch . other_config:n-dpdk-rxqs=${queues}
ovs-vsctl set Open_vSwitch . other_config:dpdk-lcore-mask=0x1

# for queues=1, using cores 2,4,6,8
#ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0x154

# for queues=2, using cores 2,4,6,8,10,12,14,16
ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0x15554

ovs-vsctl set Interface dpdk0 options:n_rxq=${queues}
ovs-vsctl set Interface dpdk1 options:n_rxq=${queues}
ovs-vsctl set Interface vhost-user1 options:n_rxq=${queues}
ovs-vsctl set Interface vhost-user2 options:n_rxq=${queues}
ovs-vsctl set Interface dpdk0 options:n_txq=${queues}
ovs-vsctl set Interface dpdk1 options:n_txq=${queues}
ovs-vsctl set Interface vhost-user1 options:n_txq=${queues}
ovs-vsctl set Interface vhost-user2 options:n_txq=${queues}
