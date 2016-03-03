package com.aug3.test.pattern.observer;

public class CountingAnimalAddedListener implements AnimalAddedListener {

	private static int animalAddedCount = 0;

	@Override
	public void onAnimalAdded(Animal animal) {
		animalAddedCount++;
		System.out.println("Total animals added: " + animalAddedCount);

	}

}
