"""Count sargassum in MARIDA: patches (from labels_mapping.txt) and,
optionally, pixels (from the *_cl.tif class masks).

Usage:
    python scripts/count_sargassum.py --marida "C:/path/to/MARIDA"
    python scripts/count_sargassum.py --marida "C:/path/to/MARIDA" --pixels

--pixels needs rasterio (pip install rasterio). In the _cl masks, pixel
value = class code 1-15 and 0 = unlabelled.

labels_mapping.txt maps each 256x256 patch to a 15-slot multi-hot list
(1 = class present in the patch). Class order follows MARIDA's _cl mask codes
1-15 (MARIDA GitHub README), so list index 1 = Dense Sargassum (code 2) and
index 2 = Sparse Sargassum (code 3).
"""
import argparse
import json
from collections import Counter
from pathlib import Path

CLASSES = [
    "Marine Debris", "Dense Sargassum", "Sparse Sargassum",
    "Natural Organic Material", "Ship", "Clouds", "Marine Water",
    "Sediment-Laden Water", "Foam", "Turbid Water", "Shallow Water",
    "Waves", "Cloud Shadows", "Wakes", "Mixed Water",
]
DENSE, SPARSE = 1, 2  # list indices in labels_mapping.txt


def scene_of(patch_name: str) -> str:
    """'S2_1-12-19_48MYU_0.tif' -> 'S2_1-12-19_48MYU' (date + tile)."""
    return patch_name.rsplit("_", 1)[0]


def load_split(marida: Path, name: str) -> set:
    """Split files list patch ids without 'S2_' prefix or '.tif'."""
    path = marida / "splits" / f"{name}_X.txt"
    return {f"S2_{line.strip()}.tif" for line in path.read_text().split() if line.strip()}


def count_pixels(marida: Path, patches) -> Counter:
    """Sum pixels per class code over the given patches' _cl masks."""
    import numpy as np
    import rasterio

    totals = Counter()
    for name in patches:
        mask_path = marida / "patches" / scene_of(name) / name.replace(".tif", "_cl.tif")
        with rasterio.open(mask_path) as src:
            mask = src.read(1)
        codes, counts = np.unique(mask, return_counts=True)
        totals.update(dict(zip(codes.tolist(), counts.tolist())))
    return totals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--marida", type=Path, required=True)
    parser.add_argument("--pixels", action="store_true",
                        help="also count pixels per class from the _cl masks")
    args = parser.parse_args()

    labels = json.loads((args.marida / "labels_mapping.txt").read_text())
    splits = {s: load_split(args.marida, s) for s in ("train", "val", "test")}

    dense = {p for p, v in labels.items() if v[DENSE]}
    sparse = {p for p, v in labels.items() if v[SPARSE]}
    either = dense | sparse

    print(f"Total patches: {len(labels)} from {len({scene_of(p) for p in labels})} scenes")
    print(f"Dense Sargassum patches:  {len(dense)}")
    print(f"Sparse Sargassum patches: {len(sparse)}")
    print(f"Either (union):           {len(either)}  ({len(dense & sparse)} have both)")

    print("\nSargassum patches per split:")
    for name, ids in splits.items():
        print(f"  {name:5s}: {len(either & ids)} of {len(ids)}")
    unassigned = either - set().union(*splits.values())
    if unassigned:
        print(f"  not in any split: {len(unassigned)}")

    scenes = Counter(scene_of(p) for p in either)
    print(f"\nScenes containing sargassum: {len(scenes)}")
    for scene, n in sorted(scenes.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {scene}: {n} patches")

    if args.pixels:
        totals = count_pixels(args.marida, labels)
        labelled = sum(n for code, n in totals.items() if code != 0)
        dense_px, sparse_px = totals[DENSE + 1], totals[SPARSE + 1]  # codes 2, 3
        print("\nPixels (all patches):")
        print(f"  Total pixels:     {sum(totals.values()):,}")
        print(f"  Labelled pixels:  {labelled:,}")
        for code in range(1, 16):
            share = 100 * totals[code] / labelled if labelled else 0
            print(f"  {code:2d} {CLASSES[code - 1]:25s} {totals[code]:>9,}  ({share:.2f}% of labelled)")
        sarg_px = dense_px + sparse_px
        print(f"\nSargassum pixels (dense + sparse): {sarg_px:,}")
        print(f"Average per sargassum patch: {sarg_px / len(either):.1f} of 65,536 pixels")


if __name__ == "__main__":
    main()
