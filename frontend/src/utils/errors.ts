export const UNSUPPORTED_CHART_TYPE_ERROR =
  "This chart type is not supported. Please try a different one.";

export const DEFAULT_API_ERROR =
  "An error occurred while processing the data. Please try again later.";

export const INVALID_INPUT_ERROR =
  "Invalid input. Please enter a valid question.";

export const NETWORK_ERROR =
  "Network error. Please check your connection and try again.";

export const TIMEOUT_ERROR = "The request timed out. Please try again later.";

export const NO_DATA_ERROR = "No data found for your query.";

export const QUESTION_LENGTH_ERROR =
  "Question must be between 10 and 200 characters.";

// List of error rules for mapping backend error messages to user-friendly messages
const errorRules: { test: (msg: string) => boolean; message: string }[] = [
  {
    test: (msg) => msg.includes("Network Error"),
    message: NETWORK_ERROR,
  },
  {
    test: (msg) => msg.includes("Timeout"),
    message: TIMEOUT_ERROR,
  },
  {
    test: (msg) =>
      msg.includes("No valid query generated") ||
      msg.includes("Invalid question"),
    message: INVALID_INPUT_ERROR,
  },
  {
    test: (msg) =>
      msg.includes("This chart is not currently supported") ||
      msg.includes("not supported"),
    message: UNSUPPORTED_CHART_TYPE_ERROR,
  },
  {
    test: (msg) => msg.includes("No data found"),
    message: NO_DATA_ERROR,
  },
  {
    test: (msg) =>
      msg.includes("Question must be between") || msg.includes("length"),
    message: QUESTION_LENGTH_ERROR,
  },
];

// Maps backend error messages to user-friendly messages using the rules above
export const handleChartTypeError = (error: string): string => {
  const rule = errorRules.find((rule) => rule.test(error));
  return rule ? rule.message : DEFAULT_API_ERROR;
};
