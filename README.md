参考计算学部群友的ai 大战知识图谱。fix 了其中的llm生成特殊符号会导致的文件错误。放置到utils.py, 可单独使用这个文件结合openai的官方大模型平台进行免费使用进行json转XML。



使用付费api的llm 生成：

1.将PPT放入ERP 文件夹

2.安装langchain （python>=3.11）

3.python basic_chain_origin.py



创建 .env文件存放openai 或者 Gemini key， 我采用的是closeai 的base_url，o4-mini。

ps. 因为输入过长可能产生未响应的错误，可以多尝试几遍，等待时间较长，或者使用summarize_chain 结合 RecursiveCharacterTextSplitter 进行分割。（但是担心效果不好就没有尝试使用）。

