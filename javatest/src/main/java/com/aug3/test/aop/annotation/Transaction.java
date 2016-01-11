package com.aug3.test.aop.annotation;

public interface Transaction {
	void open();

	void rollBack();

	void commit();

	void closeIfStillOpen();
}
