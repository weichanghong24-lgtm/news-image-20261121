# Build log — make.fun bounty `news-image-20261121`

- Bounty: "Sum up 21 November's world news in one image"
  (https://make.fun/bounty/news-image-20261121), prize $100 (50 places paid:
  1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each),
  deadline 2026-11-23 00:00 UTC (01:00 CET).
- Built: 2026-11-21 ~22:30 CET. Build only at this point; repo and submission
  follow the same steps as news-image-20261120.

## Specs followed

Read `https://make.fun/skill.md` and
`GET https://make.fun/api/competitions/news-image-20261121/requirements`
(harness `program/v1`). Key rules applied:

- Entrypoint `main.py` at repo root, run as `python3 -P -s /bot/main.py`
  (Python 3.13), standard library only, no network, 60 s wall budget, 1 CPU,
  512 MB, read-only repo at `/bot`, empty writable `/output`.
- Program writes one image to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
  `/output/entry.png`); whole PNG, at most 1 MiB and 1024×1024 px.
- Two runs must write identical bytes. The brief explicitly allows the
  simplest program: one that copies an image the repository holds.

## News chosen (Saturday 21 November 2026)

Verified from reporting published 21 Nov 2026: One Turn day brief
("Markets Slide; Mexico Captures Cartel Boss"), NYT, AP, Xinhua, SCMP,
The Peninsula.

1. **Lead — Markets:** AI sell-off sweeps world markets; S&P 500 −3.7% on
   Friday, Nikkei −5.06%, rout spreading across Asia and Europe.
2. **Mexico:** troops captured FBI most-wanted cartel boss Fausto Isidro
   Meza Flores ("El Chapo Isidro") in Guasave, Sinaloa; violence followed.
3. **Ukraine:** Russian missile struck central Kryvyi Rih, killing two and
   wounding 60; Russia fired 3 missiles and 148 drones overnight.
4. **Climate — COP31:** summit in Antalya, Turkey, overran its Friday
   deadline as talks stalled over fossil fuels.
5. **Iran:** Trump weighing another round of extensive strikes as Israel
   presses for quick action; he also said Iran wants a deal but rejects
   US terms.
6. **Britain & Europe:** UK and EU struck a landmark deal to rebuild ties:
   agri-food trade eased, carbon markets linked, youth mobility restored.
7. **Also strip:** M7.2 quake hits Indonesia's Maluku; Brazil trial: dengue
   cases down 69%; BepiColombo reaches Mercury orbit after 8 years; Trump
   threatens a "tremendous tax" on US firms building data centres abroad.

## What the program does

- `build_image.py` — build-time generator (Pillow + DejaVu fonts on this
  machine). Renders the newspaper-style poster from the news text embedded
  in the script. Kept in the repo for provenance; the entry program does not
  run it. Layout fixes during the build: Ukraine cell body overflowed its
  box (trimmed to three lines), the ALSO band ran past the footer (shortened
  to four items, smaller type, tighter gaps). Final image inspected visually:
  clean, nothing clipped.
- `entry.png` — finished image, 1024×1024, 138,217 bytes.
- `main.py` — entrypoint. Stdlib only (`os`, `shutil`); copies the bundled
  `entry.png` byte for byte to `$MAKEFUN_OUTPUT_DIR/entry.png`. No network,
  no clock, no randomness.
- `README.md`, `LICENSE` (MIT, required repo file).

## Determinism verification

Grader-style invocation, two runs into separate empty output dirs:

```
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 -P -s main.py   -> exit 0
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 -P -s main.py   -> exit 0
```

SHA-256 (all three identical):

```
87366f5867559f7007cb7aad831cd4b2218b999cca4d15c7508f9a0234ad8f6e  entry.png
87366f5867559f7007cb7aad831cd4b2218b999cca4d15c7508f9a0234ad8f6e  /tmp/out1/entry.png
87366f5867559f7007cb7aad831cd4b2218b999cca4d15c7508f9a0234ad8f6e  /tmp/out2/entry.png
```

Output checks: 1024×1024 PNG, 138,217 bytes (limit 1,048,576).

## Requirements status

All met. Next steps for submission (same as news-image-20261120): download
this competition's kit, create public repo
`weichanghong24-lgtm/news-image-20261121` with these files, bundle
transcripts with the make.fun kit CLI, submit before 2026-11-23 01:00 CET.
