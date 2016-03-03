package com.aug3.test.pattern.observer;

public class Main {

	public static void main(String[] args) {
		Zoo zoo = new Zoo();

		zoo.registerAnimalAddedListener(new PrintNameAnimalAddedListener());

		// 想添加一个计算动物园中动物总数的监听器，只需要新建一个具体的监听器类并注册到Zoo类即可，而无需对zoo类做任何修改。
		zoo.registerAnimalAddedListener(new CountingAnimalAddedListener());

		// lambda函数仅适用于监听器接口只有一个函数的情况, 如果接口有多个函数，可以选择使用匿名内部类。
		// 通过lambda函数或者匿名内部类注册的监听器不可以撤销注册，因为撤销函数需要传入已经注册监听器的引用。解决这个问题的一个简单方法是在registerAnimalAddedListener函数中返回注册监听器的引用。
		AnimalAddedListener listener = zoo.registerAnimalAddedListener((animal) -> System.out
				.println("Welcome animal " + animal.getName()));

		Animal tiger = new Animal("Tiger");
		zoo.addAnimal(tiger);
		zoo.addAnimal(new Animal("Lion"));
		zoo.unregisterAnimalAddedListener(listener);

		zoo.addAnimal(new Animal("Bear"));

	}

}
