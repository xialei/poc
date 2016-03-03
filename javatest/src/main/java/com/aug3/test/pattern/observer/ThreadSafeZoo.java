package com.aug3.test.pattern.observer;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * 观察者模式的线程安全主要集中在模式的主体上，因为修改注册监听器集合时很可能发生线程冲突，比如，一个线程试图添加一个新的监听器，
 * 而另一线程又试图添加一个新的animal对象，这将触发对所有注册监听器的通知。
 * 
 * 最简单的解决方案是：所有访问或修改注册监听器list的操作都须遵循Java的同步机制
 * 
 * 通过方法同步，可以时刻观测对监听器list的并发访问，注册和撤销监听器对监听器list而言是写操作，而通知监听器访问监听器list是只读操作。
 * 由于通过通知访问是读操作，因此是可以多个通知操作同时进行的。
 * 
 * @author roger.xia
 *
 */
public class ThreadSafeZoo {

	private final ReadWriteLock readWriteLock = new ReentrantReadWriteLock();

	protected final Lock readLock = readWriteLock.readLock();
	protected final Lock writeLock = readWriteLock.writeLock();

	private List<Animal> animals = new ArrayList<>();

	private List<AnimalAddedListener> listeners = new ArrayList<>();

	protected void notifyAnimalAddedListeners(Animal animal) {
		this.readLock.lock();
		try {
			this.listeners.forEach(listener -> listener.onAnimalAdded(animal));
		} finally {
			this.readLock.unlock();
		}
	}

	public AnimalAddedListener registerAnimalAddedListener(AnimalAddedListener listener) {
		// Lock the list of listeners for writing
		this.writeLock.lock();
		try {
			this.listeners.add(listener);
		} finally {
			this.writeLock.unlock();
		}
		return listener;
	}

	public void unregisterAnimalAddedListener(AnimalAddedListener listener) {
		this.writeLock.lock();
		try {
			this.listeners.remove(listener);
		} finally {
			this.writeLock.unlock();
		}
	}

	public void addAnimal(Animal animal) {
		this.animals.add(animal);
		this.notifyAnimalAddedListeners(animal);

	}

}
