const RAW = import.meta.env.VITE_BACKEND_URL;

// Remove trailing slash if present
const API = RAW.endsWith("/") ? RAW.slice(0, -1) : RAW;

export async function askGrievance(query) {
  const response = await fetch(`${API}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Backend error");
  }

  return response.json();
}
