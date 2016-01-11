package com.aug3.test.thread;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class TaskRunner {
	private Map<Class<? extends Runnable>, Lock> mLocks = new HashMap<Class<? extends Runnable>, Lock>();

	public void runTaskUniquely(Runnable r, int secondsToWait) {
		Lock lock = getLock(r.getClass());
		try {
			boolean acquired = lock.tryLock(secondsToWait, TimeUnit.SECONDS);
			if (acquired) {

				r.run();

			} else {
				// failure code here
			}
		} catch (Exception e) {
			
		} finally {
			lock.unlock();
		}
	}

	private synchronized Lock getLock(Class clazz) {
		Lock l = mLocks.get(clazz);
		if (l == null) {
			l = new ReentrantLock();
			mLocks.put(clazz, l);
		}
		return l;
	}
}