package com.aug3.test.aop;


public class PersistenceServiceImpl implements PersistenceService {

	//@TransactionAnnotation("REQUIRES_NEW")
	public void save(long id, String data) {

	}

	//@TransactionAnnotation("NOT_SUPPORTED")
	public String load(long id) {
		return null;
	}

}
