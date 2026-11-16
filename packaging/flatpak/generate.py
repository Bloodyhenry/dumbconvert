"""Write the Flatpak's dependency lists: every file the build needs, with its address and checksum.

Flatpak builds without the internet, so nothing can be fetched while building: python-wheels.json
lists the Linux wheels (x86_64 and aarch64), cargo-sources.json the Rust crates of NegPy's core.
Run again after changing a package version:   .venv/bin/python packaging/flatpak/generate.py
"""
import json
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PYTHON = "3.14"
# The same package versions as the Mac and Windows builds (maturin builds NegPy's core)
WHEELS = ["PySide6-Essentials==6.12.0", "shiboken6==6.12.0", "numpy==2.5.4", "pillow==13.0.0", "rawpy==0.27.0",
          "tifffile==2026.6.1", "imagecodecs==2026.11.11", "imageio==2.38.1", "piexif==1.1.3", "wgpu==0.31.1",
          "pillow-heif==1.8.1", "maturin==1.16.0"]
SKIP = ("rubicon_objc",)                       # macOS only
ARCHES = {"x86_64": "x86_64", "aarch64": "aarch64"}


def pypi_file(filename: str) -> dict:
    """The download address and sha256 PyPI gives for one wheel file."""
    name, version = filename.split("-")[:2]
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json") as r:
        for f in json.load(r)["urls"]:
            if f["filename"] == filename:
                return {"url": f["url"], "sha256": f["digests"]["sha256"]}
    raise SystemExit(f"{filename} is not on PyPI")


def wheels() -> tuple[list, list]:
    found: dict[str, set] = {}
    for arch in ARCHES:
        with tempfile.TemporaryDirectory() as d:
            platforms = [a for tag in ("manylinux2014", "manylinux_2_17", "manylinux_2_28", "manylinux_2_34", "manylinux_2_39")
                         for a in ("--platform", f"{tag}_{arch}")]
            subprocess.run([sys.executable, "-m", "pip", "download", "-q", "--dest", d, *platforms,
                            "--python-version", PYTHON, "--implementation", "cp", "--only-binary=:all:", *WHEELS], check=True)
            for f in Path(d).glob("*.whl"):
                found.setdefault(f.name, set()).add(arch)
    deps, tools = [], []
    for filename in sorted(found):
        if filename.startswith(SKIP):
            continue
        src = {"type": "file", **pypi_file(filename)}
        if len(found[filename]) < len(ARCHES):          # a wheel for one CPU only
            src["only-arches"] = sorted(found[filename])
        (tools if filename.startswith("maturin") else deps).append(src)
    return deps, tools


def cargo_sources() -> list:
    """crates.io packages from Cargo.lock, laid out as a vendored source cargo can use offline."""
    lock = tomllib.loads((ROOT / "vendor/negpy/negpy_core/Cargo.lock").read_text())
    out = []
    for pkg in lock["package"]:
        if not str(pkg.get("source", "")).startswith("registry+"):
            continue                                     # negpy_core itself
        name, version, checksum = pkg["name"], pkg["version"], pkg["checksum"]
        dest = f"cargo/vendor/{name}-{version}"
        out.append({"type": "archive", "archive-type": "tar-gzip", "sha256": checksum, "dest": dest,
                    "url": f"https://static.crates.io/crates/{name}/{name}-{version}.crate"})
        out.append({"type": "inline", "contents": json.dumps({"package": checksum, "files": {}}),
                    "dest": dest, "dest-filename": ".cargo-checksum.json"})
    out.append({"type": "inline", "dest": "cargo", "dest-filename": "config.toml",
                "contents": '[source.vendored-sources]\ndirectory = "cargo/vendor"\n\n'
                            '[source.crates-io]\nreplace-with = "vendored-sources"\n'})
    return out


if __name__ == "__main__":
    deps, tools = wheels()
    (HERE / "python-wheels.json").write_text(json.dumps(deps, indent=2) + "\n")
    (HERE / "maturin-wheels.json").write_text(json.dumps(tools, indent=2) + "\n")
    crates = cargo_sources()
    (HERE / "cargo-sources.json").write_text(json.dumps(crates, indent=2) + "\n")
    print(f"{len(deps)} wheels, {len(tools)} maturin wheels, {len(crates) // 2} crates")
