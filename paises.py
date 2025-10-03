<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>REST Countries — Card</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  </head>

  <body class="bg-dark text-light min-vh-100 d-flex align-items-center">
    <div class="container">
      <div id="alertBox" class="alert d-none" role="alert"></div>

      <div id="cardContainer" class="row justify-content-center">
        <!-- spinner inicial -->
        <div class="col-12 d-flex justify-content-center py-5" id="spinnerBox">
          <div class="text-center">
            <div class="spinner-border" role="status"></div>
            <div class="mt-2">Cargando países...</div>
          </div>
        </div>
      </div>
    </div>

    <script>
      const API = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,languages,currencies,flags";
      let countries = [];

      function showAlert(type, msg) {
        const box = document.getElementById("alertBox");
        box.className = `alert alert-${type}`;
        box.textContent = msg;
        box.classList.remove("d-none");
      }
      function hideAlert() {
        document.getElementById("alertBox").classList.add("d-none");
      }

      async function loadCountries() {
        hideAlert();
        try {
          const resp = await fetch(API, { cache: "no-store" });
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
          countries = await resp.json();
          if (!Array.isArray(countries) || !countries.length) {
            throw new Error("No se recibieron países.");
          }
          showRandomCountry();
        } catch (err) {
          console.error(err);
          document.getElementById("spinnerBox")?.remove();
          showAlert("danger", `Error al cargar países: ${err.message}`);
        }
      }

      function fmtPopulation(n) {
        try { return Number(n).toLocaleString("es-ES"); } catch { return n || "—"; }
      }

      function showRandomCountry() {
        hideAlert();
        document.getElementById("spinnerBox")?.remove();
        if (!countries.length) return;

        const c = countries[Math.floor(Math.random() * countries.length)];

        const name = (c.name && (c.name.common || c.name.official)) || "—";
        const official = (c.name && c.name.official) || "—";
        const capital = Array.isArray(c.capital) && c.capital.length ? c.capital.join(", ") : "—";
        const region = c.region || "—";
        const subregion = c.subregion || "—";
        const population = fmtPopulation(c.population);
        const languages = c.languages ? Object.values(c.languages).join(", ") : "—";
        const currencies = c.currencies ? Object.values(c.currencies).map(x => x.name).join(", ") : "—";
        const flag = (c.flags && (c.flags.svg || c.flags.png)) || "";

        const container = document.getElementById("cardContainer");
        container.innerHTML = `
          <div class="col-12 col-md-8 col-lg-6 col-xl-4">
            <div class="card text-dark shadow-lg">
              ${flag ? `<img src="${flag}" class="card-img-top" alt="Bandera de ${name}">` : ""}
              <div class="card-body">
                <h5 class="card-title fw-bold">${name}</h5>
                <p class="card-text mb-1"><strong>Nombre oficial:</strong> ${official}</p>
                <p class="card-text mb-1"><strong>Capital:</strong> ${capital}</p>
                <p class="card-text mb-1"><strong>Región:</strong> ${region} (${subregion})</p>
                <p class="card-text mb-1"><strong>Población:</strong> ${population}</p>
                <p class="card-text mb-1"><strong>Idiomas:</strong> ${languages}</p>
                <p class="card-text"><strong>Moneda(s):</strong> ${currencies}</p>
                <div class="d-grid gap-2">
                  <button class="btn btn-primary" id="btnOtro">Otro país</button>
                </div>
              </div>
            </div>
          </div>
        `;

        document.getElementById("btnOtro").addEventListener("click", showRandomCountry);
      }

      loadCountries();
    </script>
  </body>
</html>