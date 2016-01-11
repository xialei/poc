package com.aug3.test.aop.guice;

import com.google.inject.AbstractModule;
import com.google.inject.matcher.Matchers;

public class InterceptorModule extends AbstractModule {

	@Override
	protected void configure() {

		bindInterceptor(Matchers.any(), Matchers.annotatedWith(TimeLog.class), new TimeLogInterceptor());
	}

}
