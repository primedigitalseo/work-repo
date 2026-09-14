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

## What you can draw

| Product | Bills as | Notes |
|---|---|---|
| C9 12/15/18/24/36", C7 6/12" | bulbs + spool wire by the foot + a clip per socket | colour per socket from the pattern |
| Permanent RGBWW C9 8/12" | one fixture SKU for every colour, plus a 500-count controller per job | wash starts wide, since these are aimed at the wall |
| 5mm mini 4/6" | 50-count strings, 17 ft and 25 ft of coverage | |
| Lit garland, warm white or RGB | 9 ft sticks | |

Placed decor — wreaths, sparkler snowflakes, spritzers, bows, mini trees — goes
on with the Decor tool and prices from its catalog SKU. Anything else in the
745-item list can be searched and placed the same way.

Pattern slots take a named colour, a raw hex, or an empty socket. **Rainbow**
fills twelve evenly spaced hues, which is what a permanent-lighting controller
sweeps. **Tight** and **Wide wash** set the whole beam group in one click.

## Wraps

Draw a column, post, or trunk as a line up its height and turn on **Wrap**. The
strand spirals, so the footage it consumes is several times the height:

    ((width + depth) x 2 x (height / spacing + 1) + height) / 12     square
    (girth x (height / spacing + 1) + height) / 12                   round

An 8 in column 15.4 ft tall, wrapped every 12 in, takes 59.2 ft of strand
against the 15.4 ft you drew. Column and tree runs start wrapped; everything
else starts straight. The quote bills strand feet and reports the drawn length
separately.

Each run can also override which labor line it bills against, since a post wrap
and a canopy wrap are priced differently.

## Night view

The day-to-night slider is continuous. At night the sky is replaced — found in
the photo, taken to deep navy, and filled with stars — while the house itself
barely moves. A customer wants to see their own house and the lights on it, so
the render stays legible rather than photoreal-dark.

Each run throws light on the wall behind it — beam length, spread, and
brightness are per run, square to the run and washing downward unless you flip
it. Turn the wash off for a run that shouldn't light a surface.

## Known limits

- Lights draw on top of everything — a strand cannot pass behind a tree yet.
- Single fixtures (uplights, wall washers) aren't placeable yet; everything is
  a strand.
- The sky detector wants visible sky in the photo. A tight shot with no sky
  gets the darkening but no stars.
- A wrapped run still draws as a line of lights up the post rather than a
  spiral. The quote is right; the picture is an approximation.

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

Rates are editable on the Pricing tab and saved per browser.

## Where the prices come from

821 items. The 2025 estimation workbook supplies every description and
category; the 2026 catalog supplies current prices wherever its scan matched a
SKU — 282 of them, plus 76 SKUs the 2025 workbook never had.

The rest still carry 2025 prices and say so: a **2025** badge follows the SKU in
every search result and on the quote, and the quote counts how many lines are
affected. Six rows the scan read badly (a missing price, wholesale above retail,
a 279% jump) kept their 2025 price and are listed on the Pricing tab with their
catalog page number.

**Fill the gaps** on the Pricing tab lists everything still unknown, grouped by
the section of the catalog it belongs to, so one pass with the wholesale
catalog open clears it. Only the wholesale catalog carries prices; the retail
one is the same product line with prices removed. The two paginate differently,
so every page reference names its book, and pages taken from the retail scan
have been shifted to the printed number rather than the flipbook position. Each
row takes a typed price or a **Still right** click, which settles it without
changing anything. Prices barely moved between the 2025 and 2026 catalogs —
median change zero — so most rows are one click.

A price at or below cost cannot be right, so the tool refuses to let one out
quietly: the SKU is marked in search, the quote lists every affected line with
its catalog page, and the proposal asks before it prints.

## Where the prices come from

Thunder's 2026 estimation workbook carries its own price list sheet — 831 SKUs
with cost, customer price, wattage, voltage and colour temperature. Every line
is cross-checked against the 2026 wholesale PDF, which agrees on all but one
row and adds catalog pages plus bulk-buy pricing for 55 items.

That is the whole catalog now: no OCR, no guesses, no placeholder names. A
further 147 SKUs are held over from the 2025 workbook because the 2026 list
drops them; they stay searchable and are marked **dropped**.

## Which bulbs you stock

The 2026 list prices each bulb colour by LED series — **SPK** at 2600K, **MIN**
at 2850–2950K, **HBL** at 3000K — where older lists used one bare SKU. Greenery
splits the same way, as -27 or -30. Pick your series on the Pricing tab and
every quote resolves to it: red C9 becomes 20309-SPK, a 48 in wreath becomes
50048-27.

## What you charge

The Pricing tab takes a **price basis**. Thunder's suggested retail is the
default. Switch to **my markup on cost** and the quote prices everything off
your own number — one markup for the job, or a different one per category, with
anything you typed on a single SKU still winning over both.

Markup is on cost, so 65% markup is a 39% margin. The quote names the basis it
used and reports margin in dollars and percent.

The category table shows Thunder's own margin beside yours, because their
suggested retail is nowhere near a flat markup:

| Category | Their margin | | Category | Their margin |
|---|---|---|---|---|
| C7/C9 bulbs | 54% | | Hardware | 24% |
| Bulbs | 49% | | Resin | 23% |
| C9/C7 wire | 38% | | Lightburst | 19% |
| Socket cord | 34% | | Mini lights | 17% |
| Spritzers | 32% | | Bows | 15% |
| Clips | 28% | | Metal framed | 15% |
| Bistro | 26% | | RGB | 14% |
| Coaxial | 26% | | Greenery | 11% |

Quote off their retail and your margin swings with the product mix — a roofline
job of bulbs, wire and clips lands near 42%, a decor-heavy job near 12%.
**Match Thunder category by category** fills the table with their own numbers as
a starting point; move up from there.

Search any SKU on the Pricing tab and type over its cost or customer price. Your
number wins over both catalogs, is saved in that browser, and the row is marked
**yours**. That is the fastest fix for the SKUs the scan missed — the C9 spools,
the wreaths, the garland and the warm white C9 bulb among them.
