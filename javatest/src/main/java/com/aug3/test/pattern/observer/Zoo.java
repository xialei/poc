package com.aug3.test.pattern.observer;

import java.util.ArrayList;
import java.util.List;

public class Zoo {

	private List<Animal> animals = new ArrayList<>();

	private List<AnimalAddedListener> listeners = new ArrayList<>();

	protected void notifyAnimalAddedListeners(Animal animal) {
		this.listeners.forEach(listener -> listener.onAnimalAdded(animal));
	}

	public AnimalAddedListener registerAnimalAddedListener(AnimalAddedListener listener) {
		this.listeners.add(listener);
		return listener;
	}

	public void unregisterAnimalAddedListener(AnimalAddedListener listener) {
		this.listeners.remove(listener);
	}

	public void addAnimal(Animal animal) {
		this.animals.add(animal);
		this.notifyAnimalAddedListeners(animal);

	}

}
