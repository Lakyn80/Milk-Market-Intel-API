export async function loadJson(relativePath) {
  const url = new URL(relativePath, import.meta.url).toString();
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load JSON: ${relativePath}`);
  }
  return response.json();
}
