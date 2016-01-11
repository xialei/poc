package com.aug3.test.docs;

import java.io.File;
import java.net.ConnectException;
import java.util.Date;

import com.artofsolving.jodconverter.DocumentConverter;
import com.artofsolving.jodconverter.openoffice.connection.OpenOfficeConnection;
import com.artofsolving.jodconverter.openoffice.connection.SocketOpenOfficeConnection;
import com.artofsolving.jodconverter.openoffice.converter.OpenOfficeDocumentConverter;

public class DocConverter {

	/**
	 * 将word文档转换成html文档
	 * 
	 * @param docFile
	 *            需要转换的word文档
	 * @param filepath
	 *            转换之后html的存放路径
	 * @return 转换之后的html文件
	 */
	public static File convert(File docFile, String filepath, String suffix) {
		// 创建保存html的文件
		File targetFile = new File(filepath + "/" + new Date().getTime() + suffix);
		// 创建Openoffice连接
		OpenOfficeConnection con = new SocketOpenOfficeConnection(8100);
		try {
			// 连接
			con.connect();
		} catch (ConnectException e) {
			System.out.println("获取OpenOffice连接失败...");
			e.printStackTrace();
		}
		// 创建转换器
		DocumentConverter converter = new OpenOfficeDocumentConverter(con);
		// 转换文档问html
		converter.convert(docFile, targetFile);
		// 关闭openoffice连接
		con.disconnect();
		return targetFile;
	}

	public static void main(String[] args) {
		System.out.println(convert(new File("D:/test/testexcel.xlsx"), "D:/test", ".pdf"));//不支持.xlsx, docx
	}

}
