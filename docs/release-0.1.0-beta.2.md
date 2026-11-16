# DumbConvert 0.1.0 beta 2

The second public beta. A simple film-negative converter for the Mac: drop camera scans in, get
good colour straight away, nudge a few faders, export.

## Install

1. Download `DumbConvert-0.1.0-beta.2-macos-arm64.zip` below and unzip it.
2. Move **DumbConvert** to Applications.
3. The beta is not signed by Apple. Open it once and click **Done**, then go to
   **System Settings › Privacy & Security** and click **Open Anyway**. On macOS 14 or older:
   right-click the app, choose **Open**, then **Open**.

Apple Silicon Macs only.

## New in beta 2

- **Contact sheet** of a whole roll, with film edges, from the roll's details.
- **Clean Area:** draw around a part of the photo and the dust and scratches inside it are removed.
- **Auto crop levels tilted scans**, so no light around the film is left in the corners. Auto is a
  switch: a second click gives the frame back as it was.
- **Tools take over:** while cropping, healing or cleaning, the rest of the window steps back until you are done.
- **New default keys:** hold Q W E (density, contrast, saturation) or A S D (cyan, magenta, yellow) and
  press ↑ / ↓. Saved key layouts start again from these.
- **A softer look:** rounded sections, a violet second accent, clearer text hierarchy.
- **Export fixes:** PNG stays 16-bit, print-size exports keep their dpi, JPEG XL with Adobe RGB no longer
  fails, DNG metadata is written where raw editors expect it. The two DNG kinds are now called
  compact (recommended) and lossless.

## What it does

- Converts colour and B&W negatives scanned with a digital camera over a white light.
- Rolls are measured together so their colours match; single frames on their own.
- Density, contrast, saturation and cyan / magenta / yellow faders, like a lab scanner.
- Crop to film formats, straighten, rotate, heal dust, full-screen view.
- Film stock, camera, lens, date and place written into the exported files.
- Exports JPEG, HEIC, TIFF, PNG, AVIF, JPEG XL, WebP, and DNG for your raw editor.
- Works from the keyboard; every key can be changed.

## Known limits of this beta

- Not signed or notarized by Apple (see Install).
- Tested on one Mac with 16 GB of memory. Exporting many large scans at full resolution uses
  several GB; on an 8 GB Mac, large scans are exported one at a time.
- Adjustments are not kept between sessions: export before you quit (the app reminds you).
- The automatic colour was tuned on a small set of white-light scans. If your colours look
  off, please open an issue and say which camera, light and film you used.

Built on [NegPy](https://github.com/marcinz606/NegPy). GPLv3.
