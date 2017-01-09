package com.aug3.test.my;

import static java.util.Comparator.comparing;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.mapping;
import static java.util.stream.Collectors.toList;

import java.time.Clock;
import java.time.DateTimeException;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;
import java.time.MonthDay;
import java.time.OffsetDateTime;
import java.time.Period;
import java.time.YearMonth;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.function.Predicate;
import java.util.stream.IntStream;

import org.apache.commons.lang.StringUtils;

public class TestJDK8 {

	private static void testRunnable() {
		System.out.println("=== runnableLambda ===");

		// Anonymous Runnable
		Runnable r1 = new Runnable() {
			@Override
			public void run() {
				System.out.println("Hello world one!");
			}
		};

		// Lambda Runnable
		Runnable r2 = () -> System.out.println("Hello world two!");

		// Run em!
		r1.run();
		r2.run();
	}

	private static void testListFilter() {

		System.out.println("=== filter ===");

		List<String> names = Arrays.asList("Alan", "Ada", "Jim", "Roger", "Who else");
		List<String> filterNames = Arrays
				.asList(names.stream().filter(name -> name.startsWith("A")).toArray(String[]::new));

		filterNames.forEach(elem -> System.out.println(elem));

	}

	public static void printSorted(List<Person> people, Comparator<Person> comparator) {
		people.stream().sorted(comparator).forEach(System.out::println);
	}

	private static void testComparator() {

		List<Person> personList = Person.createShortList();

		// Sort with Inner Class
		Collections.sort(personList, new Comparator<Person>() {
			public int compare(Person p1, Person p2) {
				return p1.getSurName().compareTo(p2.getSurName());
			}
		});

		for (Person p : personList) {
			p.printName();
		}

		// Use Lambda instead
		Collections.sort(personList, (Person p1, Person p2) -> p1.getSurName().compareTo(p2.getSurName()));

		for (Person p : personList) {
			p.printName();
		}

		// Print Desc
		System.out.println("=== Sorted Desc SurName ===");
		Collections.sort(personList, (p1, p2) -> p2.getSurName().compareTo(p1.getSurName()));

		for (Person p : personList) {
			p.printName();
		}

		System.out.println("=== comparing SurName ===");
		printSorted(personList, comparing(Person::getSurName));

		System.out.println("=== comparing age ===");
		printSorted(personList, comparing(Person::getAge).thenComparing(Person::getGivenName).reversed());

		System.out.println("=== group by age ===");
		System.out.println(personList.stream().collect(groupingBy(Person::getAge)));

		System.out.println(
				personList.stream().collect(groupingBy(Person::getAge, mapping(Person::getGivenName, toList()))));
	}

	/**
	 * 使用JavaStream并行处理和Lambda闭包函数的特性来计算证券投资中资产组合的信用风险
	 * 
	 * @param num
	 */
	private static void testStream(List<Credit> portfolio, int horizon, int num) {

		Random rndGen = new Random();

		// 使用传统的循环迭代方法进行计算
		double[] losses = new double[num];
		for (int i = 0; i < num; i++) {
			for (Credit crd : portfolio) {
				int remDays = Math.min(crd.getRemainingTerm(), horizon);

				if (rndGen.nextDouble() >= 1 - crd.getDefaultProbability(remDays))
					losses[i] += (1 + crd.getAnnualRate() * Math.min(horizon, crd.getRemainingTerm()) / 365)
							* crd.getRemainingAmount();
				else
					losses[i] -= crd.getAnnualRate() * Math.min(horizon, crd.getRemainingTerm()) / 365
							* crd.getRemainingAmount();
			}
		}

		// 使用IntStream调用parallel()方法来执行Integer数据类型的并行流处理操作
		IntStream.range(0, num).parallel().forEach(i -> {
			for (Credit crd : portfolio) {
				int remDays = Math.min(crd.getRemainingTerm(), horizon);

				if (rndGen.nextDouble() >= 1 - crd.getDefaultProbability(remDays))
					losses[i] += (1 + crd.getAnnualRate() * Math.min(horizon, crd.getRemainingTerm()) / 365)
							* crd.getRemainingAmount();
				else
					losses[i] -= crd.getAnnualRate() * Math.min(horizon, crd.getRemainingTerm()) / 365
							* crd.getRemainingAmount();
			}
		});
	}

