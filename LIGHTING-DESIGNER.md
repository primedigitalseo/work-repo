# Holiday Lighting Designer

Internal tool for mocking up holiday lighting jobs on a photo of the customer's
house and turning the drawing into a priced estimate.

`holiday-lighting-designer.html` is the whole thing — one file, no server, no
install. Double-click it, or drop it in Drive/Dropbox and open it from there.
Nothing is uploaded anywhere; the photo and the design stay on your machine.

## Using it on a job

1. **Photo** — drag a photo of the house onto the canvas.
2. **Scale** — pick the Scale tool and drag a line across something you know the
   size of, then type that length. A single garage door is 8 ft, a double is 16 ft,
   a standard front door is 6.7 ft. Footage stays a rough guess until you do this.
3. **Draw** — click along the roofline to drop points, press Enter to finish.
   Set the run type, product, and color pattern before or after drawing.
4. **Night view** — toggle it to show the customer what the house looks like lit.
5. **Quote** — the tab tallies linear feet, bulbs, and price from your price list.
   Add wreaths, garland, and mini trees there.
6. **Proposal** — opens a print view with both renders and the estimate. Print to
   PDF from the browser dialog.
7. **Save** — writes a `.json` file that embeds the photo. Reopen it next season
   with **Open**, change the colors, and re-quote in a minute.

## Setting your prices

The **Pricing** tab holds per-foot prices, add-on prices, your minimum job, and
your company name. Those numbers ship as placeholders — replace them with your
real ones. They are saved in that browser, so each computer needs it done once.

## Keyboard

`V` select · `D` draw · `C` scale · `N` night view · `Enter` finish a run ·
`Esc` cancel · `Del` delete the selected run · `Ctrl+Z` undo ·
scroll to zoom · drag the background to pan

## Known limits

- One scale reference per photo, so runs much farther from the camera than your
  reference will measure a little short. Calibrate on something near the runs
  that matter most.
- Lights draw on top of everything — a strand cannot pass behind a tree yet.
- Labor is folded into the per-foot price rather than tracked separately.
