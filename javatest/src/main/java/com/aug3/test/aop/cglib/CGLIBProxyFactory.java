package com.aug3.test.aop.cglib;

import com.aug3.test.aop.AOPInterceptor;

public interface CGLIBProxyFactory {

	<T> T createProxy(Class<T> clazz, AOPInterceptor interceptor);

}
