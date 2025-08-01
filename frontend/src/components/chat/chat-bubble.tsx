import clsx from "clsx";
import { motion } from "motion/react";
import { Chart } from "@/components/chat/chart";
import { LoaderIcon } from "@/icons/loader";
import type { Message } from "@/types/chat";
import type { Figure } from "react-plotly.js";
import { WarnIcon } from "@/icons/warn";

// ChatBubble component renders a chat message with animation and styling based on role and status
export const ChatBubble = ({ message }: { message: Message }) => {
  const isError = message.role === "assistant" && message.status === "error";
  const isLoading =
    message.role === "assistant" && message.status === "loading";
  return (
    <motion.div
      initial={{ opacity: 0, x: message.role === "user" ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={clsx(
        "px-4 py-2 mb-2 max-w-9/10 rounded-xl text-sm md:text-base",
        message.role === "user"
          ? "bg-green-200/40 self-end rounded-br-sm w-fit"
          : "bg-green-100 self-start rounded-bl-sm w-full",
        (isError || isLoading) && "bg-transparent"
      )}
    >
      <MessageContent message={message} />
    </motion.div>
  );
};

const MessageContent = ({ message }: { message: Message }) => {
  if (message.role === "user") {
    return <UserMessage content={message.content} />;
  }
  if (message.role === "assistant") {
    switch (message.status) {
      case "success":
        return <AssistantSuccess content={message.content} />;
      case "error":
        return <AssistantError error={message.content?.error} />;
      case "loading":
        return <AssistantLoading />;
      default:
        return null;
    }
  }
  return null;
};

// Renders a user message
const UserMessage = ({ content }: { content: string }) => <>{content}</>;

// Renders a successful assistant message (chart)
const AssistantSuccess = ({ content }: { content: Figure }) => (
  <Chart figure={content} />
);

// Renders an error message from the assistant
const AssistantError = ({ error }: { error?: string }) => (
  <div className="text-red-500 text-xs flex items-center gap-2">
    <WarnIcon width={16} height={16} />
    {error || "Ups! Something went wrong."}
  </div>
);

// Renders a loading state for the assistant
const AssistantLoading = () => (
  <div className="text-gray-500 text-xs flex items-center gap-2">
    Processing answer...{" "}
    <LoaderIcon width={16} height={16} className="animate-spin" />
  </div>
);
