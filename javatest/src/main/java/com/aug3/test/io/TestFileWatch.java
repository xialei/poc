package com.aug3.test.io;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardWatchEventKinds;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;
import java.util.List;

public class TestFileWatch {

	private WatchService watcher;

	private void TestWatcherService(Path dir) throws IOException {

		watcher = FileSystems.getDefault().newWatchService();
		dir.register(watcher, StandardWatchEventKinds.ENTRY_CREATE, StandardWatchEventKinds.ENTRY_DELETE,
				StandardWatchEventKinds.ENTRY_MODIFY);
	}

	private void handlerEvents() throws InterruptedException {

		while (true) {
			WatchKey key = watcher.take();
			List<WatchEvent<?>> events = key.pollEvents();
			for (WatchEvent<?> event : events) {
				WatchEvent.Kind<?> kind = event.kind();
				if (kind == StandardWatchEventKinds.OVERFLOW) {
					continue;
				}
				WatchEvent<Path> e = (WatchEvent<Path>) event;
				Path fileName = e.context();
				System.out.printf("Event %s happened, fileName is %s%n", kind.name(), fileName);
			}
			if (!key.reset()) {
				break;
			}
		}

	}

	public static void main(String args[]) throws IOException, InterruptedException {
		Path dir = Paths.get("D:\\hq");
		TestFileWatch w = new TestFileWatch();
		w.TestWatcherService(dir);
		w.handlerEvents();
	}

}
