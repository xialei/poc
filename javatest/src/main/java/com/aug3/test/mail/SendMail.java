package com.aug3.test.mail;

public class SendMail {

	public static void main(String[] args) {
		SendMail.send_163();
	}

	// 163邮箱
	public static void send_163() {
		// 这个类主要是设置邮件
		MailSenderInfo mailInfo = new MailSenderInfo();
		mailInfo.setMailServerHost("smtp.163.com");
		mailInfo.setMailServerPort("25");
		mailInfo.setValidate(true);
		mailInfo.setUserName("hello@163.com"); // 实际发送者
		mailInfo.setPassword("helloworld");// 您的邮箱密码
		mailInfo.setFromAddress("hello@163.com"); // 设置发送人邮箱地址
		mailInfo.setToAddress("u@163.com"); // 设置接受者邮箱地址
		mailInfo.setSubject("test");
		mailInfo.setContent("<a>http://www.1hyc.com</a>");
		// 这个类主要来发送邮件
		SimpleMailSender sms = new SimpleMailSender();
		sms.sendTextMail(mailInfo); // 发送文体格式
		sms.sendHtmlMail(mailInfo); // 发送html格式
	}
}
