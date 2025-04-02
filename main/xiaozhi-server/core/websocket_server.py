import asyncio
import ssl
import websockets
from config.logger import setup_logging
from core.connection import ConnectionHandler
from core.utils.util import get_local_ip
from core.utils.util import get_public_ip
from core.utils import asr, vad, llm, tts, memory, intent

TAG = __name__


class WebSocketServer:
    def __init__(self, config: dict):
        self.config = config
        self.logger = setup_logging()
        self._vad, self._asr, self._llm, self._tts, self._memory, self.intent = (
            self._create_processing_instances()
        )
        self.active_connections = set()  # 添加全局连接记录

    def _create_processing_instances(self):
        memory_cls_name = self.config["selected_module"].get(
            "Memory", "nomem"
        )  # 默认使用nomem
        has_memory_cfg = (
            self.config.get("Memory") and memory_cls_name in self.config["Memory"]
        )
        memory_cfg = self.config["Memory"][memory_cls_name] if has_memory_cfg else {}

        """创建处理模块实例"""
        return (
            vad.create_instance(
                self.config["selected_module"]["VAD"],
                self.config["VAD"][self.config["selected_module"]["VAD"]],
            ),
            asr.create_instance(
                (
                    self.config["selected_module"]["ASR"]
                    if not "type"
                    in self.config["ASR"][self.config["selected_module"]["ASR"]]
                    else self.config["ASR"][self.config["selected_module"]["ASR"]][
                        "type"
                    ]
                ),
                self.config["ASR"][self.config["selected_module"]["ASR"]],
                self.config["delete_audio"],
            ),
            llm.create_instance(
                (
                    self.config["selected_module"]["LLM"]
                    if not "type"
                    in self.config["LLM"][self.config["selected_module"]["LLM"]]
                    else self.config["LLM"][self.config["selected_module"]["LLM"]][
                        "type"
                    ]
                ),
                self.config["LLM"][self.config["selected_module"]["LLM"]],
            ),
            tts.create_instance(
                (
                    self.config["selected_module"]["TTS"]
                    if not "type"
                    in self.config["TTS"][self.config["selected_module"]["TTS"]]
                    else self.config["TTS"][self.config["selected_module"]["TTS"]][
                        "type"
                    ]
                ),
                self.config["TTS"][self.config["selected_module"]["TTS"]],
                self.config["delete_audio"],
            ),
            memory.create_instance(memory_cls_name, memory_cfg),
            intent.create_instance(
                (
                    self.config["selected_module"]["Intent"]
                    if not "type"
                    in self.config["Intent"][self.config["selected_module"]["Intent"]]
                    else self.config["Intent"][
                        self.config["selected_module"]["Intent"]
                    ]["type"]
                ),
                self.config["Intent"][self.config["selected_module"]["Intent"]],
            ),
        )

    async def start(self):
        server_config = self.config["server"]
        host = server_config["ip"]
        port = server_config["port"]

        # 1) 创建 SSL 上下文对象
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # 2) 加载你的证书和私钥
        # certfile和keyfile请根据你自己的文件名调整
        ssl_context.load_cert_chain(
            certfile="core/certs/xiaozhiai.koreacentral.cloudapp.azure.com-crt.pem",
            keyfile="core/certs/xiaozhiai.koreacentral.cloudapp.azure.com-key.pem"
        )

        self.logger.bind(tag=TAG).info("Server is running locally at wss://{}:{}", get_local_ip(), port)
        self.logger.bind(tag=TAG).info("Server is running publicly at wss://{}:{}", get_public_ip(), port)
        self.logger.bind(tag=TAG).info("=======上面的地址是加密的websocket协议地址，请勿用浏览器直接访问=======")

        async with websockets.serve(
                self._handle_connection,
                host,
                port,
                ssl=ssl_context
        ):
            await asyncio.Future()

    async def _handle_connection(self, websocket):
        """处理新连接，每次创建独立的ConnectionHandler"""
        # 创建ConnectionHandler时传入当前server实例
        handler = ConnectionHandler(
            self.config,
            self._vad,
            self._asr,
            self._llm,
            self._tts,
            self._memory,
            self.intent,
        )
        self.active_connections.add(handler)
        try:
            await handler.handle_connection(websocket)
        finally:
            self.active_connections.discard(handler)
