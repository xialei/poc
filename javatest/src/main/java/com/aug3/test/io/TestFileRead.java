package com.aug3.test.io;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

public class TestFileRead {

	private void readFromFileNIO(String file) {

		FileChannel channel = null;
		FileInputStream fis = null;
		try {
			fis = new FileInputStream(file);
			channel = fis.getChannel();
			long size = channel.size();
			ByteBuffer buffer = ByteBuffer.allocate((int) size);
			channel.read(buffer);
			buffer.rewind();

			for (int j = 0; j < size; j++) {
				buffer.get();

			}
			fis.close();

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				channel.close();
			} catch (IOException e1) {
			}
			try {
				fis.close();
			} catch (IOException e) {
			}
		}

	}

	private void readFromFileNIO2(String file) {

		FileChannel channel = null;
		FileInputStream fis = null;
		try {
			fis = new FileInputStream(file);
			channel = fis.getChannel();
			ByteBuffer buffer = ByteBuffer.allocate(4096);

			int size = 0;
			while ((size = channel.read(buffer)) != -1) {
				buffer.rewind();
				buffer.limit(size);
				buffer.clear();
			}

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				channel.close();
			} catch (IOException e1) {
			}
			try {
				fis.close();
			} catch (IOException e) {
			}
		}

	}

	private void readFromFileIO(String file) {

		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String line = null;
			while ((line = reader.readLine()) != null) {
				// System.out.println(line);
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void readFromFileIO2(String file) {

		FileInputStream fin = null;
		try {
			File f = new File(file);
			fin = new FileInputStream(f);

			byte fileContent[] = new byte[(int) f.length()];

			/*
			 * To read content of the file in byte array, use int read(byte[]
			 * byteArray) method of java FileInputStream class.
			 */
			fin.read(fileContent);

			// create string from byte array, cost much time
			// String strFileContent = new String(fileContent);

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				fin.close();
			} catch (IOException e) {
			}
		}
	}

	private void readFromFileIO3(String file) {

		BufferedInputStream bis = null;
		try {
			bis = new BufferedInputStream(new FileInputStream(file));

			byte byteBuf[] = new byte[4096];

			int size = 0;
			while ((size = bis.read(byteBuf)) != -1) {
			}

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				bis.close();
			} catch (IOException e) {
			}
		}
	}

	/**
	 * NIO :27
	 * 
	 * NIO2 :10
	 * 
	 * IO :343
	 * 
	 * IO2 :7
	 * 
	 * IO3 :3
	 * 
	 * time cost: BufferedInputStream (4096) < FileInputStream 
	 * < NIO FileChannel(buffer with fix size 4096) < NIO FileChannel(buffer with file size) < BufferedReader
	 * 
	 * @param args
	 */
	public static void main(String[] args) {

		String file = "D:\\Show_Me_the_Numbers_v2.pdf";
		TestFileRead reader = new TestFileRead();
		long t1 = System.currentTimeMillis();
		reader.readFromFileNIO(file);
		long t2 = System.currentTimeMillis();
		reader.readFromFileIO(file);
		long t3 = System.currentTimeMillis();
		reader.readFromFileNIO2(file);
		long t4 = System.currentTimeMillis();
		reader.readFromFileIO2(file);
		long t5 = System.currentTimeMillis();
		reader.readFromFileIO3(file);
		long t6 = System.currentTimeMillis();

		System.out.println("NIO :" + (t2 - t1));
		System.out.println("NIO2 :" + (t4 - t3));
		System.out.println("IO :" + (t3 - t2));
		System.out.println("IO2 :" + (t5 - t4));
		System.out.println("IO3 :" + (t6 - t5));

	}

}
