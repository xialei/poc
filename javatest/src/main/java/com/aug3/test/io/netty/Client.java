package com.aug3.test.io.netty;

import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

import org.jboss.netty.bootstrap.ClientBootstrap;
import org.jboss.netty.buffer.ChannelBuffer;
import org.jboss.netty.channel.ChannelHandler;
import org.jboss.netty.channel.ChannelHandlerContext;
import org.jboss.netty.channel.ChannelPipeline;
import org.jboss.netty.channel.ChannelPipelineFactory;
import org.jboss.netty.channel.ChannelStateEvent;
import org.jboss.netty.channel.Channels;
import org.jboss.netty.channel.MessageEvent;
import org.jboss.netty.channel.SimpleChannelUpstreamHandler;
import org.jboss.netty.channel.socket.nio.NioClientSocketChannelFactory;

public class Client {

	ClientBootstrap bootstrap;
	ChannelHandler myHandler = new MyClientHandler();
	StringClientHandler stringHandler = new StringClientHandler();

	String host;
	int port;

	public Client() {
		bootstrap = new ClientBootstrap(new NioClientSocketChannelFactory(Executors.newCachedThreadPool(),
				Executors.newCachedThreadPool()));

		bootstrap.setPipelineFactory(new ChannelPipelineFactory() {

			@Override
			public ChannelPipeline getPipeline() throws Exception {

				return Channels.pipeline(stringHandler, myHandler);
			}

		});
	}

	Client config(String host, int port) {
		this.host = host;
		this.port = port;
		bootstrap.setOption("remoteAddress", new InetSocketAddress(this.host, this.port));
		return this;
	}

	void start() {
		bootstrap.connect();
	}

	class MyClientHandler extends SimpleChannelUpstreamHandler {
		@Override
		public void channelClosed(ChannelHandlerContext ctx, ChannelStateEvent e) throws Exception {
			System.out.println("Client Channel closed " + e);
		}

		@Override
		public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) throws Exception {
			System.out.println("Client Channel connected " + e);
		}

		@Override
		public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) throws Exception {
			try {
				// if no string client handler
				// ChannelBuffer buf = (ChannelBuffer) e.getMessage();
				// byte[] bytes = buf.array();
				// System.out.println("Client reseived message : " + new
				// String(bytes));
				String msg = (String) e.getMessage();
				System.out.println("Client reseived message : " + msg);
			} catch (Exception ex) {
				ex.printStackTrace();
				throw ex;
			}
		}
	}

	class StringClientHandler extends SimpleChannelUpstreamHandler {
		@Override
		public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) throws Exception {
			try {
				ChannelBuffer buf = (ChannelBuffer) e.getMessage();
				byte[] bytes = buf.array();
				System.out.println("Client reseived message and convert it to a String!");
				Channels.fireMessageReceived(ctx, new String(bytes));
			} catch (Exception ex) {
				ex.printStackTrace();
				throw ex;
			}
		}
	}

}
