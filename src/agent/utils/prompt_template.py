from langchain_core.prompts import ChatPromptTemplate

# Base template shared by all agents
BASE_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a specialized AI agent generator.
You will receive an agent specification and an improved prompt,
and must return only valid Next.js React code for that agent's page."""
    ),
    ("placeholder", "{messages}")
])

# Specific prompt templates for each agent
PROMPT_TEMPLATES = {
    "ConfigRouteAnalyzer": BASE_AGENT_PROMPT.with_messages([
        (
            "user",
            """
Agent Name: {agent_name}
Improved Prompt: {improved_prompt}

Agent JSON:
{agent_json}

CRITICAL REQUIREMENTS:
1. Return only valid React/Next.js page code.
2. Use fetch API for all HTTP calls.
3. Include imports, component, and export default.
"""
        )
    ]),
    "NetConfigSentry": BASE_AGENT_PROMPT.with_messages([
        (
            "user",
            """
Agent Name: NetConfigSentry
Improved Prompt: {improved_prompt}

Agent JSON:
{agent_json}

CRITICAL REQUIREMENTS:
1. Return only valid React/Next.js page code.
2. Use async/await with fetch.
3. Include imports, component, and export default.
"""
        )
    ]),
    "NextJsAgent": BASE_AGENT_PROMPT.with_messages([
        (
            "system",
            """Generate a complete Next.js React component for a dynamic agent interface based on this agent specification:

Agent Name: ${agentName or 'Custom Agent'}
Agent ID: ${agentName or 'Custom Agent'} (use this as the agentId when calling /api/ask-agent)
Improved Prompt: ${improvedPrompt or 'No additional context'}

Agent JSON Configuration:
{agentJson}

CRITICAL REQUIREMENTS:
1. Return ONLY valid code. Do NOT include markdown, explanations, or comments outside the code.
2. The file MUST start with an import statement (e.g., import  useState  from 'react').
3. On form submit, POST the user's plain text query and the agent's unique ID to /api/ask-agent as JSON:  query, agentId .
4. Use "${agentName or 'Custom Agent'}" as the agentId value.
5. Display the response from the backend in the UI.
6. Do NOT use mock data. Do NOT use JSON.parse on user input.
7. Assume the backend endpoint will use the agent's JSON to call NeuralSeek and return the answer.
8. Use fetch, not axios.
9. Always use async/await.

ALSO GENERATE THIS FILE:

Create a Next.js API route at pages/api/ask-agent.ts that:
- Accepts only POST requests with  query, agentId  in the body.
- Calls https://stagingapi.neuralseek.com/v1/liam-demo/agentId/maistro with the query as the payload.
- Uses the apikey from the environment variable process.env.NEURALSEEK_API_KEY.
- Returns the NeuralSeek response as JSON.
- Returns 405 for non-POST requests and 400 for missing fields.

""",
    "user",
    """
    Example implementation (as a string, not real code!):

\`\`\`ts
// pages/api/ask-agent.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { query, agentId } = req.body;
  if (!query || !agentId) {
    return res.status(400).json({ error: 'Missing query or agentId' });
  }
  const nsRes = await fetch(
    \`https://stagingapi.neuralseek.com/v1/liam-demo/\${agentId}/maistro\`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': process.env.NEURALSEEK_API_KEY!,
      },
      body: JSON.stringify({ params: { use_case_summary: query } }),
    }
  );
  const data = await nsRes.json();
  return res.status(200).json(data);
}
\`\`\`
    """
        )]
    ),
}

def get_prompt_template(agent_name: str) -> ChatPromptTemplate:
    """
    Factory function to retrieve the correct prompt template
    for a given agent name. Falls back to the base template.
    """
    return PROMPT_TEMPLATES.get(agent_name, BASE_AGENT_PROMPT)