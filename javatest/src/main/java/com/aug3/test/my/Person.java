package com.aug3.test.my;

import java.util.ArrayList;
import java.util.List;

public class Person {
	private String givenName;
	private String surName;
	private int age;
	private String eMail;
	private String phone;
	private String address;

	public static List<Person> createShortList() {
		List<Person> list = new ArrayList<>();
		Person p = new Person();
		p.setGivenName("Roger");
		p.setSurName("Xia");
		p.setAge(28);
		p.seteMail("roger@mail.com");
		p.setPhone("13898888888");
		p.setAddress("Shanghai China");
		list.add(p);

		Person p1 = new Person();
		p1.setGivenName("Edward");
		p1.setSurName("Yang");
		p1.setAge(28);
		p1.seteMail("edward@gmail.com");
		p1.setPhone("13798888888");
		p1.setAddress("Shanghai China");
		list.add(p1);

		Person p2 = new Person();
		p2.setGivenName("Yi");
		p2.setSurName("Yun");
		p2.setAge(28);
		p2.seteMail("yi@gmail.com");
		p2.setPhone("13698888888");
		p2.setAddress("Shanghai China");
		list.add(p2);

		return list;
	}

	public void printName() {
		System.out.println(getGivenName() + " " + getSurName());
	}

	public String getGivenName() {
		return givenName;
	}

	public void setGivenName(String givenName) {
		this.givenName = givenName;
	}

	public String getSurName() {
		return surName;
	}

	public void setSurName(String surName) {
		this.surName = surName;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String geteMail() {
		return eMail;
	}

	public void seteMail(String eMail) {
		this.eMail = eMail;
	}

	public String getPhone() {
		return phone;
	}

	public void setPhone(String phone) {
		this.phone = phone;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

}