	public static void testTime() {

		// get current date
		LocalDate today = LocalDate.now();
		System.out.println("Today's Local date : " + today);

		// get current time
		LocalTime time = LocalTime.now();
		System.out.println("local time now : " + time);

		// timestamp
		Instant timestamp = Instant.now();
		System.out.println("What is value of this instant " + timestamp);

		// get year - month - day
		int year = today.getYear();
		int month = today.getMonthValue();
		int day = today.getDayOfMonth();
		System.out.printf("Year : %d Month : %d day : %d \t %n", year, month, day);

		// get a specified day
		LocalDate dateOfBirth = LocalDate.of(2015, 03, 31);
		System.out.println("Your Date of birth is : " + dateOfBirth);

		// check if two given date are the same
		if (dateOfBirth.equals(today)) {
			System.out.printf("Today %s and dateOfBirth %s are same date %n", today, dateOfBirth);
		}

		// compare
		if (dateOfBirth.isBefore(today)) {
			System.out.println("dateOfBirth is day before today");
		}

		// check duplicate days
		MonthDay birthday = MonthDay.of(dateOfBirth.getMonth(), dateOfBirth.getDayOfMonth());
		MonthDay currentMonthDay = MonthDay.from(today);
		if (currentMonthDay.equals(birthday)) {
			System.out.println("Many Many happy returns of the day !!");
		} else {
			System.out.println("Sorry, today is not your birthday");
		}

		// add hour to time
		LocalTime newTime = time.plusHours(2); // adding two hours
		System.out.println("Time after 2 hours : " + newTime);

		// get next week day
		LocalDate nextWeek = today.plus(1, ChronoUnit.WEEKS);
		System.out.println("Date after 1 week : " + nextWeek);

		// get the date of last year
		LocalDate previousYear = today.minus(1, ChronoUnit.YEARS);
		System.out.println("Date before 1 year : " + previousYear);
		LocalDate nextYear = today.plus(1, ChronoUnit.YEARS);
		System.out.println("Date after 1 year : " + nextYear);

		// Returns the current time based on your system clock and set to UTC.
		Clock clock = Clock.systemUTC();
		System.out.println("Clock : " + clock);

		// Returns time based on system clock zone Clock defaultClock =
		Clock.systemDefaultZone();
		System.out.println("Clock : " + clock);

		// Date and time with timezone in Java 8 ZoneId america =
		// ZoneId.of("America/New_York");
		LocalDateTime localtDateAndTime = LocalDateTime.now();
		// ZonedDateTime dateAndTimeInNewYork =
		// ZonedDateTime.of(localtDateAndTime, ZoneId.of("IET"));
		// System.out.println("Current date and time in a particular timezone :
		// "
		// + dateAndTimeInNewYork);

		//
		YearMonth currentYearMonth = YearMonth.now();
		System.out.printf("Days in month year %s: %d%n", currentYearMonth, currentYearMonth.lengthOfMonth());
		YearMonth creditCardExpiry = YearMonth.of(2018, Month.FEBRUARY);
		System.out.printf("Your credit card expires on %s %n", creditCardExpiry);

		// leap year
		if (today.isLeapYear()) {
			System.out.println("This year is Leap year");
		} else {
			System.out.println("2014 is not a Leap year");
		}

		// days between two date
		LocalDate java8Release = LocalDate.of(2014, Month.MARCH, 14);
		Period periodToNextJavaRelease = Period.between(today, java8Release);
		System.out.println("Months left between today and Java 8 release : " + periodToNextJavaRelease.getMonths());

		// time zone offset date
		LocalDateTime datetime = LocalDateTime.of(2014, Month.JANUARY, 14, 19, 30);
		ZoneOffset offset = ZoneOffset.of("+05:30");
		OffsetDateTime date = OffsetDateTime.of(datetime, offset);
		System.out.println("Date and Time with timezone offset in Java : " + date);

		// formatter
		String dayAfterTommorrow = "20140116";
		LocalDate formatted = LocalDate.parse(dayAfterTommorrow, DateTimeFormatter.BASIC_ISO_DATE);
		System.out.printf("Date generated from String %s is %s %n", dayAfterTommorrow, formatted);

		// parse date
		// String goodFriday = "Apr 18 2014";
		// try {
		// DateTimeFormatter formatter =
		// DateTimeFormatter.ofPattern("MMM dd yyyy");
		// LocalDate holiday = LocalDate.parse(goodFriday, formatter);
		// System.out.printf("Successfully parsed String %s, date is %s%n",
		// goodFriday, holiday);
		// } catch (DateTimeParseException ex) {
		// System.out.printf("%s is not parsable!%n", goodFriday);
		// ex.printStackTrace();
		// }

		// format
		LocalDateTime arrivalDate = LocalDateTime.now();
		try {
			DateTimeFormatter format = DateTimeFormatter.ofPattern("MMM dd yyyy hh:mm a");
			String landing = arrivalDate.format(format);
			System.out.printf("Arriving at : %s %n", landing);
		} catch (DateTimeException ex) {
			System.out.printf("%s can't be formatted!%n", arrivalDate);
			ex.printStackTrace();
		}

		System.out.println(LocalDate.parse("2015-10-22").getDayOfWeek());
		Calendar c = Calendar.getInstance();
		c.set(2015, 10, 22);
		System.out.println(c.get(Calendar.WEEK_OF_YEAR));

	}

