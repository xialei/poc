package com.aug3.test.aop;

import com.aug3.test.aop.annotation.TransactionAnnotation;

public interface PersistenceService {
	@TransactionAnnotation("REQUIRES_NEW")
	void save(long id, String data);

	@TransactionAnnotation("NOT_SUPPORTED")
	String load(long id);
}
