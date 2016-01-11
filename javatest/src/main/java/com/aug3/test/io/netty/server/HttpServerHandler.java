package com.aug3.test.io.netty.server;

import java.util.List;
import java.util.Map;

import org.jboss.netty.buffer.ChannelBuffer;
import org.jboss.netty.buffer.ChannelBuffers;
import org.jboss.netty.channel.ChannelFuture;
import org.jboss.netty.channel.ChannelFutureListener;
import org.jboss.netty.channel.ChannelHandlerContext;
import org.jboss.netty.channel.ExceptionEvent;
import org.jboss.netty.channel.MessageEvent;
import org.jboss.netty.channel.SimpleChannelUpstreamHandler;
import org.jboss.netty.handler.codec.http.DefaultHttpResponse;
import org.jboss.netty.handler.codec.http.HttpHeaders;
import org.jboss.netty.handler.codec.http.HttpMethod;
import org.jboss.netty.handler.codec.http.HttpRequest;
import org.jboss.netty.handler.codec.http.HttpResponse;
import org.jboss.netty.handler.codec.http.HttpResponseStatus;
import org.jboss.netty.handler.codec.http.HttpVersion;
import org.jboss.netty.handler.codec.http.QueryStringDecoder;
import org.jboss.netty.handler.codec.http.multipart.Attribute;
import org.jboss.netty.handler.codec.http.multipart.DefaultHttpDataFactory;
import org.jboss.netty.handler.codec.http.multipart.HttpPostRequestDecoder;
import org.jboss.netty.handler.codec.http.multipart.InterfaceHttpData;
import org.jboss.netty.handler.codec.http.multipart.InterfaceHttpData.HttpDataType;
import org.jboss.netty.handler.codec.http.websocketx.CloseWebSocketFrame;
import org.jboss.netty.handler.codec.http.websocketx.PingWebSocketFrame;
import org.jboss.netty.handler.codec.http.websocketx.PongWebSocketFrame;
import org.jboss.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import org.jboss.netty.handler.codec.http.websocketx.WebSocketFrame;
import org.jboss.netty.handler.codec.http.websocketx.WebSocketServerHandshaker;
import org.jboss.netty.handler.codec.http.websocketx.WebSocketServerHandshakerFactory;
import org.jboss.netty.util.CharsetUtil;

/**
public class HttpServerHandler extends SimpleChannelUpstreamHandler {

	private WebSocketServerHandshaker handshaker;
	private static final String WEBSOCKET_PATH = "/websocket";

	@Override
	public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) throws Exception {
		Object msg = e.getMessage();
		if (msg instanceof HttpRequest) {
			handleHttpRequest(ctx, (HttpRequest) msg);
		} else if (msg instanceof WebSocketFrame) {
			handleWebSocketFrame(ctx, (WebSocketFrame) msg);
		}
	}

	private void handleHttpRequest(ChannelHandlerContext ctx, HttpRequest req) throws Exception {
		System.out.println("handleHttpRequest method==========" + req.getMethod());
		System.out.println("handleHttpRequest uri==========" + req.getUri());
		if (req.getMethod() == HttpMethod.GET) { // 处理get请求
			if (req.getUri().equals("/websocket")) {
				// Handshake
				WebSocketServerHandshakerFactory wsFactory = new WebSocketServerHandshakerFactory(
						getWebSocketLocation(req), null, false);
				handshaker = wsFactory.newHandshaker(req);
				if (handshaker == null) {
					wsFactory.sendUnsupportedWebSocketVersionResponse(ctx.getChannel());
				} else {
					handshaker.handshake(ctx.getChannel(), req).addListener(
							WebSocketServerHandshaker.HANDSHAKE_LISTENER);
				}
			} else {
				QueryStringDecoder decoder = new QueryStringDecoder(req.getUri());
				Map<String, List<String>> parame = decoder.getParameters();
				List<String> q = parame.get("q"); // 读取从客户端传过来的参数
				String question = q.get(0);
				if (question != null && !question.equals("")) {
					System.out.println("r :" + question);
					HttpResponse res = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
					String data = "<html><body>你好，GET</body><html>";
					ChannelBuffer content = ChannelBuffers.copiedBuffer(data, CharsetUtil.UTF_8);
					res.setHeader(HttpHeaders.Names.CONTENT_TYPE, "text/html; charset=UTF-8");
					res.setHeader(HttpHeaders.Names.ACCESS_CONTROL_ALLOW_ORIGIN, "*");
					HttpHeaders.setContentLength(res, content.readableBytes());
					res.setContent(content);
					sendHttpResponse(ctx, req, res);
				}
			}
		}
		if (req.getMethod() == HttpMethod.POST) { // 处理POST请求
			HttpPostRequestDecoder decoder = new HttpPostRequestDecoder(new DefaultHttpDataFactory(false), req);
			InterfaceHttpData postData = decoder.getBodyHttpData("q"); // 读取从客户端传过来的参数
			String question = "";
			if (postData.getHttpDataType() == HttpDataType.Attribute) {
				Attribute attribute = (Attribute) postData;
				question = attribute.getValue();
				System.out.println("q:" + question);

			}
			if (question != null && !question.equals("")) {

				HttpResponse res = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
				String data = "<html><body>你好，POST</body><html>";
				ChannelBuffer content = ChannelBuffers.copiedBuffer(data, CharsetUtil.UTF_8);
				res.setHeader(HttpHeaders.Names.CONTENT_TYPE, "text/html; charset=UTF-8");
				res.setHeader(HttpHeaders.Names.ACCESS_CONTROL_ALLOW_ORIGIN, "*");
				HttpHeaders.setContentLength(res, content.readableBytes());
				res.setContent(content);
				sendHttpResponse(ctx, req, res);

			}
			return;
		}
	}

	@Override
	public void exceptionCaught(ChannelHandlerContext ctx, ExceptionEvent e) throws Exception {
		e.getCause().printStackTrace();
		e.getChannel().close();
	}

	private void handleWebSocketFrame(ChannelHandlerContext ctx, WebSocketFrame frame) {
		if (frame instanceof CloseWebSocketFrame) {
			handshaker.close(ctx.getChannel(), (CloseWebSocketFrame) frame);
			return;
		}
		if (frame instanceof PingWebSocketFrame) {
			ctx.getChannel().write(new PongWebSocketFrame(frame.getBinaryData()));
			return;
		}
		if (!(frame instanceof TextWebSocketFrame)) {
			throw new UnsupportedOperationException(String.format("%s frame types not supported", frame.getClass()
					.getName()));
		}
		String request = ((TextWebSocketFrame) frame).getText();
		System.out.println("收到socket msg=" + request);
		request = "这是来自服务器端的数据:收到socket msg=" + request;
		ctx.getChannel().write(new TextWebSocketFrame(request.toUpperCase()));
	}

	private static void sendHttpResponse(ChannelHandlerContext ctx, HttpRequest req, HttpResponse res) {
		if (res.getStatus().getCode() != 200) {
			res.setContent(ChannelBuffers.copiedBuffer(res.getStatus().toString(), CharsetUtil.UTF_8));
			HttpHeaders.setContentLength(res, res.getContent().readableBytes());
		}

		ChannelFuture f = ctx.getChannel().write(res);
		if (!HttpHeaders.isKeepAlive(req) || res.getStatus().getCode() != 200) {
			f.addListener(ChannelFutureListener.CLOSE);
		}
	}

	private static String getWebSocketLocation(HttpRequest req) {
		return "ws://" + req.getHeader(HttpHeaders.Names.HOST) + WEBSOCKET_PATH;
	}

}

**/
