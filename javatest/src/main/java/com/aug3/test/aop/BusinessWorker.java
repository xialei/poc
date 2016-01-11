package com.aug3.test.aop;

import com.aug3.test.aop.annotation.Parallel;

public class BusinessWorker {

	@Parallel(threads = 3)
	public void doBusinessWork() {
		System.out.println("do business!");
	}

}
