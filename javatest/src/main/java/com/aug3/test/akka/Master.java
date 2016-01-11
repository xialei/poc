package com.aug3.test.akka;

import java.util.concurrent.TimeUnit;

import scala.concurrent.duration.Duration;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.routing.RoundRobinRouter;

import com.aug3.test.akka.Pi.Calculate;
import com.aug3.test.akka.Pi.PiApproximation;
import com.aug3.test.akka.Pi.Result;
import com.aug3.test.akka.Pi.Work;

public class Master extends UntypedActor {

	private final int nrOfMessages;
	private final int nrOfElements;

	private double pi;
	private int nrOfResults;
	private final long start = System.currentTimeMillis();

	private final ActorRef listener;
	private final ActorRef workerRouter;

	/**
	 * 
	 * @param nrOfWorkers
	 *            defining how many workers we should start up
	 * @param nrOfMessages
	 *            defining how many number chunks to send out to the workers
	 * @param nrOfElements
	 *            defining how big the number chunks sent to each worker should
	 *            be
	 * @param listener
	 */
	public Master(final int nrOfWorkers, int nrOfMessages, int nrOfElements, ActorRef listener) {
		this.nrOfMessages = nrOfMessages;
		this.nrOfElements = nrOfElements;
		this.listener = listener;

		workerRouter = this.getContext().actorOf(
				Props.create(Worker.class).withRouter(new RoundRobinRouter(nrOfWorkers)), "workerRouter");
	}

	@Override
	public void onReceive(Object message) throws Exception {
		// handle messages ...
		if (message instanceof Calculate) {
			for (int start = 0; start < nrOfMessages; start++) {
				workerRouter.tell(new Work(start, nrOfElements), getSelf());
			}
		} else if (message instanceof Result) {
			Result result = (Result) message;
			pi += result.getValue();
			nrOfResults += 1;
			if (nrOfResults == nrOfMessages) {
				// Send the result to the listener
				Duration duration = Duration.create(System.currentTimeMillis() - start, TimeUnit.MILLISECONDS);
				listener.tell(new PiApproximation(pi, duration), getSelf());
				// Stops this actor and all its supervised children
				getContext().stop(getSelf());
			}
		} else {
			unhandled(message);
		}
	}

}
