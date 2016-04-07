package com.aug3.test.zk;

import java.time.Instant;
import java.util.List;

import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.api.BackgroundCallback;
import org.apache.curator.framework.api.CuratorEvent;
import org.apache.curator.framework.api.CuratorListener;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.Watcher.Event.KeeperState;

import com.aug3.test.io.pb.ServicePoolProtos.ServiceInstance;
import com.aug3.test.io.pb.ServicePoolProtos.ServiceInstance.UriSpec;
import com.google.common.base.Charsets;

public class CuratorExample {

	public static CuratorFramework createWithOptions(String connectString, RetryPolicy retryPolicy,
			int connectionTimeoutMs, int sessionTimeoutMs, String namespace) {

		return CuratorFrameworkFactory.builder().connectString(connectString)
				.retryPolicy(retryPolicy).connectionTimeoutMs(connectionTimeoutMs)
				.sessionTimeoutMs(sessionTimeoutMs).namespace(namespace).build();

	}

	public static CuratorFramework createClient(String namespace) {

		// from configure
		String zkhost = "192.168.0.229:2181,192.168.0.230:2181,192.168.0.231:2181";

		RetryPolicy rp = new ExponentialBackoffRetry(1000, 3);// 重试机制

		CuratorFramework zkclient = createWithOptions(zkhost, rp, 5000, 5000, namespace);

		//zkclient.getCuratorListenable().addListener(new NodeEventListener());

		return zkclient;

	}

	public static void create(CuratorFramework client, String path, byte[] payload)
			throws Exception {

		client.create().creatingParentsIfNeeded().forPath(path, payload);

	}

	public static void create(CuratorFramework client, String nodeName, String value)
			throws Exception {

		client.create().creatingParentsIfNeeded().forPath(nodeName, value.getBytes(Charsets.UTF_8));

	}

	public static void createEphemeral(CuratorFramework client, String path, byte[] payload)
			throws Exception {

		client.create().withMode(CreateMode.EPHEMERAL).forPath(path, payload);

	}

	public static void setData(CuratorFramework client, String path, byte[] payload)
			throws Exception {

		client.setData().forPath(path, payload);

	}

	public static void setDataAsync(CuratorFramework client, String path, byte[] payload)
			throws Exception {

		CuratorListener listener = new CuratorListener() {

			@Override
			public void eventReceived(CuratorFramework client, CuratorEvent event) throws Exception {
				// examine event for details
			}

		};

		client.getCuratorListenable().addListener(listener);

		client.setData().inBackground().forPath(path, payload);

	}

	public static void setDataAsyncWithCallback(CuratorFramework client,
			BackgroundCallback callback, String path, byte[] payload) throws Exception {

		client.setData().inBackground(callback).forPath(path, payload);

	}

	public static void delete(CuratorFramework client, String path) throws Exception {
		client.delete().forPath(path);
	}

	// delete the given node and guarantee that it completes
	public static void guaranteedDelete(CuratorFramework client, String path) throws Exception {
		client.delete().guaranteed().deletingChildrenIfNeeded().forPath(path);
	}

	public static boolean checkExist(CuratorFramework client, String path) throws Exception {

		if (client.checkExists().forPath(path) == null) {
			return false;
		} else {
			return true;
		}

	}

	public static List<String> watchedGetChildren(CuratorFramework client, String path)
			throws Exception {

		// Get children and set a watcher on the node. The watcher notification
		// will come through the CuratorListener (see setDataAsync() above).
		return client.getChildren().watched().forPath(path);

	}

	public static List<String> watchedGetChildren(CuratorFramework client, String path,
			Watcher watcher) throws Exception {

		// Get children and set the given watcher on the node.
		return client.getChildren().usingWatcher(watcher).forPath(path);

	}

	public static void main(String[] args) {

		String namespace = "service_pool";
		CuratorFramework zkclient = createClient(namespace);
		zkclient.start();

		// zkclient.newNamespaceAwareEnsurePath(namespace);

		// crud
		ServiceInstance si = ServiceInstance
				.newBuilder()
				.setName("hqservice")
				.setId(1)
				.setTs(Instant.now().toEpochMilli())
				.addUri(UriSpec.newBuilder().setHost("192.168.0.86").setPort(8080)
						.setType(ServiceInstance.ProtocolType.HTTP)).build();

		try {
			create(zkclient, "/hqservice", "hqservice");
			create(zkclient, "/hqservice/node1", si.toByteArray());
			create(zkclient, "/hqservice/node2", si.toByteArray());

			List<String> children = watchedGetChildren(zkclient, "/hqservice", new Watcher() {
				@Override
				public void process(WatchedEvent event) {
					System.out.println("event:" + event.toString() + " state: "
							+ event.getState().name());
				}
			});

			for (String child : children) {
				System.out.println(child);
			}

			System.out.println(checkExist(zkclient, "/hqservice/node2"));

			guaranteedDelete(zkclient, "/hqservice/node2");

			System.out.println(checkExist(zkclient, "/hqservice/node2"));

			// guaranteedDelete(zkclient, "/hqservice/nodes");

		} catch (Exception e) {
			e.printStackTrace();
		}

		zkclient.close();

	}

}

// 监听器
final class NodeEventListener implements CuratorListener {
	@Override
	public void eventReceived(CuratorFramework client, CuratorEvent event) throws Exception {
		System.out.println(event.toString() + ".......................");
		final WatchedEvent watchedEvent = event.getWatchedEvent();
		if (watchedEvent != null) {
			System.out.println(watchedEvent.getState() + "======================="
					+ watchedEvent.getType());
			if (watchedEvent.getState() == KeeperState.SyncConnected) {
				switch (watchedEvent.getType()) {
				case NodeChildrenChanged:
					// TODO
					break;
				case NodeDataChanged:
					// TODO
					break;
				default:
					break;
				}
			}
		}
	}
}
