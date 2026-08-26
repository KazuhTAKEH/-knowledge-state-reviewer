export function normalizeNameTs(name: string): string {
  return name.trim().toLowerCase();
}

export function buildGreetingTs(name: string): string {
  const normalized = normalizeNameTs(name);
  return `hello ${normalized}`;
}
