### Multipurpose tool for discovering and collecting metrics from Cloudera Manager Hadoop clusters.

####Usage
TBD.

####Examples
Current Options:
```
usage: clouderasizer.py [-h] [--username USERNAME] [--password PASSWORD]
                        [--cm_host CM_HOST] [--config_file CONFIG_FILE]
                        {metrics,collect,tsql} ...

positional arguments:
  {metrics,collect,tsql}
    metrics             Find and describe available metrics
    collect             Collect metrics
    tsql                Build a TSQL query for running your own API calls

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   Name of an user with administrative access (defaults
                        to admin)
  --password PASSWORD   Password for the administrative user (defaults to
                        admin)
  --cm_host CM_HOST     The hostname/ip of the Cloudera Manager server
  --config_file CONFIG_FILE
                        Cluster configuration file (.ini)
```

Find available metrics based on search terms. Below I'm looking for metrics related to all 3 of "memory, host, and total":
```
python clouderasizer.py metrics --search memory host total


Metric Name: total_agent_physical_memory_used_across_hosts
Display Name: Total Agent Physical Memory Across Hosts
Description: The sum of the Agent Physical Memory metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_cached_across_hosts
Display Name: Total Physical Memory Caches Across Hosts
Description: The sum of the Physical Memory Caches metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_jvm_heap_committed_mb_across_hostmonitors
Display Name: Total Committed Heap Memory Across Host Monitors
Description: The sum of the Committed Heap Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: megabytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_jvm_max_memory_mb_across_hostmonitors
Display Name: Total Max Memory Across Host Monitors
Description: The sum of the Max Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: megabytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_mapped_across_hosts
Display Name: Total Physical Memory Mapped Across Hosts
Description: The sum of the Physical Memory Mapped metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_dirty_across_hosts
Display Name: Total Physical Memory Dirty Across Hosts
Description: The sum of the Physical Memory Dirty metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_oom_exits_rate_across_hostmonitors
Display Name: Total Out of Memory Exits Across Host Monitors
Description: The sum of the Out of Memory Exits metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: exits
Unit Denominator: seconds
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_mem_swap_across_hostmonitors
Display Name: Total Swap Memory Usage Across Host Monitors
Description: The sum of the Swap Memory Usage metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_writeback_across_hosts
Display Name: Total Physical Memory Writeback Across Hosts
Description: The sum of the Physical Memory Writeback metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_used_across_hosts
Display Name: Total Physical Memory Used Across Hosts
Description: The sum of the Physical Memory Used metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_mem_rss_across_hostmonitors
Display Name: Total Resident Memory Across Host Monitors
Description: The sum of the Resident Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_buffers_across_hosts
Display Name: Total Physical Memory Buffers Across Hosts
Description: The sum of the Physical Memory Buffers metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_cgroup_mem_page_cache_across_hostmonitors
Display Name: Total CGroup Page Cache Memory Across Host Monitors
Description: The sum of the CGroup Page Cache Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_jvm_non_heap_committed_mb_across_hostmonitors
Display Name: Total Committed Non-Heap Memory Across Host Monitors
Description: The sum of the Committed Non-Heap Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: megabytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_jvm_non_heap_used_mb_across_hostmonitors
Display Name: Total Used Non-Heap Memory Across Host Monitors
Description: The sum of the Used Non-Heap Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: megabytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_supervisord_physical_memory_used_across_hosts
Display Name: Total Supervisord Physical Memory Across Hosts
Description: The sum of the Supervisord Physical Memory metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_cgroup_mem_rss_across_hostmonitors
Display Name: Total CGroup Resident Memory Across Host Monitors
Description: The sum of the CGroup Resident Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_jvm_heap_used_mb_across_hostmonitors
Display Name: Total Used Heap Memory Across Host Monitors
Description: The sum of the Used Heap Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: megabytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_dirty_ratio_across_hosts
Display Name: Total Physical Memory Dirty Ratio Across Hosts
Description: The sum of the Physical Memory Dirty Ratio metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: percent
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_supervisord_virtual_memory_used_across_hosts
Display Name: Total Supervisord Virtual Memory Across Hosts
Description: The sum of the Supervisord Virtual Memory metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_agent_virtual_memory_used_across_hosts
Display Name: Total Agent Virtual Memory Across Hosts
Description: The sum of the Agent Virtual Memory metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_mem_virtual_across_hostmonitors
Display Name: Total Virtual Memory Across Host Monitors
Description: The sum of the Virtual Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_total_across_hosts
Display Name: Total Physical Memory Capacity Across Hosts
Description: The sum of the Physical Memory Capacity metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_physical_memory_memfree_across_hosts
Display Name: Total Physical Memory Free Across Hosts
Description: The sum of the Physical Memory Free metric computed across all this entity's descendant Host entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'CLUSTER': [u'enterprise'], u'RACK': [u'enterprise']}
____________________________________________

Metric Name: total_cgroup_mem_swap_across_hostmonitors
Display Name: Total CGroup Swap Cache Memory Across Host Monitors
Description: The sum of the CGroup Swap Cache Memory metric computed across all this entity's descendant Host Monitor entities.
Is Counter: False
Unit Numerator: bytes
Unit Denominator: None
Aliases: []
Sources: {u'RACK': [u'enterprise'], u'MGMT': [u'enterprise']}
____________________________________________
```
