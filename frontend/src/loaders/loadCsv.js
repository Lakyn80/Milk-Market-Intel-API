import Papa from "papaparse";

export async function loadCsv(relativePath) {
  const response = await fetch(relativePath);
  if (!response.ok) {
    throw new Error(`Failed to load CSV: ${relativePath}`);
  }
  const text = await response.text();
  const parsed = Papa.parse(text, {
    header: true,
    skipEmptyLines: true,
  });
  return parsed.data;
}
