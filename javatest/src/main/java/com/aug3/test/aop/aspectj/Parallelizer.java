package com.aug3.test.aop.aspectj;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;

import com.aug3.test.aop.annotation.Parallel;

@Aspect
public final class Parallelizer {

	/**
	 * Execute method in multiple threads.
	 * 
	 * <p>
	 * This aspect should be used only on void returning methods.
	 * 
	 * <p>
	 * Try NOT to change the signature of this method, in order to keep it
	 * backward compatible.
	 * 
	 * @param point
	 *            Joint point
	 * @return The result of call
	 * @throws ParallelException
	 *             If something goes wrong inside
	 * @checkstyle IllegalThrowsCheck (4 lines)
	 */
	@Around("execution(@com.csf.test.aop.annotation.Parallel * * (..))")
	public Object wrap(final ProceedingJoinPoint point) throws ParallelException {
		final int total = ((MethodSignature) point.getSignature()).getMethod().getAnnotation(Parallel.class).threads();
		final Collection<Callable<Throwable>> callables = new ArrayList<Callable<Throwable>>(total);
		final CountDownLatch start = new CountDownLatch(1);
		for (int thread = 0; thread < total; ++thread) {
			callables.add(this.callable(point, start));
		}
		final ExecutorService executor = Executors.newFixedThreadPool(total);
		// final ExecutorService executor = Executors.newFixedThreadPool(total,
		// new VerboseThreads());
		final List<Future<Throwable>> futures = new ArrayList<Future<Throwable>>(total);
		for (Callable<Throwable> callable : callables) {
			futures.add(executor.submit(callable));
		}
		start.countDown();
		final Collection<Throwable> failures = new LinkedList<Throwable>();
		for (Future<Throwable> future : futures) {
			final Throwable exception;
			try {
				exception = future.get();
				if (exception != null) {
					failures.add(exception);
				}
			} catch (InterruptedException ex) {
				failures.add(ex);
			} catch (ExecutionException ex) {
				failures.add(ex);
			}
		}
		if (!failures.isEmpty()) {
			throw this.exceptions(failures);
		}
		return null;
	}

	/**
	 * Create parallel exception.
	 * 
	 * @param failures
	 *            List of exceptions from threads.
	 * @return Aggregated exceptions.
	 */
	private ParallelException exceptions(final Collection<Throwable> failures) {
		ParallelException current = null;
		for (Throwable failure : failures) {
			current = new ParallelException(failure, current);
		}
		return current;
	}

	/**
	 * Create callable that executes join point.
	 * 
	 * @param point
	 *            Join point to use.
	 * @param start
	 *            Latch to use.
	 * @return Created callable.
	 */
	private Callable<Throwable> callable(final ProceedingJoinPoint point, final CountDownLatch start) {
		return new Callable<Throwable>() {
			@Override
			public Throwable call() {
				Throwable result = null;
				try {
					start.await();
					point.proceed();
				} catch (Throwable ex) {
					result = ex;
				}
				return result;
			}
		};
	}

	/**
	 * Exception that encapsulates all exceptions thrown from threads.
	 */
	private static final class ParallelException extends Exception {
		/**
		 * Serialization marker.
		 */
		private static final long serialVersionUID = 0x8743ef363febc422L;
		/**
		 * Next parallel exception.
		 */
		private final transient ParallelException next;

		/**
		 * Constructor.
		 * 
		 * @param cause
		 *            Cause of the current exception.
		 * @param nxt
		 *            Following exception.
		 */
		protected ParallelException(final Throwable cause, final ParallelException nxt) {
			super(cause);
			this.next = nxt;
		}

		/**
		 * Get next parallel exception.
		 * 
		 * @return Next exception.
		 */
		public ParallelException getNext() {
			return this.next;
		}
	}

}
