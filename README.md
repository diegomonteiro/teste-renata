# LAZ -> GeoTIFF (SIRGAS 2000)

Aplicação web em Python para:
- Upload de arquivos `.laz`
- Agendamento/execução de processamento em background
- Acompanhamento de status com barra de progresso
- Geração de `.tif` em SIRGAS 2000 (`EPSG:4674`) via PDAL

## Executar com Docker

```bash
docker compose up --build
```

Acesse: `http://localhost:8000`

## Executar localmente

Pré-requisitos:
- Python 3.11+
- Bibliotecas de sistema: PDAL e GDAL instaladas

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Fluxo da aplicação

1. Usuário envia `.laz` pela interface.
2. API cria um job com status `queued`.
3. Worker em thread de background executa pipeline PDAL.
4. Frontend consulta `/api/jobs/{job_id}` a cada 2 segundos.
5. Ao concluir, o usuário baixa o `.tif` gerado.
