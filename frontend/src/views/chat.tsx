import { useState } from "react";
import type { Message } from "@/types/chat";
import { AutoScrollContainer } from "@/components/auto-scroll-container";
import { ChatBubble } from "@/components/chat/chat-bubble";
import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { LoaderIcon } from "@/icons/loader";
import { SendIcon } from "@/icons/send";
import { chartService } from "@/services/chart";
import { handleChartTypeError } from "@/utils/errors";
import { motion } from "motion/react";

export const ChatView = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [inputError, setInputError] = useState("");

  const fetchChart = async (question: string) => {
    const messageId = crypto.randomUUID();
    setLoading(true);
    try {
      // Add loading message
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: messageId,
          role: "assistant",
          status: "loading",
        },
      ]);

      const result = await chartService.requestChart(question);

      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === messageId && msg.role === "assistant"
            ? { ...msg, status: "success", content: result.chart }
            : msg
        )
      );
    } catch (error) {
      if (error instanceof Error) {
        // Handle error and map to user-friendly message
        const errorMessage = handleChartTypeError(error.message);

        setMessages((prevMessages) =>
          prevMessages.map((msg) =>
            msg.id === messageId && msg.role === "assistant"
              ? {
                  ...msg,
                  status: "error",
                  content: { error: errorMessage },
                }
              : msg
          )
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const trimmedQuestion = question.trim();
    // Validate input length
    const isValid = validateInput(trimmedQuestion);

    if (!isValid) return;

    // Add user message to chat
    setMessages([
      ...messages,
      { id: crypto.randomUUID(), role: "user", content: trimmedQuestion },
    ]);
    setQuestion("");
    try {
      fetchChart(trimmedQuestion);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const validateInput = (input: string) => {
    if (input.length < 10 || input.length > 200) {
      setInputError("Question must be between 10 and 200 characters.");
      return false;
    } else {
      setInputError("");
      return true;
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Validate input on change only if there is an error
    if (inputError) validateInput(e.target.value);
    setQuestion(e.target.value);
  };

  return (
    <div className="h-screen flex flex-col font-sans pb-2">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Navbar />
      </motion.div>
      <div className="h-[calc(100vh-4rem)] max-w-2xl w-full mx-auto flex flex-col ">
        <AutoScrollContainer className="flex-1 flex flex-col space-y-4 overflow-scroll hide-scrollbar py-4 px-2">
          {messages.map((message) => (
            <ChatBubble key={message.id} message={message} />
          ))}
        </AutoScrollContainer>
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex gap-2 px-2 z-10 bg-white w-full py-2"
          onSubmit={handleSubmit}
        >
          <Input
            value={question}
            onChange={handleInputChange}
            placeholder="Ask a question..."
            error={inputError}
          />
          <Button type="submit" disabled={loading || !!inputError}>
            {loading ? <LoaderIcon className="animate-spin" /> : <SendIcon />}
          </Button>
        </motion.form>
      </div>
    </div>
  );
};
