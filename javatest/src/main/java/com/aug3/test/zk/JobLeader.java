package com.aug3.test.zk;

import java.io.Closeable;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.recipes.leader.LeaderSelector;
import org.apache.curator.framework.recipes.leader.LeaderSelectorListenerAdapter;

public class JobLeader extends LeaderSelectorListenerAdapter implements Closeable {

	private final String name;
	private final LeaderSelector leaderSelector;
	private final AtomicInteger leaderCount = new AtomicInteger();

	public JobLeader(CuratorFramework client, String path, String name) {
		this.name = name;
		leaderSelector = new LeaderSelector(client, path, this);
		leaderSelector.autoRequeue();
	}

	public void start() throws IOException {
		leaderSelector.start();
	}

	@Override
	public void takeLeadership(CuratorFramework client) throws Exception {
		final int waitSeconds = (int) (5 * Math.random()) + 1;
		System.out.println(name + " is now the leader. Waiting " + waitSeconds + " seconds...");
		System.out.println(name + " has been leader " + leaderCount.getAndIncrement()
				+ " time(s) before.");
		try {
			Thread.sleep(TimeUnit.SECONDS.toMillis(waitSeconds));
		} catch (InterruptedException e) {
			System.err.println(name + " was interrupted. error[" + e.getMessage() + "]");
			Thread.currentThread().interrupt();
		} finally {
			System.out.println(name + " relinquishing leadership.\n");
		}

	}

	@Override
	public void close() throws IOException {
		leaderSelector.close();
	}

}
