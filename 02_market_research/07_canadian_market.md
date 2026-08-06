# The Canadian Exposition & Event Services Market

Research pass conducted 2026-08-06. WebSearch was unavailable this session — all findings below come from direct WebFetch on named URLs. Many target URLs 404'd, DNS-failed, or SSL-failed (noted inline); those are reported as failures, not papered over. Every claim is tagged: **[SOURCED]** = confirmed from a fetched page this session, **[VENDOR]** = a vendor's own claim about itself (self-interested, unverified by a third party), **[INDUSTRY-COMMON]** = widely known in the trade but not sourced this session, **[UNVERIFIED]** = could not confirm, fetch failed, **[SPECULATIVE]** = my own inference/analysis, flagged as such.

---

## 1. Canadian players — who's actually there

- **Stronco** [SOURCED, VENDOR] — Canadian GSC, "over 70 years" in the trade show industry, Ontario-rooted ("A Made in Ontario Story"). Confirmed as the **official/exclusive show services provider at Cohere Centre, Ottawa** (formerly EY Centre) via its own announcement. Services: exhibitions, events, exhibits, creative, logistics.
- **GES Canada** [SOURCED] — has a Toronto office (recently announced a new GM there) and a confirmed **partnership with Rogers Centre Ottawa** (formerly Shaw Centre) — i.e., a *different* GSC than Stronco holds the *other* major Ottawa venue. Active on CPMA 2026 and PDAC. GES's own site (`ges.com/ca/`) is the working Canada portal.
- **Showtech Power & Lighting** [SOURCED, VENDOR] — Canada-wide, but a narrower service layer: electrical, lighting, sign/banner hanging, mechanical. Claims exclusive supplier status "at several major conference venues across Canada" — names not disclosed on its homepage.
- **Levy Show Service** [SOURCED, VENDOR] — full-service GSC (design, exhibits, transportation/customs, floor management, labour, cleaning, AV/rigging) with a dedicated **Canada office in Richmond, BC**; cited safety-partnership work with Vancouver Convention Centre. Reads as a Western Canada regional player.
- **Freeman** [UNVERIFIED] — could not confirm any Canadian presence this session. `freeman.com/locations/canada/` and `where-we-are/` both 404'd; the homepage content fetched contained no Canada reference. This is a fetch-failure gap, not proof Freeman has no Canadian operations — worth a follow-up pass with different URLs.
- **Vancouver Convention Centre's own exclusive-supplier list** (Oct 2022 announcement) [SOURCED] names **Proshow, Riggit, Promosa, and Loungeworks** — none of the "big" national GSC names. This is a real signal: BC's flagship venue runs on regional specialty suppliers, not Freeman/GES/Stronco.

**Market structure verdict:** fragmented, not consolidated. Ottawa alone has two major venues with two *different* exclusive GSCs (Stronco at Cohere/EY, GES at Rogers/Shaw). Vancouver's exclusive roster is entirely regional specialists. No player found holds Canada-wide exclusive lock the way Freeman/GES dominate large swaths of the US. [SPECULATIVE, drawn from the sourced facts above]

## 2. Major venues

