package com.aug3.test.io;

import java.io.IOException;
import java.nio.file.FileVisitOption;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.util.EnumSet;

public class TestFileVisitor {

	private void walkFilePath(Path dir) throws IOException {
		ListTree walk = new ListTree();
		Files.walkFileTree(dir, walk);

		// 遍历的时候跟踪链接
		EnumSet opts = EnumSet.of(FileVisitOption.FOLLOW_LINKS);
		try {
			Files.walkFileTree(dir, opts, Integer.MAX_VALUE, walk);
		} catch (IOException e) {
			System.err.println(e);
		}

	}

	class ListTree extends SimpleFileVisitor<Path> {

		@Override
		public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
			System.out.println("Visited directory: " + dir.toString());
			return FileVisitResult.CONTINUE;
		}

		@Override
		public FileVisitResult visitFileFailed(Path file, IOException exc) {
			System.out.println(exc);
			return FileVisitResult.CONTINUE;
		}
	}
	
	public static void main(String[] args) throws IOException {
		Path dir = Paths.get("D:\\hq");
		TestFileVisitor v = new TestFileVisitor();
		v.walkFilePath(dir);
	}

}