	private static void changeCode() {

		String s = "601398_SH_EQ,600775_SH_EQ,002588_SZ_EQ";
		String[] secuArray = s.split(",");

		long t1 = System.currentTimeMillis();
		String sss = "";
		for (String tik : secuArray) {
			if (tik.contains("SH")) {
				sss = sss + "sh" + tik.substring(0, 6) + ",";
			} else if (tik.contains("SZ")) {
				sss = sss + "sz" + tik.substring(0, 6) + ",";
			}
		}
		long t2 = System.currentTimeMillis();
		int len = secuArray.length;
		for (int i = 0; i < len; i++) {
			String secu = secuArray[i];
			if (secu.contains("SH")) {
				secuArray[i] = "sh" + secu.substring(0, 6);
			} else if (secu.contains("SZ")) {
				secuArray[i] = "sz" + secu.substring(0, 6);
			}
		}
		String ss = StringUtils.join(secuArray, ",");
		long t3 = System.currentTimeMillis();

		System.out.println(ss);
		System.out.println(t3 - t2);
		System.out.println(sss);
		System.out.println(t2 - t1);

	}

	private static void testStringJoins() {
		List<String> names = Arrays.asList("Roger", "Tom", "Terry", "Jack");

		// print the names in uppercase with comma separated
		System.out.println(names.stream().map(String::toUpperCase).collect(joining(", ")));
	}

	private static void testPredicate(int number, Predicate<Integer> predicate, String msg) {
		System.out.println(number + " " + msg + ":" + predicate.test(number));

	}

	private static double compute(int number) {
		return Math.sqrt(number);
	}

	private static int doubleIt(int number) {
		System.out.println(number + " : " + Thread.currentThread());
		try {
			Thread.sleep(500);
		} catch (Exception ex) {

		}
		return number * 2;
	}

	private static void testParallelStream() {
		List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16);

		long t1 = System.currentTimeMillis();
		System.out.println(numbers.stream().map(TestJDK8::doubleIt).reduce(0, Integer::sum));
		long t2 = System.currentTimeMillis();
		System.out.println(numbers.parallelStream().map(TestJDK8::doubleIt).reduce(0, Integer::sum));
		long t3 = System.currentTimeMillis();
		System.out.println(t2 - t1 + " " + (t3 - t2));
	}

	public static void main(String[] args) {

		// testRunnable();
		//
		// testListFilter();
		//
		testComparator();
		//
		// changeCode();

		// testTime();
		testStringJoins();

		System.out.println(Util.numberOfCores());

		SeaPlane seaPlane = new SeaPlane();
		seaPlane.takeOff();
		seaPlane.turn();
		seaPlane.cruise();
		seaPlane.land();
		// FastFly : take off
		// Fly : turn
		// SeaPlane : cruise
		// Fly : cruise
		// Vehicle : land

		Predicate<Integer> isEven = e -> e % 2 == 0;
		Predicate<Integer> isGreatThan4 = e -> e > 4;
		testPredicate(5, isEven, "is even?");
		testPredicate(5, isEven.and(isGreatThan4), "is even and great than 4?");

		Map<Integer, Double> sqrt = new HashMap<>();
		sqrt.computeIfAbsent(4, TestJDK8::compute);
		System.out.println(sqrt.get(4));

		testParallelStream();

	}

}

interface Util {
	// static interface method
	public static int numberOfCores() {
		return Runtime.getRuntime().availableProcessors();
	}

}

interface Fly {
	// default method
	// four rules of default method
	// 1. you get what is in the base interface
	// 2. you may override a default method
	// 3. if a method is there in the class hiearchy then it takes precedence
	// 4. if there is no method on any of the classes in the hierachy, but two
	// of your interfaces
	// that you implements has the default method, to solve this use rule 3.
	default void takeOff() {
		System.out.println("Fly : take off");
		getState();
	}

	default void turn() {
		System.out.println("Fly : turn");
	}

	default void cruise() {
		System.out.println("Fly : cruise");
	}

	default void land() {
		System.out.println("Fly : land");
	}

	void getState();
}

interface FastFly extends Fly {
	default void takeOff() {
		System.out.println("FastFly : take off");
	}
}

interface Sail {
	default void cruise() {
		System.out.println("Sail : cruise");
	}
}

class Vehicle {
	public void land() {
		System.out.println("Vehicle : land");
	}
}

class SeaPlane extends Vehicle implements FastFly, Sail {

	@Override
	public void getState() {
		// TODO Auto-generated method stub

	}

	public void cruise() {
		System.out.println("SeaPlane : cruise");
		FastFly.super.cruise();
	}

}