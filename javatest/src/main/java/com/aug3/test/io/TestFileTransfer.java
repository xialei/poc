package com.aug3.test.io;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.nio.channels.FileChannel;

public class TestFileTransfer {

	private void copyFile(final String fromFile, final String toFile) throws IOException {
		File from = new File(fromFile);
		File to = new File(toFile);

		final InputStream is = new FileInputStream(from);
		try {
			final OutputStream os = new FileOutputStream(to);
			try {
				final byte[] buf = new byte[8192];
				int read = 0;
				while ((read = is.read(buf)) != -1) {
					os.write(buf, 0, read);
				}
			} finally {
				os.close();
			}
		} finally {
			is.close();
		}
	}

	private void copyFileNio(final String fromFile, final String toFile) throws IOException {

		File from = new File(fromFile);
		File to = new File(toFile);

		final RandomAccessFile inFile = new RandomAccessFile(from, "r");
		try {
			final RandomAccessFile outFile = new RandomAccessFile(to, "rw");
			try {
				final FileChannel inChannel = inFile.getChannel();
				final FileChannel outChannel = outFile.getChannel();
				long pos = 0;
				long toCopy = inFile.length();
				while (toCopy > 0) {
					final long bytes = inChannel.transferTo(pos, toCopy, outChannel);
					pos += bytes;
					toCopy -= bytes;
				}
			} finally {
				outFile.close();
			}
		} finally {
			inFile.close();
		}
	}

	/**
	 * IO :53, 6
	 * 
	 * NIO :49, 12
	 * 
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		String file = "D:\\Show_Me_the_Numbers_v2.pdf";
		TestFileTransfer fileOps = new TestFileTransfer();
		long t1 = System.currentTimeMillis();
		fileOps.copyFile(file, file + ".io");
		long t2 = System.currentTimeMillis();
		fileOps.copyFileNio(file, file + ".nio");
		long t3 = System.currentTimeMillis();

		System.out.println("IO :" + (t2 - t1));
		System.out.println("NIO :" + (t3 - t2));

	}

}
