export async function loadJson(relativePath) {
  const response = await fetch(relativePath);
  if (!response.ok) {
    throw new Error(`Failed to load JSON: ${relativePath}`);
  }
  return response.json();
}
