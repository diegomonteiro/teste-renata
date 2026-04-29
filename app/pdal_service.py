from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def build_pipeline(input_path: Path, output_path: Path) -> str:
    pipeline = [
        {
            "type": "readers.las",
            "filename": str(input_path),
            "override_srs": "EPSG:4674",
        },
        {
            "type": "filters.reprojection",
            "in_srs": "EPSG:4674",
            "out_srs": "EPSG:4674",
        },
        {
            "type": "writers.gdal",
            "filename": str(output_path),
            "gdaldriver": "GTiff",
            "output_type": "idw",
            "resolution": 1.0,
            "radius": 1.5,
            "nodata": -9999,
            "override_srs": "EPSG:4674",
        },
    ]
    return json.dumps(pipeline)


def process_laz_to_tif(input_path: Path, output_path: Path) -> None:
    pdal_bin = shutil.which("pdal")
    if not pdal_bin:
        raise RuntimeError("Executável 'pdal' não encontrado no container.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pipeline_json = build_pipeline(input_path, output_path)

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        tmp.write(pipeline_json)
        pipeline_path = Path(tmp.name)

    try:
        result = subprocess.run(  # noqa: S603
            [pdal_bin, "pipeline", str(pipeline_path)],
            check=False,
            capture_output=True,
            text=True,
        )
    finally:
        pipeline_path.unlink(missing_ok=True)

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        log_tail = stderr[-1200:] if stderr else stdout[-1200:]
        raise RuntimeError(f"Falha ao executar PDAL CLI (code={result.returncode}): {log_tail}")

    if not output_path.exists():
        raise RuntimeError("Saída .tif não foi criada após a execução do pipeline.")
