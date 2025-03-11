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

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from arkitect.core.component.llm.model import ChatCompletionTool
from arkitect.telemetry.trace import task

from .model import BaseToolResponse


class BaseTool(BaseModel, ABC):
    """
    Represents a base tool

    Tool has two core functions: tool_schema and execute
    tool_schema() is used to generate the manifest for the tool
        in the form of `ChatCompletionTool`
    execute() is used to execute the tool
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            **kwargs,
        )

    @task()
    @abstractmethod
    async def execute(self, **kwargs: Any) -> BaseToolResponse:
        """
        Executes the tool with the given parameters.
        """
        pass

    @abstractmethod
    def tool_schema(self) -> ChatCompletionTool:
        """
        Returns the schema of the tool.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return tool name
        """
        pass