| Venue | City | Size (sourced) | Provider notes |
|---|---|---|---|
| Metro Toronto Convention Centre | Toronto | not disclosed | In-house exhibitor services + a "suppliers & partners" list; exclusivity unconfirmed [SOURCED partial] |
| International Centre | Mississauga/GTA | 500,000+ sq ft | Privately owned — rare model for Canada; 500+ events/yr; provider structure undisclosed [SOURCED partial] |
| Vancouver Convention Centre | Vancouver | not disclosed | Exclusive suppliers Proshow/Riggit/Promosa/Loungeworks (2022) [SOURCED] |
| Palais des congrès de Montréal | Montreal | not disclosed | In-house AV/technical/furnishings/food via Exhibitor Order Portal; explicitly notes Charter of the French Language governs consultation of English content [SOURCED] |
| Cohere Centre (ex-EY Centre) | Ottawa | 200,000+ sq ft | Stronco = official show services provider [SOURCED, cross-referenced with Stronco's own site] |
| Rogers Centre Ottawa (ex-Shaw Centre) | Ottawa | 192,000 sq ft | GES partnership announced [SOURCED] |
| Edmonton EXPO Centre | Edmonton | 522,000 sq ft | "Among Western Canada's largest"; 7 halls; approved-vendor directory, no exclusive GSC confirmed [SOURCED partial] |
| Halifax Convention Centre | Halifax | 120,000 sq ft | LEED Silver/AIPC Gold; no provider info disclosed [SOURCED partial] |
| BMO Centre | Calgary | — | **Fetch failed** (404/DNS) [UNVERIFIED] |
| RBC Convention Centre | Winnipeg | — | **Fetch failed** (DNS/parked domain) [UNVERIFIED] |
| Quebec City Convention Centre | Quebec City | — | **Fetch failed** (SSL error) [UNVERIFIED] |

## 3. Canada-specific structural facts

**Bilingual / Bill 96** [SOURCED — Wikipedia + CAI/LégisQuébec redirects confirm the framework]: Extends the Charter of the French Language to businesses with **25–49 employees** (previously 50+ threshold). Software (incl. UIs) **must be available in French unless no French version exists**, deadline **June 2025** (already past). Same June 2025 deadline applied to product packaging/labels/instructions. Commercial signage must have French "markedly predominant." Employers must communicate with employees in French first. Contracts of adhesion default to French. Provision requiring businesses to pay for certified French translation of legal documents was judicially challenged (suspended pending litigation as of Aug 2022) — current status not re-verified this session. Bill 96 also invoked the notwithstanding clause. **This is not a nicety — a Canada-facing SaaS selling into Quebec today is already past the compliance deadline for a French UI.**

**Privacy / Law 25** [SOURCED — direct from CAI, Quebec's privacy regulator]: Staggered rollout — breach notification + regulator registry + administrative penalties (up to **2% of global revenue or $10M CAD**) effective **Sept 2022**; privacy officer designation, new consent standard ("manifeste, libre, éclairé"), and — critically for a SaaS platform — **mandatory privacy impact assessment before transferring personal information outside Quebec**, effective **Sept 2023**; biometric database use requires 60-day advance notice to the regulator. A US-hosted platform selling to Quebec venues/organizers carries a real compliance step (the cross-border PIA) that Canadian-hosted competitors don't.

**PIPEDA** [SOURCED — OPC]: Federal baseline (10 fair-information principles: consent, purpose limitation, accuracy, safeguards, access, accountability). Provinces with "substantially similar" laws (Quebec's Law 25, and similar in BC/Alberta) are generally understood to displace PIPEDA for intra-provincial activity [INDUSTRY-COMMON — not explicitly confirmed on the fetched OPC page].

**Tax (GST/HST/PST/QST)** [SOURCED — rate table]: Five different regimes across the country: GST-only 5% (Alberta, territories), GST+PST (BC 12%, Saskatchewan 11%, Manitoba 12%), HST (Ontario 13%, NB/NL/PEI 15%, **Nova Scotia 14% — reduced from 15% effective April 1, 2025**), and GST+QST in Quebec (14.975% combined). Place-of-supply rules for services specifically **could not be sourced** this session (CRA page 403'd) — flagged as [UNVERIFIED]; general principle that event/venue services are taxed in the province where delivered is [INDUSTRY-COMMON], not confirmed against CRA text.

**Customs / cross-border** [SOURCED — Canadian Chamber of Commerce, the actual issuing body]: **ATA Carnets** are the standard mechanism — the Canadian Chamber of Commerce is Canada's **exclusive national guaranteeing/issuing body** (since 1972), enabling duty/tax-free temporary import (1-year validity) of trade show displays, commercial samples, and professional equipment into 80+ countries, covering essentially all goods except consumables/disposables and repair items. This is the real, genuine pain point flagged in the brief: US exhibitors bringing booth materials into Canada (and vice versa) either use a carnet or face full duty/tax exposure and CBSA temporary-importation paperwork. Today this friction is absorbed as a **service** by GSCs/brokers (Levy Show Service explicitly lists "transportation and customs management" as a line item), not solved by software — worth noting for anyone assuming this is a clean software wedge.

**Accessibility / AODA** [SOURCED — ontario.ca]: Applies to Ontario businesses/nonprofits with **50+ employees**; public-facing websites/content published after Jan 1, 2012 must meet **WCAG 2.0 Level AA**; compliance deadline was **Jan 1, 2021** (already past — no grace period remaining). Internal-only sites (intranet/extranet) are exempt.

**Currency** [INDUSTRY-COMMON, not sourced this session]: CAD is standard; cross-border shows commonly quote US exhibitors in USD. Not independently verified this session.

**Labour/unions** [UNVERIFIED / gap]: Could not source which unions (Teamsters, LiUNA, IATSE) hold jurisdiction over exhibit-floor labour at which Canadian venues. IATSE's own site confirmed only one Canadian local (891, BC/Yukon, motion-picture crews — not exhibit labour). The common industry belief that Canadian venues carry less jurisdictional-craft-split complexity than major US venues (e.g., McCormick Place, Javits) is **[SPECULATIVE]** — I did not verify it and it should not be treated as fact.

## 4. Associations & show organisers

- The `cemaonline.com` domain given in the brief is **not** a Canadian exhibition association — it resolves to the **Corporate Event Marketing Association**, a US-based community for event marketers [SOURCED — correction to the brief's assumption]. I could not locate a live, fetchable "Canadian Exhibition Management Association" site this session — flag as **[UNVERIFIED]**, not confirmed to exist under that name/domain.
- **IAEE** confirmed it has **no Canadian chapters** — only 12 US regional chapters listed on its own chapters page [SOURCED].
- **CMEexpo** (Canadian Meetings + Events Expo) [SOURCED] — a genuine, long-running (34 years) Canadian trade show specifically for meeting/event planners and suppliers; 2026 edition Aug 11–12. This is a real go-to-market venue for a Canadian platform, not a market-structure data source.

## 5. Market sizing

**Could not source any dollar figure, GDP contribution, or event-count statistic for the Canadian exhibition/exposition industry specifically**, despite direct attempts on Destination Canada's business-events site, the (redirected) Business Events Canada portal, CMEexpo, and Wikipedia's trade-show article. Wikipedia's trade-show page cites "10,000+ shows/year" for the **US** with zero comparable Canadian figure. This absence is itself a finding: the sector does not appear to be tracked/published as a standalone Canadian statistic the way US industry bodies (CEIR etc.) track the US market — treat any Canadian market-size number you see elsewhere as an estimate, not a sourced fact, until proven otherwise. **[UNVERIFIED — reported as a gap, not filled with a guess.]**

## 6. Verdict: is Canada-first a real structural opening?

**Yes, but as a beachhead, not a standalone thesis.** Two genuinely defensible, sourced advantages: (1) Bill 96's software-French deadline has *already passed* (June 2025) and Law 25's cross-border-transfer PIA requirement is real and currently a live compliance cost for any US-hosted competitor selling into Quebec — a bilingual, Canadian-hosted platform removes friction competitors carry today, not friction that might someday matter. (2) The market is provably fragmented, not Freeman/GES-locked — Ottawa's two flagship venues run on two different exclusive GSCs, and Vancouver's exclusive roster skips the national names entirely for regional specialists. That means no single incumbent has to be dislodged; the wedge is winning trust with venues/organizers that a US-headquartered platform treats as an afterthought.

**But the honest counterweight is real too:** the total market ceiling could not be sourced at all — not a small number, an *absent* one, and the number of primary venues worth targeting nationally is roughly a dozen. GES already has a Toronto beachhead and an Ottawa venue relationship, so the space isn't virgin. And the sharpest "Canada pain point" in the brief — customs/carnets — is currently solved as a *service* by existing GSCs (Levy explicitly sells it), not as an acute unmet software gap, so a platform still has to prove it beats what a competent local GSC already bundles into its fee. Read this as: real, defensible niche for bilingual + compliance + fragmented mid-market fit — size it as a beachhead into US-capability, not as a business case that stands alone on Canadian volume.
