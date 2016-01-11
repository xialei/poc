package com.aug3.test.thread.fork;

import java.util.Arrays;

public class BinarySearchProblem {

	private final int[] numbers;
	private final int start;
	private final int end;
	public final int size;

	public BinarySearchProblem(int[] numbers, int start, int end) {
		this.numbers = numbers;
		this.start = start;
		this.end = end;
		this.size = end - start;
	}

	public int searchSequentially(int numberToSearch) {
		// 偷懒，不自己写二分查找了
		return Arrays.binarySearch(numbers, start, end, numberToSearch);
	}

	public BinarySearchProblem subProblem(int subStart, int subEnd) {
		return new BinarySearchProblem(numbers, start + subStart, start + subEnd);
	}

}
