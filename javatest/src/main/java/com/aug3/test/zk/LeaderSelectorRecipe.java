package com.aug3.test.zk;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.utils.CloseableUtils;

import com.google.common.collect.Lists;

public class LeaderSelectorRecipe {

	private static final int CLIENT_QTY = 10;
	private static final String PATH = "/examples/leader";

	public static void main(String[] args) throws Exception {
		testConcurrent();
	}

	public static void testSeq() throws Exception {
		List<CuratorFramework> clients = Lists.newArrayList();
		List<JobLeader> examples = Lists.newArrayList();
		// TestingServer server = new TestingServer();
		try {
			for (int i = 0; i < CLIENT_QTY; ++i) {
				CuratorFramework client = CuratorExample.createClient("service_pool");
				clients.add(client);
				JobLeader example = new JobLeader(client, PATH, "Client #" + i);
				examples.add(example);
				client.start();
				example.start();
			}

			System.out.println("Press enter/return to quit\n");
			new BufferedReader(new InputStreamReader(System.in)).readLine();
		} finally {
			System.out.println("Shutting down...");
			for (JobLeader JobLeader : examples) {
				CloseableUtils.closeQuietly(JobLeader);
			}
			for (CuratorFramework client : clients) {
				CloseableUtils.closeQuietly(client);
			}
			// CloseableUtils.closeQuietly(server);
		}
	}

	public static void testConcurrent() throws Exception {

		ExecutorService executors = Executors.newCachedThreadPool();
		for (int i = 0; i < CLIENT_QTY; i++) {

			final int num = i;
			Runnable r = () -> {
				CuratorFramework client = CuratorExample.createClient("service_pool");
				JobLeader job = new JobLeader(client, PATH, "Client #" + num);
				client.start();
				try {
					job.start();
					Thread.sleep(10000);
				} catch (Exception e) {
				} finally {
					CloseableUtils.closeQuietly(job);
					CloseableUtils.closeQuietly(client);
				}
			};

			executors.execute(r);

		}
	}

}
