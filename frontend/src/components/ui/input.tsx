import clsx from "clsx";
import { AnimatePresence, motion } from "framer-motion";

interface InputProps {
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  className?: string;
  error?: string;
}

export const Input = ({
  type = "text",
  placeholder = "",
  value = "",
  onChange = () => {},
  className = "",
  error,
}: InputProps) => {
  return (
    <div className="flex flex-col w-full">
      <input
        className={clsx(
          `flex h-9 w-full rounded-md border-2 bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-green-600 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm`,
          className,
          {
            "border-red-500 focus-visible:ring-red-600": error,
            "border-green-500 focus-visible:ring-green-600": !error,
          }
        )}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <AnimatePresence>
        {error ? (
          <motion.p
            className="mt-1 text-sm text-red-600"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
          >
            {error}
          </motion.p>
        ) : null}
      </AnimatePresence>
    </div>
  );
};
