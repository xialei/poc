package com.aug3.test.pattern.observer;

import java.util.concurrent.atomic.AtomicLong;

/**
 * 并发访问监听器可以通过保证监听器的线程安全来实现。秉承着类的“责任自负”精神，监听器有“义务”确保自身的线程安全。例如，对于前面计数的监听器，
 * 多线程的递增或递减动物数量可能导致线程安全问题，要避免这一问题，动物数的计算必须是原子操作（原子变量或方法同步）
 * 
 * @author roger.xia
 *
 */
public class ThreadSafeCountingAnimalAddedListener implements AnimalAddedListener {

	private static AtomicLong animalsAddedCount = new AtomicLong(0);

	@Override
	public void onAnimalAdded(Animal animal) {
		animalsAddedCount.incrementAndGet();
		System.out.println(animalsAddedCount);

	}

}
