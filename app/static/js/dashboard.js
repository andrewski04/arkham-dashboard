// content stored in static will be directly accessible at the `/static` path.
// static content will store javascript, css, images, etc.

// dashboard.js shows an example of fetching data from the API.

document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/network-monitoring/");
  const data = await res.json();
  document.getElementById("network-status").innerText = JSON.stringify(
    data,
    null,
    2
  );
});
