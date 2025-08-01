import type { Figure } from "react-plotly.js";

type UserMessage = {
  id: string;
  role: "user";
  content: string;
};

type AssistantSuccessMessage = {
  status: "success";
  content: Figure;
};

type AssistantLoadingMessage = {
  status: "loading";
};

type AssistantErrorMessage = {
  status: "error";
  content: { error: string };
};

type AssistantMessage = {
  id: string;
  role: "assistant";
} & (AssistantSuccessMessage | AssistantLoadingMessage | AssistantErrorMessage);

export type Message = UserMessage | AssistantMessage;
