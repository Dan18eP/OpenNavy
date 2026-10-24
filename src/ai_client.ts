import OpenAI from "openai";

const SERVER_URL = process.env.AI_SERVER_URL || "http://localhost:11434/v1";
const API_KEY = process.env.AI_API_KEY || "ollama";
export const PRIMARY_MODEL = process.env.AI_MODEL_NAME || "gemma4:e4b";
export const FALLBACK_MODEL = process.env.AI_FALLBACK_MODEL || "gemma4:e2b";

export const aiClient = new OpenAI({
  baseURL: SERVER_URL,
  apiKey: API_KEY,
});

/**
 * Generador asíncrono para streaming de tokens
 */
export async function* streamCompletion(
  prompt: string,
  systemPrompt?: string,
  model: string = PRIMARY_MODEL,
  temperature: number = 0.2
): AsyncGenerator<string, void, unknown> {
  const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [];

  if (systemPrompt) {
    messages.push({ role: "system", content: systemPrompt });
  }
  messages.push({ role: "user", content: prompt });

  try {
    const stream = await aiClient.chat.completions.create({
      model,
      messages,
      stream: true,
      temperature,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  } catch (error) {
    if (model !== FALLBACK_MODEL) {
      console.warn(`[AI Client] Falló ${model}. Reintentando con modelo de respaldo ${FALLBACK_MODEL}...`);
      const fallbackStream = await aiClient.chat.completions.create({
        model: FALLBACK_MODEL,
        messages,
        stream: true,
        temperature,
      });

      for await (const chunk of fallbackStream) {
        const content = chunk.choices[0]?.delta?.content;
        if (content) {
          yield content;
        }
      }
    } else {
      throw error;
    }
  }
}

/**
 * Petición con retorno estricto en JSON
 */
export async function generateJSON<T = unknown>(
  prompt: string,
  systemPrompt?: string,
  model: string = PRIMARY_MODEL
): Promise<T> {
  const sys = systemPrompt
    ? `${systemPrompt} Return strictly valid JSON.`
    : "You are a helpful assistant. Output valid JSON only.";

  const response = await aiClient.chat.completions.create({
    model,
    messages: [
      { role: "system", content: sys },
      { role: "user", content: prompt },
    ],
    response_format: { type: "json_object" },
    temperature: 0.1,
  });

  const content = response.choices[0]?.message?.content || "{}";
  return JSON.parse(content) as T;
}
