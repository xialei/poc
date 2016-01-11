package com.aug3.test.thread;

import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class Calculator {
	private int calculatedValue;
	private int value;
	private ReadWriteLock lock = new ReentrantReadWriteLock();

	public void calculate(int value) {
		lock.writeLock().lock();
		try {
			this.value = value;
			this.calculatedValue = doMySlowCalculation(value);
		} finally {
			lock.writeLock().unlock();
		}
	}

	public int getCalculatedValue() {
		lock.readLock().lock();
		try {
			return calculatedValue;
		} finally {
			lock.readLock().unlock();
		}
	}

	public int getValue() {
		lock.readLock().lock();
		try {
			return value;
		} finally {
			lock.readLock().unlock();
		}
	}

	private int doMySlowCalculation(int value) {

		return 0;
	}
}
