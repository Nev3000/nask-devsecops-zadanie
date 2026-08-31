## Jak uruchomić całość

### Wymagania
- Docker
- Docker Compose
- Git

### Uruchomienie

1. Sklonuj repozytorium:
```bash
   git clone https://github.com/Nev3000/nask-devsecops-zadanie.git
   cd nask-devsecops-zadanie
```

2. Uruchom cały stos jednym poleceniem:
```bash
   docker-compose up
```

3. Po uruchomieniu, dostępne są:
   - **Aplikacja (Swagger UI)**: http://127.0.0.1:8000/docs - tutaj można przetestować wszystkie endpointy API
   - **Grafana**: http://localhost:3000 - tutaj można przeglądać logi aplikacji

### Konfiguracja źródła danych logów w Grafanie

Po pierwszym uruchomieniu trzeba ręcznie podłączyć Loki jako źródło danych:

1. W Grafanie: **Data sources -> Add data source → Loki**
2. W polu URL wpisz: `http://loki:3100`
3. Kliknij **Save & test**

### Przeglądanie logów

1. Przejdź do **Explore**
2. Skorzystaj z **Label browser**, wybierz etykietę `container`
3. Wybierz konkretny kontener, którego logi chcesz zobaczyć

## Jakie narzędzia wybrałem i dlaczego

### Aplikacja

Do stworzenia aplikacji wykorzystałem język Python oraz framework FastAPI, napisany właśnie w tym języku. Wynika to ze ścieżki mojego rozwoju zawodowego — obecnie sporą część czasu spędzam na poszerzaniu wiedzy dot. Pythona w zastosowaniach DevSecOps. FastAPI wykorzystuje Swaggera, interaktywną dokumentację, która ułatwia testowanie endpointów bez dodatkowych narzędzi. Pydantic jest ściśle powiązany z FastAPI i pozwala na szybką walidację danych wychodzących oraz przychodzących.

Faker został wybrany, by generować wiarygodne dane bez importowania bazy danych, co niepotrzebnie wydłużałoby proces tworzenia aplikacji.

Przechowywanie danych in-memory – wymóg zadania; poza tym, jak już wspomniałem, baza danych wydłużyłaby proces tworzenia aplikacji, testując przy tym inne umiejętności niż te, które zadanie faktycznie sprawdza.

### Konteneryzacja

`python:3.12-slim` jako obraz bazowy - wersja slim zawiera mniej pakietów systemowych niż pełny obraz, co ogranicza potencjalny wektor ataku.

Uruchamianie kontenera jako użytkownik non-root — domyślnie kontenery Dockera uruchamiają procesy jako root, co jest ryzykowne: gdyby aplikacja została skompromitowana przez podatność, atakujący od razu miałby pełne uprawnienia roota wewnątrz kontenera, co ułatwiłoby dalszą eskalację.

### Stos logów

Wybrałem Loki + Promtail + Grafana jako lżejszą alternatywę dla pełnego ELK Stack (Elasticsearch + Logstash + Kibana) — mniejsze zużycie zasobów i prostsza konfiguracja miały znaczenie przy uruchamianiu całości lokalnie.

### CI/CD

- **GitHub Actions** - posiadam już repozytorium na GitHubie, więc naturalną koleją rzeczy było wykorzystanie GitHub Actions.
- **Ruff** - szybki, nowoczesny linter, który łączy funkcje starszych narzędzi, np. flake8.
- **Bandit** - narzędzie wykorzystywane do przeprowadzenia SAST w projekcie, standard w branży.
- **Trivy** - było mi już wcześniej znane z przygotowań do rozmowy kwalifikacyjnej. Testowałem je praktycznie, skanując publiczne obrazy Docker i analizując strukturę raportów podatności, co ułatwiło mi świadome wdrożenie go w tym pipeline.

**Decyzja o Quality Gate opartym na `ignore-unfixed`:** w trakcie testowania Trivy na własnym obrazie wykryłem 3 podatności CRITICAL w pakiecie `perl-base`. Żadna z nich nie miała jeszcze dostępnej wersji naprawiającej (status `affected`/`fix_deferred`). Bezwarunkowe blokowanie pipeline'u na te podatności skutkowałoby trwale zablokowanym Quality Gate, co mijałoby się z celem całego mechanizmu. Dlatego zastosowałem flagę `ignore-unfixed: true`, dzięki której Trivy nadal wykrywa i raportuje te podatności (widoczne w artefakcie `trivy-report.json`), ale blokuje pipeline tylko na podatności CRITICAL, dla których faktycznie istnieje dostępna poprawka.

## Co bym zmienił/dodał mając więcej czasu

### Aplikacja
- Model `DeviceCreate`/`Device` ma zduplikowane pola — w środowisku produkcyjnym oczywistym rozwiązaniem byłoby wykorzystanie klasy bazowej, żeby nie powtarzać kodu i unikać pomyłek.
- Brak testów jednostkowych (pytest) — powinny się one znaleźć w projekcie.
- Prawdziwa baza danych zamiast in-memory storage — w środowisku produkcyjnym oczywistym wyborem byłoby wykorzystanie bazy danych do trwałego przechowywania rekordów.
- Walidacja `ip_address` — obecnie jest to zwykły string; przy większej ilości czasu można byłoby wykorzystać dedykowany typ Pydantic odpowiadający za faktyczną walidację formatu adresu IP.

### Bezpieczeństwo/konfiguracja
- `GF_AUTH_ANONYMOUS_ENABLED=true` — na potrzeby testu i wygody prowadzenia projektu został zostawiony anonimowy dostęp administracyjny do Grafany; w środowisku produkcyjnym absolutnie niedopuszczalne.
- Używanie tagów `latest` dla obrazów Loki/Promtail/Grafana — nieprzewidywalne, obrazy mogą się zmienić w dowolnym momencie bez ostrzeżenia.
- Hardkodowanie portów w `docker-compose.yml` zamiast przez zmienne środowiskowe — wygodniejsze, lecz mniej elastyczne między środowiskami.

### CI/CD
- Mniej rozbudowane Quality Gate - obecna wersja blokuje pipeline na podstawie samego wyniku Trivy; w środowisku produkcyjnym wykorzystałbym połączenie wyników obu skanerów (Bandit + Trivy) do bardziej precyzyjnej decyzji.
- Skanowanie sekretów (np. Gitleaks) - z powodu braku czasu nie udało się tego wdrożyć, mimo że to standardowy element pełnego pipeline'u shift-left security.

### Frontend
- Napisanie prostego frontendu (np. HTML + CSS) do wygodniejszej pracy z aplikacją. To nie jest praca typowo DevSecOps, ale urozmaiciłoby projekt i ułatwiło demonstrację API bez konieczności korzystania ze Swaggera.