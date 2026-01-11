export async function askGrievance(query) {
    const response = await fetch("http://127.0.0.1:8000/ask", {
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
  