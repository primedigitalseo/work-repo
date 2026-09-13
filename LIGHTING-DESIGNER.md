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

## Yardsticks

Place as many as the photo needs. One sets the scale everywhere; two or more get
blended by distance, so a run along the back of the house measures on the
yardstick nearest it instead of the one by the front door. Every measurement
walks the path foot by foot as the local scale changes, rather than dividing one
length by one number.

## Night view

The day-to-night slider is continuous. At night the tool finds the sky in the
photo, darkens it further than the house, and scatters stars through it.

Each run throws light on the wall behind it — beam length, spread, and
brightness are per run, square to the run and washing downward unless you flip
it. Turn the wash off for a run that shouldn't light a surface.

## Known limits

- Lights draw on top of everything — a strand cannot pass behind a tree yet.
- Single fixtures (uplights, wall washers) aren't placeable yet; everything is
  a strand.
- The sky detector wants visible sky in the photo. A tight shot with no sky
  gets the darkening but no stars.

## Two ways to run it

**Hosted link** (easiest) — open the artifact URL. Saved jobs live in a shared
library everyone on the link can open, photos are stored with the job, and PNG
and proposal exports save through the browser. Share it from the page's share
menu to give the crew access.

**The file itself** — download `holiday-lighting-designer.html` and double-click
it. Full features, works offline, nothing leaves the computer. Jobs save as
`.json` files to your own drive instead of the shared library.

The page detects which mode it is in and adjusts the Save and Jobs controls.

## Pricing model

The quote follows the Thunder Lighting Supply estimation sheet rather than a
flat per-foot rate:

- **Materials** come out of the geometry at retail — bulbs by color, socket wire
  by the foot off the spool price, one clip per socket, mini strings by coverage
  (25 ft per 50-count at 6", 17 ft at 4"). The 745-item 2025 price list is built
  in, and the Quote tab searches it for anything else you want on the job.
- **Labor** bills per line with separate install, takedown, and storage rates,
  plus the crew minutes each takes. A run marked *difficult* moves to the higher
  roof-line rate.
- **Contract total** = materials + install + takedown + storage. Tax and a
  deposit percentage sit on top, and next season quotes at labor alone.
- Yours only, never on the proposal: wholesale cost, margin on materials, crew
  hours, and the electrical load in watts, amps, and circuits.

Rates are editable on the Pricing tab and saved per browser. Prices are 2025;
swap in a newer list by sending the distributor's spreadsheet.
