package com.aug3.test.redis;

import java.util.HashSet;
import java.util.Set;

import redis.clients.jedis.HostAndPort;
import redis.clients.jedis.JedisCluster;

public class ClusterDemo {

	public static void main(String args[]) {
		Set<HostAndPort> jedisClusterNodes = new HashSet<HostAndPort>();
		// Jedis Cluster will attempt to discover cluster nodes automatically
		jedisClusterNodes.add(new HostAndPort("192.168.0.229", 6379));
		jedisClusterNodes.add(new HostAndPort("192.168.0.230", 6379));
		jedisClusterNodes.add(new HostAndPort("192.168.0.231", 6379));
		JedisCluster jc = new JedisCluster(jedisClusterNodes);
		jc.set("name", "roger.xia");
		String value = jc.get("name");
		System.out.println(value);
		jc.close();
	}

}
