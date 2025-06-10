# template and basic chain

from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompt import *
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import *
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json
import os

load_dotenv()

def GetJsonFromLLM(pdf_path):
    
    llm = ChatOpenAI(
        model_name="o4-mini",
        base_url="https://api.openai-proxy.org/v1",   
        # temperature=0.1
    )
    # option: gemini模型
    # llm = ChatGoogleGenerativeAI(
    #     model = "gemini-2.0-flash-lite-preview-02-05",
    #     client_options={"api_endpoint": "https://api.openai-proxy.org/google"},   
    #     google_api_key = os.getenv("GEMINI_API_KEY"),
    #     streaming=True,  # 启用流式输出
    #     callbacks=[StreamingStdOutCallbackHandler()],  # 流式输出到终端
    #     temperature=0.0
    # )

    # 文档加载
    loader = PyPDFLoader(os.path.join('ERP', pdf_path))
    documents = loader.load()

    # 合并所有文档页面为一个字符串
    full_text = "\n".join([doc.page_content for doc in documents])

    #print(full_text)
    # prompt 模板
    template = TPL
    prompt = PromptTemplate(
        template=template,
        input_variables=['topic','context'],
    )
    #print(TPL)

    # # construct chain
    chain = LLMChain(prompt=prompt, llm=llm,verbose= True)
    result =chain.run(topic= pdf_path.rsplit('.', 1)[0],context = full_text)
    print(result)

    jsonResult = json.loads(result)
    return jsonResult


def main():
    # 选取ERP所在PDF的路径
    folder_path = 'ERP'
    file_names = os.listdir(folder_path)
    print(file_names)
    # exit(0)
    for  pdf_path in file_names:
        out_path = os.path.join('outputXML',pdf_path.replace('.pdf', '.xml'))
        if  os.path.exists(out_path): continue
        # 获取为前面转化的json
        json_data =GetJsonFromLLM(pdf_path)

        xml_output = json_to_xml(json_data)
       
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(xml_output)
        print(f"[INFO] XML 文件已保存至: {out_path}")


if __name__ == "__main__":
    main()