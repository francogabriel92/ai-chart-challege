import type { Figure } from "react-plotly.js";
import { API_URL } from "@/utils/config";
import type { ApiError } from "@/types/api";

export interface ChartRequest {
  question: string;
}

export interface ChartResponse {
  chart: Figure;
}

/**
 * ChartService handles requests related to chart generation.
 */
class ChartService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = API_URL;
  }
  /**
   * Requests a chart based on the provided question.
   * @param question The question to generate a chart for.
   * @returns A promise that resolves to the chart data.
   */
  async requestChart(question: string): Promise<ChartResponse> {
    const response = await fetch(`${this.apiUrl}charts/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    // Check if the response is ok (status in the range 200-299)
    if (!response.ok) {
      const responseDetailed = (await response.json()) as ApiError;
      throw new Error(`Error: ${response.status} ${responseDetailed.detail}`);
    }

    return response.json();
  }
}

export const chartService = new ChartService();
