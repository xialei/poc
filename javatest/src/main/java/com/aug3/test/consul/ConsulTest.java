package com.aug3.test.consul;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import javax.ws.rs.client.ClientBuilder;

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

		Consul consul = Consul.builder().build();

		AgentClient agentClient = consul.agentClient();

		String serviceName = "hqservice";
		String serviceId = UUID.randomUUID().toString();

		// 1. register service
		agentClient.register(18080, 20L, serviceName, serviceId);

		agentClient.pass(serviceId); // check in with consul

		// 2. find available services
		HealthClient healthClient = consul.healthClient();
		List<ServiceHealth> nodes = healthClient.getHealthyServiceInstances(serviceName)
				.getResponse();

		// 3. Subscribe to healthy services
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
