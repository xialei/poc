package com.aug3.test.docs;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

public class PdfReader {

	public void readFdf(String file) throws Exception {
		// 是否排序
		boolean sort = false;
		// pdf文件名
		String pdfFile = file;
		// 输入文本文件名称
		String textFile = null;
		// 编码方式
		String encoding = "UTF-8";
		// 开始提取页数
		int startPage = 1;
		// 结束提取页数
		int endPage = Integer.MAX_VALUE;
		// 文件输入流，生成文本文件
		Writer output = null;
		// 内存中存储的PDF Document
		PDDocument document = null;

		try {
			document = PDDocument.load(new File(pdfFile));
			// 以原来PDF的名称来命名新产生的txt文件
			if (pdfFile.length() > 4) {
				File outputFile = new File(pdfFile.substring(0, pdfFile.length() - 4) + ".txt");
				textFile = outputFile.getName();
			}

			// 文件输入流，写入文件倒textFile
			output = new OutputStreamWriter(new FileOutputStream(textFile), encoding);
			// PDFTextStripper来提取文本
			PDFTextStripper stripper = null;
			stripper = new PDFTextStripper();
			// 设置是否排序
			stripper.setSortByPosition(sort);
			// 设置起始页
			stripper.setStartPage(startPage);
			// 设置结束页
			stripper.setEndPage(endPage);
			// 调用PDFTextStripper的writeText提取并输出文本
			stripper.writeText(document, output);
		} finally {
			if (output != null) {
				// 关闭输出流
				output.close();
			}
			if (document != null) {
				// 关闭PDF Document
				document.close();
			}
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		PdfReader pdfReader = new PdfReader();
		try {
			pdfReader.readFdf("D:\\test\\c.pdf");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
