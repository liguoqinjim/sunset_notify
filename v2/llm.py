import langchain
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

class SunsetReport(BaseModel):
    date: str = Field(description="报告中的日期")
    time: str = Field(description="报告中的时间")
    phase: str = Field(description="报告中的时间是属于日出还是日落，输出中文")
    aod550: float = Field(description="报告中的字段：AOD-550")
    quality: float = Field(description="报告中的字段：质量（不含AOD)")
    quality_report: str = Field(description="根据quality总结今天的火烧云质量")

    # # You can add custom validation logic easily with Pydantic.
    # @validator("setup")
    # def question_ends_with_question_mark(cls, field):
    #     if field[-1] != "?":
    #         raise ValueError("Badly formed question!")
    #     return field



def get_llm_quality_report(ocr_content):
    """
    根据ocr_content，调用openai返回火烧云的质量报告
    """
    template = """这是一份今天的火烧云预测数据：
    ```
    {report}
    ```
    下面是怎么使用这份数据的说明：
    ```
    质量（不含AOD)：
    0：今天没有火烧云
    0.1~0.5：火烧云质量一般，可能是因为颜色暗／云量少
    0.5~1：可观的火烧云，值得一看
    1~2：质量好的火烧云
    2以上：不仅质量好且持续时间很长
    ```

    请你总结今天的火烧云质量。{format_instructions}。
    Let's think step by step, and output in chinese"""

    # prompt = PromptTemplate(template=template, input_variables=["report"])
    parser = PydanticOutputParser(pydantic_object=SunsetReport)
    prompt = PromptTemplate(template=template, input_variables=["report"], partial_variables={"format_instructions": parser.get_format_instructions()})

    llm = OpenAI()
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    report = ocr_content

    output = llm_chain.run(report)
    print("output----")
    print(output)
    print("output----")

    report = parser.parse(output)
    return report