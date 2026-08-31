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