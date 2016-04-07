package com.aug3.test.consul;

import java.util.List;
import java.util.Map;

import com.google.common.net.HostAndPort;
import com.orbitz.consul.AgentClient;
import com.orbitz.consul.Consul;
import com.orbitz.consul.HealthClient;
import com.orbitz.consul.cache.ConsulCache;
import com.orbitz.consul.cache.ServiceHealthCache;
import com.orbitz.consul.model.health.ServiceHealth;

/**
 * consul > etcd > zookeeper
 * 
 * @author roger.xia
 *
 */
public class ConsulTest {

	public static void main(String[] args) throws Exception {

		Consul consul = Consul.builder().withUrl("http://192.168.0.228:8500").build();

		AgentClient agentClient = consul.agentClient();

		String serviceName = "hqservice";
		String serviceId = "1";

		agentClient.register(18080, 3L, serviceName, serviceId, "hqservice");

		agentClient.pass(serviceId);

		HealthClient healthClient = consul.healthClient();
		List<ServiceHealth> nodes = healthClient.getHealthyServiceInstances("hqservice")
				.getResponse();

		// Subscribe to healthy services
		ServiceHealthCache svHealth = ServiceHealthCache.newCache(healthClient, serviceName);

		svHealth.addListener(new ConsulCache.Listener<HostAndPort, ServiceHealth>() {
			@Override
			public void notify(Map<HostAndPort, ServiceHealth> newValues) {
				// do Something with updated server map
			}
		});
		svHealth.start();

	}

}
