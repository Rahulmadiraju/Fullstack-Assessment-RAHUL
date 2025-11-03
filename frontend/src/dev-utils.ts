// dev-utils.ts
// small dev utility with debug console.log as requested
export function devLog(...args: any[]) {
  // one debug console.log in development utility
  console.log("[DEV-UTIL]", ...args);
}
