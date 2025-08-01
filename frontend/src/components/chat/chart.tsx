import type { Figure } from "react-plotly.js";
import React from "react";
import Plot from "react-plotly.js";

interface ChartProps {
  figure: Figure;
}

export const Chart = React.memo(({ figure }: ChartProps) => {
  return (
    <Plot
      data={figure.data}
      layout={{
        ...figure.layout,
        autosize: true,
        margin: { l: 50, r: 20, t: 50, b: 50 },
        // Remove the title
        title: { text: "" },
      }}
      config={{
        responsive: true,
        displayModeBar: false,
      }}
      style={{ width: "100%", height: "auto" }}
    />
  );
});
