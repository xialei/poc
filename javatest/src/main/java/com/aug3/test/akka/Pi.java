package com.aug3.test.akka;

import scala.concurrent.duration.Duration;
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.actor.UntypedActorFactory;

/**
 * The design we are aiming for is to have one Master actor initiating the
 * computation, creating a set of Worker actors. Then it splits up the work into
 * discrete chunks, and sends these chunks to the different workers in a
 * round-robin fashion. The master waits until all the workers have completed
 * their work and sent back results for aggregation. When computation is
 * completed the master sends the result to the Listener, which prints out the
 * result.
 * 
 * Messages sent to actors should always be immutable to avoid sharing mutable
 * state.
 * 
 * Calculate – sent to the Master actor to start the calculation
 * 
 * Work – sent from the Master actor to the Worker actors containing the work
 * assignment
 * 
 * Result – sent from the Worker actors to the Master actor containing the
 * result from the worker’s calculation
 * 
 * PiApproximation – sent from the Master actor to the Listener actor containing
 * the the final pi result and how long time the calculation took
 * 
 * 
 */
public class Pi {

	static class Calculate {
	}

	static class Work {
		private final int start;
		private final int nrOfElements;

		public Work(int start, int nrOfElements) {
			this.start = start;
			this.nrOfElements = nrOfElements;
		}

		public int getStart() {
			return start;
		}

		public int getNrOfElements() {
			return nrOfElements;
		}
	}

	static class Result {
		private final double value;

		public Result(double value) {
			this.value = value;
		}

		public double getValue() {
			return value;
		}
	}

	static class PiApproximation {
		private final double pi;
		private final Duration duration;

		public PiApproximation(double pi, Duration duration) {
			this.pi = pi;
			this.duration = duration;
		}

		public double getPi() {
			return pi;
		}

		public Duration getDuration() {
			return duration;
		}
	}

	public static void main(String[] args) {
		Pi pi = new Pi();
		pi.calculate(4, 10000, 10000);
	}

	public void calculate(final int nrOfWorkers, final int nrOfElements, final int nrOfMessages) {
		// Create an Akka system, which will contain all actors created in that “context”
		ActorSystem system = ActorSystem.create("PiSystem");

		// create the result listener, which will print the result and shutdown
		// the system
		final ActorRef listener = system.actorOf(Props.create(Listener.class), "listener");

		// create the master
		ActorRef master = system.actorOf(Props.create(new UntypedActorFactory() {
			public UntypedActor create() {
				return new Master(nrOfWorkers, nrOfMessages, nrOfElements, listener);
			}
		}), "master");

		// start the calculation
		//master.tell(new Calculate());

	}

}
