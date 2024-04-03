export interface ToolOutput {
  crosshair_output: string[];
  crosshair_valid: boolean[];
  prospector_output: (null | any)[]; // 'any' can be replaced with a more specific type if the structure of the output is known.
  prospector_valid: boolean[];
  session_id: string;
}