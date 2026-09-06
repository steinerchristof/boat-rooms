# boat-rooms

Walkable room impressions of a boat, generated from the photos of a sales listing.

Each listing photo becomes one small 3D Gaussian splat world. The viewer shows one room at a time with a room menu, mouse or touch look, and WASD walking. Everything outside the original photo frame is filled in by the model, so the page is labelled as an AI impression and not as the actual boat.

## Stack

- Generation: [FlashWorld](https://github.com/imlixinyang/FlashWorld) (Apache 2.0), single image to 3DGS, run locally in WSL2 on an RTX 5090 Laptop with all offload flags.
- Viewer: [Spark](https://sparkjs.dev) 2.1 on three.js 0.180, loaded from CDN, no build step.
- Hosting: GitHub Pages from `main`. Rooms live in `rooms/<room>.spz`.

## Add a room

1. Pick one wide interior photo per room.
2. Build the input JSON with `make_inputs.py` (24-frame walk-in trajectory).
3. Run `cli.py --ply --spz --offload_t5 --offload_transformer_during_vae --offload_vae`.
4. Optionally crop floaters in [SuperSplat](https://supersplat.at) and re-export as SPZ.
5. Copy to `rooms/<room>.spz`, add the room to the `ROOMS` list in `index.html`, push.
