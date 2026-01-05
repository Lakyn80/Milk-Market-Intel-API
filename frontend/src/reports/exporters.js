function triggerDownload(path, filename) {
  const link = document.createElement("a");
  link.href = path;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export function exportCsv(path, filename) {
  triggerDownload(path, filename);
}

export function exportJson(path, filename) {
  triggerDownload(path, filename);
}
