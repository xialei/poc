package com.aug3.test.my;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.zip.ZipFile;

public class Testjdk7 {

	public static String getTypeOfDayWithSwitchStatement(String dayOfWeekArg) {
		String typeOfDay;
		switch (dayOfWeekArg) {
		case "Monday":
			typeOfDay = "Start of work week";
			break;
		case "Tuesday":
		case "Wednesday":
		case "Thursday":
			typeOfDay = "Midweek";
			break;
		case "Friday":
			typeOfDay = "End of work week";
			break;
		case "Saturday":
		case "Sunday":
			typeOfDay = "Weekend";
			break;
		default:
			throw new IllegalArgumentException("Invalid day of the week: " + dayOfWeekArg);
		}
		return typeOfDay;
	}

	public static void listZipFile(String zipFileName, String outputFilePath) throws IOException {

		try (ZipFile zf = new ZipFile(zipFileName);
				java.io.BufferedWriter writer = Files.newBufferedWriter(Paths.get(outputFilePath),
						StandardCharsets.UTF_8, StandardOpenOption.WRITE)) {
			// Enumerate each entry
			for (java.util.Enumeration entries = zf.entries(); entries.hasMoreElements();) {
				// Get the entry name and write it to the output file
				String newLine = System.getProperty("line.separator");
				String zipEntryName = ((java.util.zip.ZipEntry) entries.nextElement()).getName() + newLine;
				writer.write(zipEntryName, 0, zipEntryName.length());
			}
		}

	}

	public static void main(String[] args) throws IOException {
		System.out.println(getTypeOfDayWithSwitchStatement("Wednesday"));

		listZipFile("D:\\提示页.zip", "D:\\output\\");
	}

}
