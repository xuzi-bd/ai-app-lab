// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// Licensed under the 【火山方舟】原型应用软件自用许可协议
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at 
//     https://www.volcengine.com/docs/82379/1433703
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { PostSSE } from '@/demo/longTermMemory/utils/PostSSE';
import { Memory } from '@/demo/longTermMemory/types';
import { useConfigStore } from '@/demo/longTermMemory/stores/useConfigStore';
import { useMemoryStore } from '@/demo/longTermMemory/stores/useMemoryStore';

export const startReasoning = (
  chatList: { role: string; content: string }[],
  onMessage: (data: string) => void,
  onEnd: () => void,
) => {
  const { botId, userId, apiPath } = useConfigStore.getState();
  const body = JSON.stringify({
    stream: true,
    model: '',
    metadata: {
      type: 'store_memory',
      user_id: userId,
      agent_id: botId,
      memory: [],
    },
    messages: chatList.map(({ role, content }) => ({ role, content })),
  });

  const headers = new Headers();
  headers.append('Content-Type', 'application/json');

  const eventSource = new PostSSE(apiPath, {
    body,
    headers,
    onMessage,
    onError: error => console.error('Reasoning error:', error),
    onEnd,
  });

  eventSource.connect();
};

export const listMemories = async (setMemoryList: (memories: Memory[]) => void) => {
  const { botId, userId, apiPath } = useConfigStore.getState();
  const body = JSON.stringify({
    stream: true,
    model: '',
    metadata: {
      type: 'list_memory',
      user_id: userId,
      agent_id: botId,
      memory: [],
    },
    messages: [],
  });

  const headers = new Headers();
  headers.append('Content-Type', 'application/json');

  const eventSource = new PostSSE(apiPath, {
    body,
    headers,
    onMessage: data => {
      try {
        const apiResponse: any = JSON.parse(data);
        const { metadata = {} as any } = apiResponse;
        const { returned_memories = [] } = metadata;

        const memories: Memory[] = returned_memories.map(
          (memory: { id: any; memory: any; created_at: any; updated_at: any }) => ({
            id: memory.id,
            content: memory.memory,
            createdAt: memory.created_at,
            updatedAt: memory.updated_at || memory.created_at,
          }),
        );

        setMemoryList(memories);
      } catch (error) {
        console.error('Error parsing memory list:', error);
      }
    },
    onError: error => console.error('Memory list error:', error),
    onEnd: () => {},
  });

  eventSource.connect();
};

export const startChat = (
  chatList: { role: string; content: string }[],
  onMessage: (data: string) => void,
  onEnd: () => void,
) => {
  const { botId, userId, apiPath } = useConfigStore.getState();
  const body = JSON.stringify({
    stream: true,
    model: '',
    metadata: {
      type: 'chat_completions',
      user_id: userId,
      agent_id: botId,
      memory: [],
    },
    messages: chatList.map(({ role, content }) => ({ role, content })),
  });

  const headers = new Headers();
  headers.append('Content-Type', 'application/json');

  const eventSource = new PostSSE(apiPath, {
    body,
    headers,
    onMessage,
    onError: error => console.error('Chat error:', error),
    onEnd,
  });

  eventSource.connect();
};

export const addMemory = () => {
  const { botId, userId, apiPath } = useConfigStore.getState();
  const { presetMemoryList } = useMemoryStore.getState();
  if (!presetMemoryList.length) {
    return;
  }
  const body = JSON.stringify({
    stream: true,
    model: '',
    metadata: {
      type: 'add_memory',
      user_id: userId,
      agent_id: botId,
      memory: presetMemoryList.map(m => m.content),
    },
    messages: [],
  });

  const headers = new Headers();
  headers.append('Content-Type', 'application/json');
  const hi = () => {};
  const eventSource = new PostSSE(apiPath, {
    body,
    headers,
    onMessage: hi,
    onError: hi,
    onEnd: hi,
  });

  eventSource.connect();
};
