package com.aug3.test.aop.annotation;

import java.lang.reflect.Method;

import com.aug3.test.aop.AOPInterceptor;

public class TransactionInterceptor implements AOPInterceptor {
	private Transaction transaction;

	public void before(Method method, Object[] args) {
		if (isRequiresNew(method)) {
			transaction = new TransactionAdapter();
			transaction.open();
		}
	}

	public void after(Method method, Object[] args) {
		if (transaction != null) {
			transaction.commit();
		}
	}

	public void afterThrowing(Method method, Object[] args, Throwable t) {
		if (transaction != null) {
			transaction.rollBack();
		}
	}

	public void afterFinally(Method method, Object[] args) {
		if (transaction != null) {
			transaction.closeIfStillOpen();
			transaction = null;
		}
	}

	protected boolean isRequiresNew(Method method) {
		TransactionAnnotation transactionAnnotation = method.getAnnotation(TransactionAnnotation.class);

		if (transactionAnnotation != null) {
			if ("REQUIRES_NEW".equals(transactionAnnotation.value())) {
				return true;
			}
		}

		return false;
	}
}