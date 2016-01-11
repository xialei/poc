package com.aug3.test.thread.fork;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class BiSearchWithForkJoin extends RecursiveAction {

	private final int threshold;
	private final BinarySearchProblem problem;
	public int result;
	private final int numberToSearch;

	public BiSearchWithForkJoin(BinarySearchProblem problem, int threshold, int numberToSearch) {
		this.problem = problem;
		this.threshold = threshold;
		this.numberToSearch = numberToSearch;
	}

	@Override
	protected void compute() {
		if (problem.size < threshold) { // 小于阀值，就直接用普通的二分查找
			result = problem.searchSequentially(numberToSearch);
		} else {
			// 分解子任务
			int midPoint = problem.size / 2;
			BiSearchWithForkJoin left = new BiSearchWithForkJoin(problem.subProblem(0, midPoint), threshold,
					numberToSearch);
			BiSearchWithForkJoin right = new BiSearchWithForkJoin(problem.subProblem(midPoint + 1, problem.size),
					threshold, numberToSearch);
			invokeAll(left, right);
			result = Math.max(left.result, right.result);
		}
	}

	// 构造数据
	private static final int[] data = new int[1000_0000];
	static {
		for (int i = 0; i < 1000_0000; i++) {
			data[i] = i;
		}
	}

	public static void main(String[] args) {
		BinarySearchProblem problem = new BinarySearchProblem(data, 0, data.length);
		int threshold = 100;
		int nThreads = 10;
		// 查找100_0000所在的下标
		BiSearchWithForkJoin bswfj = new BiSearchWithForkJoin(problem, threshold, 100_0000);
		ForkJoinPool fjPool = new ForkJoinPool(nThreads);
		fjPool.invoke(bswfj);
		System.out.printf("Result is:%d%n", bswfj.result);
	}

}
