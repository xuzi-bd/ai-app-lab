# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Optional

from pydantic import BaseModel
from volcenginesdkarkruntime import AsyncArk
from volcenginesdkarkruntime.types.chat import ChatCompletionMessageParam

from arkitect.core.client.http import default_ark_client


class ArkToolRequest(BaseModel):
    """ """

    action_name: str
    tool_name: str

    parameters: Optional[Dict[str, Any]] = None
    dry_run: Optional[bool] = False
    timeout: Optional[int] = 60


class ArkToolResponse(BaseModel):
    status_code: Optional[int] = None

    data: Optional[Any] = None


async def execute(
    action_name, tool_name, parameters: dict[str, Any] | None = None, **kwargs: Any
) -> ArkToolResponse | ChatCompletionMessageParam:
    parameter = ArkToolRequest(
        action_name=action_name,
        tool_name=tool_name,
        parameters=parameters or {},
    )
    client: AsyncArk = default_ark_client()
    response = await client.post(
        path="/tools/execute",
        body=parameter.model_dump(),
        cast_to=ArkToolResponse,
    )
    return ArkToolResponse(**response)


async def calculator(input: str) -> str:
    """Evaluate a given mathematical expression

    Args:
        input (str): The mathematical expression in Wolfram Language InputForm

    Returns:
        str: computed value
    """
    return await execute(
        action_name="Calculator", tool_name="Calculator", parameters={"input": input}
    )


async def link_reader(url_list: list[str]):
    """当你需要获取网页、pdf、抖音视频内容时，使用此工具。可以获取url链接下的标题和内容。

    examples: {"url_list":["abc.com", "xyz.com"]}

    Args:
        url_list (list[str]): 需要解析网页链接,最多3个,以列表返回
    """
    return await execute(
        action_name="LinkReader",
        tool_name="LinkReader",
        parameters={"url_list": url_list},
    )
