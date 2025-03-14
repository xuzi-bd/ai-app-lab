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

from ..manifest import ParameterTypeEnum, ToolManifest, ToolParameter


class Calculator(ToolManifest):
    def __init__(self) -> None:
        super().__init__(
            action_name="Calculator",
            tool_name="Calculator",
            description="Evaluate a given mathematical expression",
            parameters=[
                ToolParameter(
                    name="input",
                    description="The mathematical expression in Wolfram"
                    + "Language InputForm",
                    param_type=ParameterTypeEnum.STRING,
                    required=True,
                )
            ],
        )
